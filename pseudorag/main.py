#!/usr/bin/env python3
"""
PseudoRAG - Главный скрипт
Демонстрация работы системы расширения запросов
"""

import sys
from pathlib import Path

# Добавляем путь к модулю
sys.path.insert(0, str(Path(__file__).parent.parent))

from pseudorag.core.query_expander import QueryExpander
from pseudorag.core.archetypes import ARCHETYPES


def print_header(text: str):
    """Красивый заголовок"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def demo_archetypes():
    """Демонстрация системы архетипов"""
    print_header("СИСТЕМА ИНФОРМАЦИОННЫХ АРХЕТИПОВ")

    print("Всего архетипов: 16\n")
    print("Квадранты:\n")

    quadrants = {
        'MS': [],
        'MD': [],
        'AS': [],
        'AD': []
    }

    for arch in ARCHETYPES:
        quadrant = arch.materiality + arch.dynamics
        quadrants[quadrant].append(arch)

    quadrant_names = {
        'MS': 'Материальное-Статичное',
        'MD': 'Материальное-Динамичное',
        'AS': 'Абстрактное-Статичное',
        'AD': 'Абстрактное-Динамичное'
    }

    for quad_code, quad_name in quadrant_names.items():
        print(f"📦 {quad_name} ({quad_code}):")
        for arch in quadrants[quad_code]:
            priority_stars = "★" * arch.default_priority
            print(f"   {arch.code} - {arch.name_ru:15} ({arch.name_en:15}) {priority_stars}")
        print()


def demo_query_expansion():
    """Демонстрация расширения запросов"""
    print_header("ДЕМОНСТРАЦИЯ РАСШИРЕНИЯ ЗАПРОСОВ")

    expander = QueryExpander()

    test_queries = [
        ("Города Европы", 0.4),
        ("Транспортные системы", 0.35),
        ("Животные Африки", 0.3),
    ]

    results = []

    for query, min_rel in test_queries:
        print(f"\n{'─'*70}")
        print(f"ЗАПРОС: '{query}'")
        print(f"{'─'*70}\n")

        tree = expander.expand_query(query, depth=1, min_relevance=min_rel)

        # Сохранение результатов
        safe_name = query.lower().replace(" ", "_")
        examples_dir = Path(__file__).parent / "examples"
        examples_dir.mkdir(exist_ok=True)

        json_path = examples_dir / f"{safe_name}.json"
        md_path = examples_dir / f"{safe_name}.md"

        tree.to_json(str(json_path))
        tree.to_markdown(str(md_path))

        print(f"\n✅ Результаты сохранены:")
        print(f"   📄 {json_path}")
        print(f"   📝 {md_path}\n")

        results.append({
            'query': query,
            'questions': len(tree.questions),
            'archetypes': tree.metadata['archetypes_used']
        })

    # Итоговая статистика
    print_header("ИТОГОВАЯ СТАТИСТИКА")

    print("Результаты расширения:\n")
    for res in results:
        print(f"📌 {res['query']}")
        print(f"   Вопросов: {res['questions']}")
        print(f"   Архетипов: {res['archetypes']}/16")
        print()

    total_questions = sum(r['questions'] for r in results)
    print(f"💡 Всего сгенерировано вопросов: {total_questions}")


def demo_questionnaire_structure():
    """Демонстрация структуры вопросника"""
    print_header("СТРУКТУРА ВОПРОСНИКА")

    expander = QueryExpander()
    tree = expander.expand_query("Города Европы", depth=1, min_relevance=0.4)

    # Группировка по архетипам
    by_archetype = {}
    for q in tree.questions:
        if q.archetype_code not in by_archetype:
            by_archetype[q.archetype_code] = []
        by_archetype[q.archetype_code].append(q)

    print(f"Тема: {tree.topic}")
    print(f"Всего вопросов: {len(tree.questions)}\n")

    print("Распределение по архетипам:\n")
    for arch in ARCHETYPES:
        if arch.code in by_archetype:
            questions = by_archetype[arch.code]
            bar = "█" * len(questions)
            print(f"{arch.code} ({arch.name_ru:12}): {len(questions):2} {bar}")

    print("\n" + "─"*70)
    print("Примеры вопросов:\n")

    # Показываем по 2 вопроса из каждого архетипа
    for arch in ARCHETYPES:
        if arch.code in by_archetype:
            questions = by_archetype[arch.code][:2]
            print(f"📂 {arch.name_ru} ({arch.code}):")
            for q in questions:
                print(f"   ❓ {q.text}")
            print()


def main():
    """Главная функция"""
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  PSEUDORAG - ИЕРАРХИЧЕСКАЯ СИСТЕМА СТРУКТУРИРОВАНИЯ ЗНАНИЙ".center(68) + "█")
    print("█" + "  Прототип v0.1.0".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)

    # Демонстрации
    demo_archetypes()

    input("\n⏎ Нажмите Enter для продолжения...")

    demo_query_expansion()

    input("\n⏎ Нажмите Enter для продолжения...")

    demo_questionnaire_structure()

    print_header("ЗАВЕРШЕНО")
    print("✨ Демонстрация завершена!")
    print("📁 Результаты сохранены в папке examples/\n")


if __name__ == "__main__":
    main()
