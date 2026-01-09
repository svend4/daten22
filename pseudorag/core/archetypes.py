"""
Система информационных архетипов (16 типов)
Базовые классы и определения архетипов для PseudoRAG системы
"""

from dataclasses import dataclass
from typing import List, Dict
from enum import Enum


class ArchetypeAxis(Enum):
    """Оси измерения реальности"""
    MATERIALITY = "materiality"  # M/A: Материальное/Абстрактное
    DYNAMICS = "dynamics"        # S/D: Статичное/Динамичное
    SCALE = "scale"              # E/C: Элементарное/Комплексное
    STRUCTURE = "structure"      # O/F: Упорядоченное/Текучее


@dataclass
class Archetype:
    """Информационный архетип"""
    code: str                    # "MSEO"
    name_ru: str                 # "Кристалл"
    name_en: str                 # "Crystal"
    description: str             # Подробное описание

    # Оси (4 бита)
    materiality: str             # "M" или "A"
    dynamics: str                # "S" или "D"
    scale: str                   # "E" или "C"
    structure: str               # "O" или "F"

    # Ключевые слова для поиска
    keywords_ru: List[str]
    keywords_en: List[str]

    # Примеры сущностей этого архетипа
    examples: List[str]

    # Приоритет по умолчанию (1-5)
    default_priority: int = 3


