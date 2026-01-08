#!/usr/bin/env python3
"""
Тест расширения запроса "Города Европы"
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from pseudorag.core.query_expander import QueryExpander

def test_cities():
    print("="*70)
    print("  ТЕСТ: Расширение запроса 'Города Европы'")
    print("="*70 + "\n")

    expander = QueryExpander()

    # Расширение запроса
    tree = expander.expand_query(
        query="Города Европы",
        depth=1,
        min_relevance=0.4
    )

    # Анализ результатов
    print(f"\n{'─'*70}")
    print("РЕЗУЛЬТАТЫ")
    print(f"{'─'*70}\n")

    print(f"✅ Всего вопросов: {len(tree.questions)}")
    print(f"✅ Использовано архетипов: {tree.metadata['archetypes_used']}/16")
    print(f"✅ Домен: {tree.metadata['domain']}")

    # Группировка по архетипам
    by_archetype = {}
    for q in tree.questions:
        if q.archetype_code not in by_archetype:
            by_archetype[q.archetype_code] = []
        by_archetype[q.archetype_code].append(q)

    print(f"\nРаспределение по архетипам:\n")
    for code, questions in sorted(by_archetype.items()):
        print(f"  {code}: {len(questions)} вопросов")

    # Показываем примеры
    print(f"\n{'─'*70}")
    print("ПРИМЕРЫ ВОПРОСОВ")
    print(f"{'─'*70}\n")

    for code in list(by_archetype.keys())[:5]:  # Первые 5 архетипов
        questions = by_archetype[code]
        print(f"📂 {code}:")
        for q in questions[:2]:  # По 2 вопроса
            print(f"   ❓ {q.text}")
        print()

    # Сохранение
    examples_dir = Path(__file__).parent / "examples"
    examples_dir.mkdir(exist_ok=True)

    json_path = examples_dir / "города_европы.json"
    md_path = examples_dir / "города_европы.md"

    tree.to_json(str(json_path))
    tree.to_markdown(str(md_path))

    print(f"{'─'*70}")
    print("ФАЙЛЫ")
    print(f"{'─'*70}\n")
    print(f"📄 JSON: {json_path}")
    print(f"📝 Markdown: {md_path}\n")

    return tree

if __name__ == "__main__":
    tree = test_cities()
    print("✨ Тест завершён успешно!\n")
