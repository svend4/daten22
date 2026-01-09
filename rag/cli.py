#!/usr/bin/env python3
"""
CLI Interface for MBTI RAG System
"""
import sys
import argparse
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from rag.scripts.query_engine import MBTIQueryEngine


def main():
    parser = argparse.ArgumentParser(
        description="MBTI Documentation RAG System - Поиск по документации типов личности"
    )
    parser.add_argument(
        'query',
        nargs='?',
        help='Вопрос для поиска (если не указан, запускается интерактивный режим)'
    )
    parser.add_argument(
        '-k', '--top-k',
        type=int,
        default=5,
        help='Количество результатов поиска (по умолчанию: 5)'
    )
    parser.add_argument(
        '--no-llm',
        action='store_true',
        help='Показать только найденные документы без генерации ответа'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Показать статистику индексированных документов'
    )

    args = parser.parse_args()

    # Initialize engine
    use_llm = not args.no_llm
    engine = MBTIQueryEngine(use_llm=use_llm)

    # Show stats if requested
    if args.stats:
        stats = engine.get_collection_stats()
        print("\n📊 СТАТИСТИКА")
        print("=" * 60)
        print(f"Индексировано документов: {stats['total_documents']}")
        print(f"Коллекция: {stats['collection_name']}")
        print(f"Embedding модель: {stats['embedding_model']}")
        print("=" * 60)
        return

    # Single query mode
    if args.query:
        print(f"\n🔍 Поиск: {args.query}\n")

        if use_llm:
            result = engine.ask(args.query)
            print(engine.format_answer(result))
        else:
            docs = engine.search(args.query, k=args.top_k)
            print("=" * 60)
            print(f"📚 НАЙДЕНО {len(docs)} ДОКУМЕНТОВ")
            print("=" * 60)

            for i, doc in enumerate(docs, 1):
                metadata = doc.metadata
                print(f"\n[{i}] {metadata.get('filename', 'Unknown')}")
                if metadata.get('title'):
                    print(f"    Раздел: {metadata['title']}")
                print(f"    Фрагмент: {doc.page_content[:200]}...")
                print()

        return

    # Interactive mode
    print("\n" + "=" * 60)
    print("🧠 MBTI RAG SYSTEM - Интерактивный режим")
    print("=" * 60)
    print("\nВведите вопрос о типах личности MBTI")
    print("Команды: 'exit' или 'quit' для выхода, 'stats' для статистики\n")

    while True:
        try:
            query = input("💬 Вопрос: ").strip()

            if not query:
                continue

            if query.lower() in ['exit', 'quit', 'выход']:
                print("\n👋 До свидания!")
                break

            if query.lower() in ['stats', 'статистика']:
                stats = engine.get_collection_stats()
                print(f"\n📊 Индексировано: {stats['total_documents']} документов")
                print(f"    Модель: {stats['embedding_model']}\n")
                continue

            if use_llm:
                result = engine.ask(query)
                print()
                print(engine.format_answer(result))
            else:
                docs = engine.search(query, k=args.top_k)
                print(f"\n📚 Найдено {len(docs)} документов:\n")
                for i, doc in enumerate(docs, 1):
                    metadata = doc.metadata
                    print(f"[{i}] {metadata.get('filename', 'Unknown')}")
                    print(f"    {doc.page_content[:150]}...\n")

            print()

        except KeyboardInterrupt:
            print("\n\n👋 До свидания!")
            break
        except Exception as e:
            print(f"\n❌ Ошибка: {e}\n")


if __name__ == "__main__":
    main()