# Определение всех 16 архетипов
ARCHETYPES = [
    # КВАДРАНТ I: МАТЕРИАЛЬНОЕ-СТАТИЧНОЕ (MS)
    Archetype(
        code="MSEO",
        name_ru="Кристалл",
        name_en="Crystal",
        description="Простая физическая структура с четким порядком",
        materiality="M", dynamics="S", scale="E", structure="O",
        keywords_ru=["материал", "элемент", "вещество", "атом", "молекула", "химический элемент"],
        keywords_en=["material", "element", "substance", "atom", "molecule", "chemical element"],
        examples=["Железо", "Золото", "Кремний", "Кристаллы", "Простые молекулы"],
        default_priority=2
    ),

    Archetype(
        code="MSEF",
        name_ru="Песок",
        name_en="Sand",
        description="Простые физические частицы без порядка",
        materiality="M", dynamics="S", scale="E", structure="F",
        keywords_ru=["песок", "порошок", "гранулы", "частицы", "сыпучее"],
        keywords_en=["sand", "powder", "granules", "particles", "bulk material"],
        examples=["Песок", "Пыль", "Зерно", "Порошковые вещества"],
        default_priority=1
    ),

    Archetype(
        code="MSCO",
        name_ru="Здание",
        name_en="Building",
        description="Сложная структура с четкой архитектурой",
        materiality="M", dynamics="S", scale="C", structure="O",
        keywords_ru=["здание", "сооружение", "архитектура", "структура", "конструкция", "объект"],
        keywords_en=["building", "structure", "architecture", "construction", "edifice"],
        examples=["Здания", "Мосты", "Памятники", "Инфраструктура"],
        default_priority=5
    ),

    Archetype(
        code="MSCF",
        name_ru="Лес",
        name_en="Forest",
        description="Сложная природная система, медленно меняющаяся",
        materiality="M", dynamics="S", scale="C", structure="F",
        keywords_ru=["природа", "ландшафт", "экосистема", "среда", "местность", "территория"],
        keywords_en=["nature", "landscape", "ecosystem", "environment", "terrain", "territory"],
        examples=["Леса", "Горы", "Реки", "Природные ландшафты"],
        default_priority=3
    ),

    # КВАДРАНТ II: МАТЕРИАЛЬНОЕ-ДИНАМИЧНОЕ (MD)
    Archetype(
        code="MDEO",
        name_ru="Механизм",
        name_en="Mechanism",
        description="Простое устройство с движущимися частями",
        materiality="M", dynamics="D", scale="E", structure="O",
        keywords_ru=["механизм", "устройство", "инструмент", "деталь", "компонент"],
        keywords_en=["mechanism", "device", "tool", "part", "component"],
        examples=["Рычаг", "Шестерня", "Пружина", "Простые механизмы"],
        default_priority=2
    ),

    Archetype(
        code="MDEF",
        name_ru="Организм",
        name_en="Organism",
        description="Живое существо с органической адаптивностью",
        materiality="M", dynamics="D", scale="E", structure="F",
        keywords_ru=["организм", "существо", "животное", "растение", "жизнь", "биология"],
        keywords_en=["organism", "creature", "animal", "plant", "life", "biology"],
        examples=["Животные", "Растения", "Микроорганизмы", "Люди"],
        default_priority=4
    ),

    Archetype(
        code="MDCO",
        name_ru="Машина",
        name_en="Machine",
        description="Сложная техническая система с алгоритмами работы",
        materiality="M", dynamics="D", scale="C", structure="O",
        keywords_ru=["машина", "техника", "система", "оборудование", "транспорт", "устройство"],
        keywords_en=["machine", "equipment", "system", "apparatus", "transport", "device"],
        examples=["Автомобили", "Самолеты", "Роботы", "Фабрики"],
        default_priority=5
    ),

    Archetype(
        code="MDCF",
        name_ru="Город",
        name_en="City",
        description="Сложная живая система с органическим развитием",
        materiality="M", dynamics="D", scale="C", structure="F",
        keywords_ru=["город", "система", "динамика", "поток", "процесс", "изменение"],
        keywords_en=["city", "system", "dynamics", "flow", "process", "change"],
        examples=["Города", "Муравейники", "Океанические течения"],
        default_priority=5
    ),

    # КВАДРАНТ III: АБСТРАКТНОЕ-СТАТИЧНОЕ (AS)
    Archetype(
        code="ASEO",
        name_ru="Аксиома",
        name_en="Axiom",
        description="Фундаментальная истина, неизменный факт",
        materiality="A", dynamics="S", scale="E", structure="O",
        keywords_ru=["факт", "данные", "статистика", "число", "константа", "показатель"],
        keywords_en=["fact", "data", "statistics", "number", "constant", "indicator"],
        examples=["Математические константы", "Физические законы", "Статистика"],
        default_priority=4
    ),

    Archetype(
        code="ASEF",
        name_ru="Архетип",
        name_en="Archetype",
        description="Базовый паттерн без четких границ",
        materiality="A", dynamics="S", scale="E", structure="F",
        keywords_ru=["символ", "образ", "паттерн", "эмоция", "ощущение", "смысл"],
        keywords_en=["symbol", "image", "pattern", "emotion", "feeling", "meaning"],
        examples=["Эмоции", "Архетипы Юнга", "Символы", "Цвета"],
        default_priority=3
    ),

    Archetype(
        code="ASCO",
        name_ru="Теория",
        name_en="Theory",
        description="Структурированная система знаний",
        materiality="A", dynamics="S", scale="C", structure="O",
        keywords_ru=["теория", "наука", "концепция", "модель", "система знаний", "учение"],
        keywords_en=["theory", "science", "concept", "model", "knowledge system", "doctrine"],
        examples=["Научные теории", "Философские учения", "Математические системы"],
        default_priority=3
    ),

    Archetype(
        code="ASCF",
        name_ru="Культура",
        name_en="Culture",
        description="Сложная система ценностей и традиций",
        materiality="A", dynamics="S", scale="C", structure="F",
        keywords_ru=["культура", "традиция", "искусство", "религия", "обычай", "ценность"],
        keywords_en=["culture", "tradition", "art", "religion", "custom", "value"],
        examples=["Культура народов", "Религии", "Мифология", "Искусство"],
        default_priority=5
    ),

    # КВАДРАНТ IV: АБСТРАКТНОЕ-ДИНАМИЧНОЕ (AD)
    Archetype(
        code="ADEO",
        name_ru="Алгоритм",
        name_en="Algorithm",
        description="Пошаговая процедура с детерминированным выполнением",
        materiality="A", dynamics="D", scale="E", structure="O",
        keywords_ru=["алгоритм", "процедура", "метод", "правило", "протокол", "инструкция"],
        keywords_en=["algorithm", "procedure", "method", "rule", "protocol", "instruction"],
        examples=["Алгоритмы", "Рецепты", "Процедуры", "Протоколы"],
        default_priority=2
    ),

    Archetype(
        code="ADEF",
        name_ru="Интуиция",
        name_en="Intuition",
        description="Спонтанный мыслительный процесс",
        materiality="A", dynamics="D", scale="E", structure="F",
        keywords_ru=["мысль", "идея", "интуиция", "вдохновение", "творчество", "озарение"],
        keywords_en=["thought", "idea", "intuition", "inspiration", "creativity", "insight"],
        examples=["Идеи", "Мысли", "Импровизация", "Инсайты"],
        default_priority=2
    ),

    Archetype(
        code="ADCO",
        name_ru="Программа",
        name_en="Program",
        description="Сложная система алгоритмов",
        materiality="A", dynamics="D", scale="C", structure="O",
        keywords_ru=["программа", "план", "проект", "стратегия", "система", "разработка"],
        keywords_en=["program", "plan", "project", "strategy", "system", "development"],
        examples=["Программное обеспечение", "Планы развития", "Проекты"],
        default_priority=3
    ),

    Archetype(
        code="ADCF",
        name_ru="Общество",
        name_en="Society",
        description="Сложная социальная динамика",
        materiality="A", dynamics="D", scale="C", structure="F",
        keywords_ru=["общество", "социум", "экономика", "политика", "рынок", "сообщество"],
        keywords_en=["society", "community", "economy", "politics", "market", "social"],
        examples=["Общество", "Экономика", "Политические процессы", "Социальные движения"],
        default_priority=5
    ),
]


