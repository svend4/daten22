"""
Query Engine for MBTI RAG System
Handles search and answer generation
"""
import sys
from pathlib import Path
from typing import List, Dict, Optional

sys.path.append(str(Path(__file__).parent.parent.parent))

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.schema import Document

from rag.config import (
    CHROMA_DIR, COLLECTION_NAME, EMBEDDING_MODEL,
    TOP_K_RESULTS, QA_PROMPT_TEMPLATE, OPENAI_API_KEY
)


class MBTIQueryEngine:
    """Query engine for MBTI documentation"""

    def __init__(self, use_llm: bool = True):
        """
        Initialize query engine

        Args:
            use_llm: Whether to use LLM for answer generation
                    If False, only returns retrieved documents
        """
        print("🔍 Инициализация поискового движка...")

        # Load embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )

        # Load vector store
        self.vectorstore = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=self.embeddings,
            persist_directory=str(CHROMA_DIR)
        )

        self.use_llm = use_llm
        self.llm = None
        self.qa_chain = None

        if use_llm and OPENAI_API_KEY:
            print("  🤖 Инициализация LLM...")
            self.llm = ChatOpenAI(
                temperature=0,
                model_name="gpt-3.5-turbo",
                openai_api_key=OPENAI_API_KEY
            )

            # Create QA chain
            prompt = PromptTemplate(
                template=QA_PROMPT_TEMPLATE,
                input_variables=["context", "question"]
            )

            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vectorstore.as_retriever(
                    search_kwargs={"k": TOP_K_RESULTS}
                ),
                return_source_documents=True,
                chain_type_kwargs={"prompt": prompt}
            )

        print("✅ Движок готов к работе")

    def search(self, query: str, k: int = TOP_K_RESULTS) -> List[Document]:
        """
        Search for relevant documents

        Args:
            query: Search query
            k: Number of results to return

        Returns:
            List of relevant documents
        """
        results = self.vectorstore.similarity_search(query, k=k)
        return results

    def search_with_score(self, query: str, k: int = TOP_K_RESULTS) -> List[tuple]:
        """
        Search with similarity scores

        Args:
            query: Search query
            k: Number of results

        Returns:
            List of (document, score) tuples
        """
        results = self.vectorstore.similarity_search_with_score(query, k=k)
        return results

    def ask(self, question: str) -> Dict:
        """
        Ask a question and get an answer

        Args:
            question: Question to ask

        Returns:
            Dictionary with answer and source documents
        """
        if self.use_llm and self.qa_chain:
            # Use LLM for answer generation
            result = self.qa_chain({"query": question})
            return {
                'answer': result['result'],
                'sources': result['source_documents']
            }
        else:
            # Just return relevant documents
            docs = self.search(question)
            return {
                'answer': "LLM не настроен. Показаны найденные документы.",
                'sources': docs
            }

    def format_answer(self, result: Dict) -> str:
        """
        Format answer with sources

        Args:
            result: Result from ask()

        Returns:
            Formatted string
        """
        output = []
        output.append("=" * 60)
        output.append("📝 ОТВЕТ")
        output.append("=" * 60)
        output.append(result['answer'])
        output.append("")

        if result['sources']:
            output.append("=" * 60)
            output.append("📚 ИСТОЧНИКИ")
            output.append("=" * 60)

            for i, doc in enumerate(result['sources'], 1):
                metadata = doc.metadata
                filename = metadata.get('filename', 'Unknown')
                title = metadata.get('title', 'No title')

                output.append(f"\n[{i}] {filename}")
                if title and title != 'No title':
                    output.append(f"    Раздел: {title}")

                # Show snippet
                content = doc.page_content[:200]
                if len(doc.page_content) > 200:
                    content += "..."
                output.append(f"    Фрагмент: {content}")

        output.append("=" * 60)
        return "\n".join(output)

    def get_collection_stats(self) -> Dict:
        """Get statistics about the vector store"""
        collection = self.vectorstore._collection
        count = collection.count()

        return {
            'total_documents': count,
            'collection_name': COLLECTION_NAME,
            'embedding_model': EMBEDDING_MODEL
        }


def main():
    """Test query engine"""
    print("🧪 Тестирование поискового движка\n")

    engine = MBTIQueryEngine(use_llm=False)

    # Show stats
    stats = engine.get_collection_stats()
    print(f"📊 Индексировано документов: {stats['total_documents']}\n")

    # Test queries
    test_queries = [
        "Что такое INTJ?",
        "Какие когнитивные функции у ENFP?",
        "Как взаимодействуют INTJ и ENFP?"
    ]

    for query in test_queries:
        print(f"\n🔍 Поиск: {query}")
        print("-" * 60)

        results = engine.search(query, k=3)

        for i, doc in enumerate(results, 1):
            metadata = doc.metadata
            print(f"\n[{i}] {metadata.get('filename', 'Unknown')}")
            print(f"    {doc.page_content[:150]}...")


if __name__ == "__main__":
    main()
