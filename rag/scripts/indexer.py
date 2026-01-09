"""
Document Indexer for MBTI RAG System
Loads, chunks, and indexes all documentation into ChromaDB
"""
import sys
from pathlib import Path
from typing import List
from tqdm import tqdm

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

from rag.config import (
    DOCS_DIR, TYPES_DIR, CHROMA_DIR, COLLECTION_NAME,
    CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL
)


class MBTIDocumentIndexer:
    """Indexes MBTI documentation into vector database"""

    def __init__(self):
        print("🚀 Инициализация индексатора MBTI документации...")

        # Initialize embeddings
        print(f"📦 Загрузка embedding модели: {EMBEDDING_MODEL}")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )

        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

        self.documents = []
        self.chunks = []

    def load_documents(self) -> List[Document]:
        """Load all markdown documents from docs and types directories"""
        print("\n📚 Загрузка документов...")

        all_docs = []

        # Load from docs directory
        if DOCS_DIR.exists():
            print(f"  📁 Загрузка из {DOCS_DIR}")
            loader = DirectoryLoader(
                str(DOCS_DIR),
                glob="**/*.md",
                loader_cls=TextLoader,
                loader_kwargs={'encoding': 'utf-8'}
            )
            docs = loader.load()
            print(f"    ✓ Загружено {len(docs)} документов")
            all_docs.extend(docs)

        # Load from types directory
        if TYPES_DIR.exists():
            print(f"  📁 Загрузка из {TYPES_DIR}")
            loader = DirectoryLoader(
                str(TYPES_DIR),
                glob="**/*.md",
                loader_cls=TextLoader,
                loader_kwargs={'encoding': 'utf-8'}
            )
            docs = loader.load()
            print(f"    ✓ Загружено {len(docs)} документов")
            all_docs.extend(docs)

        # Add metadata
        for doc in all_docs:
            file_path = Path(doc.metadata['source'])
            doc.metadata['filename'] = file_path.name
            doc.metadata['directory'] = file_path.parent.name

            # Extract title from first line if it's a header
            lines = doc.page_content.split('\n')
            if lines and lines[0].startswith('#'):
                doc.metadata['title'] = lines[0].strip('#').strip()

        self.documents = all_docs
        print(f"\n✅ Всего загружено: {len(all_docs)} документов")
        return all_docs

    def chunk_documents(self) -> List[Document]:
        """Split documents into chunks"""
        print("\n🔪 Разбиение документов на фрагменты...")

        chunks = []
        for doc in tqdm(self.documents, desc="Chunking"):
            doc_chunks = self.text_splitter.split_documents([doc])
            chunks.extend(doc_chunks)

        self.chunks = chunks
        print(f"✅ Создано {len(chunks)} фрагментов")
        return chunks

    def create_vectorstore(self) -> Chroma:
        """Create and populate vector store"""
        print("\n🔍 Создание векторной базы данных...")
        print(f"  📍 Локация: {CHROMA_DIR}")
        print(f"  📦 Коллекция: {COLLECTION_NAME}")

        # Create vector store
        vectorstore = Chroma.from_documents(
            documents=self.chunks,
            embedding=self.embeddings,
            collection_name=COLLECTION_NAME,
            persist_directory=str(CHROMA_DIR)
        )

        print("✅ Векторная база создана и сохранена")
        return vectorstore

    def index_all(self):
        """Complete indexing pipeline"""
        print("=" * 60)
        print("🎯 ИНДЕКСАЦИЯ ДОКУМЕНТАЦИИ MBTI")
        print("=" * 60)

        # Load documents
        self.load_documents()

        if not self.documents:
            print("❌ Документы не найдены!")
            return

        # Chunk documents
        self.chunk_documents()

        # Create vector store
        vectorstore = self.create_vectorstore()

        # Print statistics
        print("\n" + "=" * 60)
        print("📊 СТАТИСТИКА ИНДЕКСАЦИИ")
        print("=" * 60)
        print(f"Документов: {len(self.documents)}")
        print(f"Фрагментов: {len(self.chunks)}")
        print(f"Размер чанка: {CHUNK_SIZE} символов")
        print(f"Перекрытие: {CHUNK_OVERLAP} символов")
        print(f"Embedding модель: {EMBEDDING_MODEL}")
        print(f"Векторная БД: {CHROMA_DIR}")
        print("=" * 60)
        print("\n✨ Индексация завершена успешно!")

        return vectorstore

    def get_stats(self) -> dict:
        """Get indexing statistics"""
        return {
            'total_documents': len(self.documents),
            'total_chunks': len(self.chunks),
            'chunk_size': CHUNK_SIZE,
            'chunk_overlap': CHUNK_OVERLAP,
            'embedding_model': EMBEDDING_MODEL
        }


def main():
    """Main indexing function"""
    indexer = MBTIDocumentIndexer()
    indexer.index_all()


if __name__ == "__main__":
    main()
