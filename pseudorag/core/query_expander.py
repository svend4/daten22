"""
Модуль расширения запросов (Query Expansion)
Превращает простой вопрос в структурированный вопросник по 16 архетипам
"""

import json
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from .archetypes import ARCHETYPES, Archetype, get_archetype


@dataclass
class Question:
    """Вопрос в вопроснике"""
    id: str                           # "1.3.2" (иерархический номер)
    text: str                         # Текст вопроса
    archetype_code: str               # "MSCO"
    priority: int                     # 1-5
    keywords: List[str]               # Ключевые слова
    expected_answer_type: str         # "list", "number", "text", "boolean"
    parent_id: Optional[str] = None   # ID родительского вопроса
    depth: int = 1                    # Глубина в дереве


@dataclass
class QuestionTree:
    """Дерево вопросов"""
    topic: str                        # "Города Европы"
    root_question: str                # Исходный вопрос
    questions: List[Question]         # Все вопросы
    metadata: Dict                    # Метаданные

    def to_json(self, filepath: str):
        """Сохранить в JSON"""
        data = {
            'topic': self.topic,
            'root_question': self.root_question,
            'questions': [asdict(q) for q in self.questions],
            'metadata': self.metadata
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def to_markdown(self, filepath: str):
        """Экспортировать в Markdown"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# Вопросник: {self.topic}\n\n")
            f.write(f"**Исходный запрос:** {self.root_question}\n\n")
            f.write(f"**Всего вопросов:** {len(self.questions)}\n\n")
            f.write("---\n\n")

            # Группировка по архетипам
            by_archetype = {}
            for q in self.questions:
                if q.archetype_code not in by_archetype:
                    by_archetype[q.archetype_code] = []
                by_archetype[q.archetype_code].append(q)

            # Вывод по секциям
            for arch in ARCHETYPES:
                if arch.code in by_archetype:
                    questions = by_archetype[arch.code]
                    f.write(f"## {arch.code} - {arch.name_ru} ({len(questions)} вопросов)\n\n")

                    for q in questions:
                        indent = "  " * (q.depth - 1)
                        f.write(f"{indent}**{q.id}.** {q.text}\n")
                        f.write(f"{indent}  *Тип ответа: {q.expected_answer_type}*\n\n")

                    f.write("\n")


class QueryExpander:
    """Расширитель запросов"""

    # Шаблоны вопросов для каждого архетипа
    QUESTION_TEMPLATES = {
        "MSEO": [
            "Какие базовые материалы используются в {topic}?",
            "Из каких элементов состоит {topic}?",
            "Какие физические свойства важны для {topic}?"
        ],
        "MSEF": [
            "Какие сыпучие или неупорядоченные материалы присутствуют в {topic}?",
            "Какие гранулированные вещества связаны с {topic}?"
        ],
        "MSCO": [
            "Какие сооружения и структуры составляют {topic}?",
            "Какая архитектура характерна для {topic}?",
            "Какие типы зданий встречаются в {topic}?",
            "Какие исторические архитектурные стили представлены?",
            "Какие современные архитектурные решения используются?",
            "Какие знаковые здания и памятники есть?"
        ],
        "MSCF": [
            "Какая природная среда окружает {topic}?",
            "Как ландшафт интегрирован в {topic}?",
            "Какие экосистемы связаны с {topic}?",
            "Какие природные особенности характерны?"
        ],
        "MDEO": [
            "Какие базовые механизмы обеспечивают работу {topic}?",
            "Какие инфраструктурные элементы необходимы для {topic}?",
            "Какие простые устройства используются?"
        ],
        "MDEF": [
            "Кто населяет или использует {topic}?",
            "Какие живые существа связаны с {topic}?",
            "Какая демография характерна для {topic}?",
            "Какой этнический и культурный состав?"
        ],
        "MDCO": [
            "Какие технические системы функционируют в {topic}?",
            "Какой транспорт используется в {topic}?",
            "Какие машины и оборудование присутствуют?",
            "Какие транспортные системы развиты?",
            "Какая техническая инфраструктура существует?"
        ],
        "MDCF": [
            "Как {topic} функционирует как сложная система?",
            "Какова динамика и потоки в {topic}?",
            "Как организованы части {topic}?",
            "Какие процессы происходят в системе?",
            "Как части взаимодействуют между собой?"
        ],
        "ASEO": [
            "Какие ключевые показатели характеризуют {topic}?",
            "Какие статистические данные доступны по {topic}?",
            "Какие константы и факты определяют {topic}?",
            "Какие числовые характеристики важны?",
            "Какие измеримые параметры существуют?"
        ],
        "ASEF": [
            "Какие символы и образы ассоциируются с {topic}?",
            "Какие эмоции и ощущения вызывает {topic}?",
            "Какая символика связана с {topic}?",
            "Какие культурные архетипы проявляются?"
        ],
        "ASCO": [
            "Какие теории применимы к {topic}?",
            "Какие научные концепции объясняют {topic}?",
            "Какие модели описывают {topic}?",
            "Какие теоретические основы существуют?"
        ],
        "ASCF": [
            "Какая культура характерна для {topic}?",
            "Какие традиции связаны с {topic}?",
            "Какое искусство представлено в {topic}?",
            "Какая культурная жизнь развита?",
            "Какие традиции и обычаи существуют?",
            "Какие культурные особенности проявляются?"
        ],
        "ADEO": [
            "Какие процедуры и алгоритмы используются в {topic}?",
            "Как планируется и управляется {topic}?",
            "Какие процессы протекают в {topic}?",
            "Какие методы управления применяются?"
        ],
        "ADEF": [
            "Какая атмосфера характерна для {topic}?",
            "Каков 'дух' или идентичность {topic}?",
            "Какие неосязаемые качества определяют {topic}?",
            "Какое общее впечатление производит?"
        ],
        "ADCO": [
            "Какие программные системы используются в {topic}?",
            "Какова цифровизация {topic}?",
            "Какие алгоритмические системы управляют {topic}?",
            "Какие IT-системы развиты?",
            "Какие цифровые решения применяются?"
        ],
        "ADCF": [
            "Какие социальные процессы происходят в {topic}?",
            "Какова социальная динамика {topic}?",
            "Как общество организовано в {topic}?",
            "Какие экономические процессы происходят?",
            "Какая политическая ситуация?",
            "Какие социальные явления наблюдаются?"
        ]
    }

    def __init__(self):
        self.questions = []
        self.question_counter = 0

    def parse_topic(self, query: str) -> Dict:
        """Парсинг темы запроса"""
        # Простой парсинг (в реальной системе - NLP)
        entities = self._extract_entities(query)

        return {
            'query': query,
            'entities': entities,
            'domain': self._classify_domain(query),
            'language': self._detect_language(query)
        }

    def _extract_entities(self, text: str) -> List[str]:
        """Извлечение сущностей (упрощенно)"""
        # В реальной системе - spaCy или другой NER
        words = re.findall(r'\b[А-ЯЁA-Z][а-яёa-z]+\b', text)
        return words

    def _classify_domain(self, query: str) -> str:
        """Классификация домена"""
        # Упрощенная классификация
        domains = {
            'урбанистика': ['город', 'горо', 'столиц', 'мегаполис'],
            'биология': ['животн', 'растен', 'организм', 'вид'],
            'техника': ['машин', 'транспорт', 'устройств'],
            'география': ['стран', 'территор', 'регион', 'континент'],
            'культура': ['искусств', 'культур', 'традиц']
        }

        query_lower = query.lower()
        for domain, keywords in domains.items():
            if any(kw in query_lower for kw in keywords):
                return domain

        return 'общее'

    def _detect_language(self, text: str) -> str:
        """Определение языка"""
        if re.search(r'[а-яёА-ЯЁ]', text):
            return 'ru'
        return 'en'

    def calculate_archetype_relevance(self, archetype: Archetype, topic_data: Dict) -> float:
        """Вычисление релевантности архетипа для темы"""
        # Упрощенная оценка (в реальной системе - ML модель)
        domain = topic_data['domain']
        query = topic_data['query'].lower()

        # Базовая релевантность = приоритет архетипа
        relevance = archetype.default_priority / 5.0

        # Бонус за совпадение ключевых слов
        keywords = archetype.keywords_ru if topic_data['language'] == 'ru' else archetype.keywords_en
        keyword_matches = sum(1 for kw in keywords if kw.lower() in query)
        relevance += keyword_matches * 0.1

        # Бонус по домену
        domain_bonus = {
            'урбанистика': {
                'MSCO': 0.3, 'MDCO': 0.3, 'MDCF': 0.3, 'ASCF': 0.2,
                'ADCF': 0.3, 'ASEO': 0.2, 'MDEF': 0.2
            },
            'биология': {
                'MDEF': 0.4, 'MSCF': 0.3, 'ASEO': 0.2, 'ASCO': 0.2
            },
            'техника': {
                'MDCO': 0.4, 'MDEO': 0.3, 'ADCO': 0.3, 'ASEO': 0.2
            }
        }.get(domain, {})

        relevance += domain_bonus.get(archetype.code, 0)

        return min(relevance, 1.0)

    def generate_base_questions(self, topic: str, archetype: Archetype) -> List[Question]:
        """Генерация базовых вопросов для архетипа"""
        templates = self.QUESTION_TEMPLATES.get(archetype.code, [])
        questions = []

        for i, template in enumerate(templates, 1):
            self.question_counter += 1
            question_text = template.format(topic=topic)

            # Определение типа ожидаемого ответа
            if "какие" in question_text.lower() or "какой" in question_text.lower():
                answer_type = "list"
            elif "сколько" in question_text.lower() or "количество" in question_text.lower():
                answer_type = "number"
            elif "как" in question_text.lower():
                answer_type = "text"
            else:
                answer_type = "text"

            question = Question(
                id=f"{archetype.code}.{i}",
                text=question_text,
                archetype_code=archetype.code,
                priority=archetype.default_priority,
                keywords=archetype.keywords_ru,
                expected_answer_type=answer_type,
                depth=1
            )
            questions.append(question)

        return questions

    def expand_query(self, query: str, depth: int = 1, min_relevance: float = 0.3) -> QuestionTree:
        """
        Основной метод: расширение запроса в вопросник

        Args:
            query: Исходный запрос
            depth: Глубина декомпозиции (1-3)
            min_relevance: Минимальная релевантность архетипа

        Returns:
            QuestionTree с вопросами
        """
        print(f"🔍 Расширение запроса: '{query}'")
        print(f"   Глубина: {depth}, Мин. релевантность: {min_relevance}\n")

        # Парсинг темы
        topic_data = self.parse_topic(query)
        print(f"📊 Домен: {topic_data['domain']}")
        print(f"🌐 Язык: {topic_data['language']}\n")

        # Оценка релевантности архетипов
        archetype_scores = []
        for arch in ARCHETYPES:
            score = self.calculate_archetype_relevance(arch, topic_data)
            archetype_scores.append((arch, score))

        # Сортировка по релевантности
        archetype_scores.sort(key=lambda x: x[1], reverse=True)

        print("📈 Релевантность архетипов:")
        for arch, score in archetype_scores:
            if score >= min_relevance:
                stars = "★" * int(score * 5)
                print(f"   {arch.code} ({arch.name_ru}): {score:.2f} {stars}")

        print()

        # Генерация вопросов
        all_questions = []
        for arch, score in archetype_scores:
            if score >= min_relevance:
                questions = self.generate_base_questions(query, arch)
                all_questions.extend(questions)
                print(f"✅ {arch.code}: сгенерировано {len(questions)} вопросов")

        print(f"\n🎯 Всего сгенерировано вопросов: {len(all_questions)}")

        # Создание дерева вопросов
        tree = QuestionTree(
            topic=query,
            root_question=query,
            questions=all_questions,
            metadata={
                'total_questions': len(all_questions),
                'depth': depth,
                'domain': topic_data['domain'],
                'language': topic_data['language'],
                'archetypes_used': len([s for _, s in archetype_scores if s >= min_relevance])
            }
        )

        return tree


if __name__ == "__main__":
    # Тестирование
    expander = QueryExpander()

    # Пример 1: Города Европы
    print("="*60)
    print("ТЕСТ 1: Города Европы")
    print("="*60 + "\n")

    tree = expander.expand_query("Города Европы", depth=1, min_relevance=0.4)

    # Сохранение результатов
    tree.to_json("examples/cities_questionnaire.json")
    tree.to_markdown("examples/cities_questionnaire.md")

    print(f"\n📁 Результаты сохранены:")
    print(f"   - examples/cities_questionnaire.json")
    print(f"   - examples/cities_questionnaire.md")
