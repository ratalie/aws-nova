"""Translation engine that combines Nova 2 Lite with the knowledge base.

This module orchestrates the translation pipeline:
1. Searches the knowledge base for relevant vocabulary and grammar
2. Builds context-aware prompts with few-shot examples
3. Sends to Nova 2 Lite for translation
4. Returns the result with confidence indicators
"""

from app.nova_lite import NovaLiteClient
from app.knowledge_base import KnowledgeBase
from app.config import SOURCE_LANGUAGE_NAME


class Translator:
    """Orchestrates translation between Spanish and indigenous languages.

    Combines the knowledge base (dictionary, grammar, phrases) with
    Nova 2 Lite's reasoning capabilities to produce translations
    for underrepresented indigenous languages.
    """

    def __init__(self, language_key: str, language_name: str):
        self.nova = NovaLiteClient()
        self.kb = KnowledgeBase(language_key)
        self.language_name = language_name

    def translate_to_indigenous(self, spanish_text: str) -> dict:
        """Translate Spanish text to the indigenous language.

        Args:
            spanish_text: Text in Spanish to translate.

        Returns:
            Dict with translation, context used, and confidence notes.
        """
        dictionary_context = self.kb.get_all_vocabulary_context()
        grammar_context = self.kb.get_grammar_context()
        matching_phrases = self.kb.get_matching_phrases(spanish_text)

        full_dict_context = dictionary_context
        if matching_phrases and "No se encontraron" not in matching_phrases:
            full_dict_context += f"\n\nFRASES SIMILARES CONOCIDAS:\n{matching_phrases}"

        translation = self.nova.translate(
            text=spanish_text,
            source_lang=SOURCE_LANGUAGE_NAME,
            target_lang=self.language_name,
            dictionary_context=full_dict_context,
            grammar_context=grammar_context,
        )

        return {
            "original": spanish_text,
            "translation": translation,
            "source_lang": SOURCE_LANGUAGE_NAME,
            "target_lang": self.language_name,
            "dictionary_matches": self.kb.search_dictionary(spanish_text),
        }

    def translate_to_spanish(self, indigenous_text: str) -> dict:
        """Translate indigenous language text to Spanish.

        Args:
            indigenous_text: Text in the indigenous language.

        Returns:
            Dict with translation and context.
        """
        dictionary_context = self.kb.get_all_vocabulary_context()
        grammar_context = self.kb.get_grammar_context()

        translation = self.nova.translate(
            text=indigenous_text,
            source_lang=self.language_name,
            target_lang=SOURCE_LANGUAGE_NAME,
            dictionary_context=dictionary_context,
            grammar_context=grammar_context,
        )

        return {
            "original": indigenous_text,
            "translation": translation,
            "source_lang": self.language_name,
            "target_lang": SOURCE_LANGUAGE_NAME,
        }

    def generate_lesson(self, topic: str, difficulty: str = "básico") -> str:
        """Generate a bilingual lesson on a given topic.

        Args:
            topic: The lesson topic.
            difficulty: Level (básico, intermedio, avanzado).

        Returns:
            Formatted bilingual lesson content.
        """
        dictionary_context = self.kb.get_all_vocabulary_context()

        return self.nova.generate_lesson(
            topic=topic,
            target_lang=self.language_name,
            difficulty=difficulty,
            dictionary_context=dictionary_context,
        )

    def explain_culture(self, text: str) -> str:
        """Get cultural context for a message.

        Args:
            text: The text to explain culturally.

        Returns:
            Cultural explanation.
        """
        cultural_expressions = self.kb.get_cultural_expressions()
        cultural_notes = "\n".join(
            f"- {expr.get('spanish', '')}: {expr.get('cultural_note', '')}"
            for expr in cultural_expressions
            if expr.get("cultural_note")
        )

        return self.nova.explain_cultural_context(
            text=text,
            language=self.language_name,
            cultural_notes=cultural_notes,
        )

    def get_phrase_book(self, category: str = "classroom") -> list[dict]:
        """Get pre-built phrases for quick reference.

        Args:
            category: 'classroom', 'daily', or 'cultural'.

        Returns:
            List of phrase dicts.
        """
        mapping = {
            "classroom": "classroom_phrases",
            "daily": "daily_interaction",
            "cultural": "cultural_expressions",
        }
        section_key = mapping.get(category, "classroom_phrases")
        return self.kb.phrases.get(section_key, [])
