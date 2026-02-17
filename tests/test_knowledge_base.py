"""Tests for the knowledge base module."""

import os
import pytest
from app.knowledge_base import KnowledgeBase


@pytest.fixture
def kb():
    """Create a KnowledgeBase instance for Awajún."""
    return KnowledgeBase("awajun")


def test_load_dictionary(kb):
    """Dictionary data loads correctly."""
    assert kb.dictionary is not None
    assert "categories" in kb.dictionary
    assert len(kb.dictionary["categories"]) > 0


def test_load_grammar(kb):
    """Grammar data loads correctly."""
    assert kb.grammar is not None
    assert "word_order" in kb.grammar


def test_load_phrases(kb):
    """Phrases data loads correctly."""
    assert kb.phrases is not None
    assert "classroom_phrases" in kb.phrases


def test_search_dictionary_spanish(kb):
    """Search dictionary with Spanish term."""
    result = kb.search_dictionary("madre")
    assert "dukug" in result


def test_search_dictionary_awajun(kb):
    """Search dictionary with Awajún term."""
    result = kb.search_dictionary("yumi")
    assert "agua" in result


def test_search_dictionary_no_results(kb):
    """Search with non-existent term returns message."""
    result = kb.search_dictionary("xyznonexistent")
    assert "No se encontraron" in result


def test_get_category_vocabulary(kb):
    """Get vocabulary for a category."""
    result = kb.get_category_vocabulary("numeros")
    assert "makichik" in result
    assert "uno" in result


def test_get_category_vocabulary_invalid(kb):
    """Invalid category returns message with available categories."""
    result = kb.get_category_vocabulary("invalid_category")
    assert "no encontrada" in result


def test_get_all_vocabulary_context(kb):
    """Get all vocabulary formatted for LLM context."""
    result = kb.get_all_vocabulary_context()
    assert len(result) > 100
    assert "=" in result


def test_get_grammar_context(kb):
    """Get grammar rules formatted for LLM context."""
    result = kb.get_grammar_context()
    assert "SOV" in result
    assert "CONJUGACIÓN" in result


def test_get_classroom_phrases(kb):
    """Get classroom phrases."""
    phrases = kb.get_classroom_phrases()
    assert len(phrases) > 0
    assert "spanish" in phrases[0]
    assert "awajun" in phrases[0]


def test_get_cultural_expressions(kb):
    """Get cultural expressions with notes."""
    expressions = kb.get_cultural_expressions()
    assert len(expressions) > 0
    assert "cultural_note" in expressions[0]


def test_get_available_categories(kb):
    """List available categories."""
    categories = kb.get_available_categories()
    assert "saludos" in categories
    assert "numeros" in categories
    assert "familia" in categories