# Индекс архетипов по коду
ARCHETYPE_INDEX: Dict[str, Archetype] = {
    arch.code: arch for arch in ARCHETYPES
}


def get_archetype(code: str) -> Archetype:
    """Получить архетип по коду"""
    return ARCHETYPE_INDEX.get(code)


def get_all_codes() -> List[str]:
    """Получить все коды архетипов"""
    return list(ARCHETYPE_INDEX.keys())


def filter_by_priority(min_priority: int = 3) -> List[Archetype]:
    """Фильтровать архетипы по приоритету"""
    return [arch for arch in ARCHETYPES if arch.default_priority >= min_priority]


def get_quadrant(archetype: Archetype) -> str:
    """Определить квадрант архетипа"""
    mat = archetype.materiality
    dyn = archetype.dynamics

    if mat == "M" and dyn == "S":
        return "MS - Материальное-Статичное"
    elif mat == "M" and dyn == "D":
        return "MD - Материальное-Динамичное"
    elif mat == "A" and dyn == "S":
        return "AS - Абстрактное-Статичное"
    else:  # mat == "A" and dyn == "D"
        return "AD - Абстрактное-Динамичное"


if __name__ == "__main__":
    # Тестирование
    print("=== СИСТЕМА ИНФОРМАЦИОННЫХ АРХЕТИПОВ ===\n")

    for arch in ARCHETYPES:
        print(f"{arch.code} - {arch.name_ru} ({arch.name_en})")
        print(f"  Квадрант: {get_quadrant(arch)}")
        print(f"  Приоритет: {'★' * arch.default_priority}")
        print(f"  Примеры: {', '.join(arch.examples[:3])}")
        print()

    print(f"\nВсего архетипов: {len(ARCHETYPES)}")
    print(f"Высокоприоритетных (≥3): {len(filter_by_priority(3))}")
