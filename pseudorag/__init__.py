"""
PseudoRAG - Иерархическая система структурирования знаний
Прототип системы для превращения простых запросов в структурированные базы знаний
"""

__version__ = "0.1.0"
__author__ = "PseudoRAG Project"

from .core.archetypes import ARCHETYPES, Archetype, get_archetype
from .core.query_expander import QueryExpander, QuestionTree, Question

__all__ = [
    'ARCHETYPES',
    'Archetype',
    'get_archetype',
    'QueryExpander',
    'QuestionTree',
    'Question',
]
