"""
Streamlit Web Interface for MBTI RAG System
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

import streamlit as st
from rag.scripts.query_engine import MBTIQueryEngine

# Page config
st.set_page_config(
    page_title="MBTI RAG System",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1E88E5;
        padding: 20px;
    }
    .source-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .source-title {
        font-weight: bold;
        color: #1565C0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'engine' not in st.session_state:
    with st.spinner("🔧 Инициализация RAG системы..."):
        st.session_state.engine = MBTIQueryEngine(use_llm=False)
    st.success("✅ Система готова!")

if 'history' not in st.session_state:
    st.session_state.history = []

# Header
st.markdown("<h1 class='main-header'>🧠 MBTI Documentation RAG System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Интеллектуальный поиск по документации 16 типов личности</p>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Настройки")

    # Search settings
    top_k = st.slider("Количество результатов", 1, 10, 5)

    st.divider()

    # Statistics
    st.header("📊 Статистика")
    stats = st.session_state.engine.get_collection_stats()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Документов", stats['total_documents'])
    with col2:
        st.metric("Коллекция", stats['collection_name'])

    st.caption(f"Модель: {stats['embedding_model']}")

    st.divider()

    # Quick queries
    st.header("🚀 Быстрые запросы")
    quick_queries = [
        "Что такое INTJ?",
        "Какие когнитивные функции у ENFP?",
        "Совместимость INTJ и ENFP",
        "Что такое соционика?",
        "Подтипы А и Т",
        "Теневые функции",
        "Стили лидерства",
        "Романтические отношения типов"
    ]

    for query in quick_queries:
        if st.button(query, key=f"quick_{query}", use_container_width=True):
            st.session_state.current_query = query

    st.divider()

    # Clear history
    if st.button("🗑️ Очистить историю", use_container_width=True):
        st.session_state.history = []
        st.rerun()

    # About
    st.divider()
    st.header("ℹ️ О системе")
    st.markdown("""
    Эта система использует RAG (Retrieval-Augmented Generation) для
    интеллектуального поиска по документации MBTI.

    **Возможности:**
    - Семантический поиск
    - 42 документа
    - 16 описаний типов
    - Русский язык
    """)

# Main content
tabs = st.tabs(["🔍 Поиск", "📜 История", "📖 Документы"])

# Tab 1: Search
with tabs[0]:
    # Get query from session state or user input
    if 'current_query' in st.session_state:
        query = st.session_state.current_query
        del st.session_state.current_query
    else:
        query = ""

    # Search input
    search_query = st.text_input(
        "Задайте вопрос о типах личности MBTI:",
        value=query,
        placeholder="Например: Какие сильные стороны у INTJ?",
        key="search_input"
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        search_button = st.button("🔍 Найти", type="primary", use_container_width=True)
    with col2:
        example_button = st.button("💡 Пример", use_container_width=True)

    if example_button:
        search_query = "Что такое когнитивные функции в MBTI?"
        st.rerun()

    # Perform search
    if search_button and search_query:
        with st.spinner("🔍 Поиск в документации..."):
            # Search
            docs = st.session_state.engine.search(search_query, k=top_k)

            # Add to history
            st.session_state.history.insert(0, {
                'query': search_query,
                'results': docs
            })

            # Display results
            st.success(f"✅ Найдено {len(docs)} релевантных фрагментов")

            for i, doc in enumerate(docs, 1):
                with st.expander(f"📄 Результат {i}: {doc.metadata.get('filename', 'Unknown')}", expanded=(i==1)):
                    # Metadata
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        if doc.metadata.get('title'):
                            st.markdown(f"**Раздел:** {doc.metadata['title']}")
                    with col2:
                        st.caption(f"Источник: {doc.metadata.get('directory', 'Unknown')}")

                    # Content
                    st.markdown("---")
                    st.markdown(doc.page_content)

# Tab 2: History
with tabs[1]:
    st.header("📜 История поиска")

    if not st.session_state.history:
        st.info("История пуста. Выполните поиск, чтобы увидеть результаты здесь.")
    else:
        for i, entry in enumerate(st.session_state.history):
            with st.expander(f"🔍 {entry['query']}", expanded=(i==0)):
                st.markdown(f"**Найдено результатов:** {len(entry['results'])}")
                st.markdown("---")

                for j, doc in enumerate(entry['results'], 1):
                    st.markdown(f"**[{j}] {doc.metadata.get('filename', 'Unknown')}**")
                    if doc.metadata.get('title'):
                        st.caption(f"Раздел: {doc.metadata['title']}")
                    st.text(doc.page_content[:300] + "...")
                    st.markdown("")

# Tab 3: Documents
with tabs[2]:
    st.header("📖 Индексированные документы")

    # Get unique documents from vector store
    st.info(f"Всего индексировано: {stats['total_documents']} фрагментов из документации")

    st.markdown("""
    ### 📚 Структура документации

    **docs/** (42 документа):
    - 01-09: Основы MBTI
    - 10-12: Углубленная теория (соционика, подтипы, тень)
    - 13-19: Отношения и командная работа
    - 20-42: Специализированные темы

    **types/** (16 документов):
    - Детальные описания всех 16 типов личности
    - INTJ, INTP, ENTJ, ENTP, INFJ, INFP, ENFJ, ENFP
    - ISTJ, ISFJ, ESTJ, ESFJ, ISTP, ISFP, ESTP, ESFP
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    🧠 MBTI RAG System | Powered by LangChain & ChromaDB | 2024
</div>
""", unsafe_allow_html=True)
