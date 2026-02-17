"""Knowledge base for indigenous language data.

Loads and queries the linguistic data (dictionary, grammar, phrases)
for each supported indigenous language. Provides context to Nova 2 Lite
for more accurate translations and educational content.
"""

import json
import os
from typing import Optional


class KnowledgeBase:
    """Manages linguistic data for indigenous languages.

    Loads dictionary, grammar rules, and common phrases from JSON files
    and provides methods to query relevant context for translations.
    """

    def __init__(self, language_key: str, data_dir: str = "data"):
        self.language_key = language_key
        self.data_dir = os.path.join(data_dir, language_key)
        self.dictionary = self._load_json("dictionary.json")
        self.grammar = self._load_json("grammar.json")
        self.phrases = self._load_json("phrases.json")

    def _load_json(self, filename: str) -> dict:
        """Load a JSON data file."""
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.exists(filepath):
            return {}
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def search_dictionary(self, query: str, max_results: int = 10) -> str:
        """Search the dictionary for relevant entries.

        Searches both Spanish and indigenous language entries for matches.

        Args:
            query: Search term (in Spanish or indigenous language).
            max_results: Maximum number of results to return.

        Returns:
            Formatted string of matching dictionary entries.
        """
        query_lower = query.lower()
        results = []

        categories = self.dictionary.get("categories", {})
        for cat_key, category in categories.items():
            for entry in category.get("entries", []):
                awajun = entry.get("awajun", "").lower()
                spanish = entry.get("spanish", "").lower()

                if query_lower in awajun or query_lower in spanish:
                    results.append(
                        f"  {entry['awajun']} = {entry['spanish']}"
                        + (f" ({entry['context']})" if entry.get("context") else "")
                    )

                if len(results) >= max_results:
                    break

        if not results:
            return "No se encontraron entradas relevantes."
        return "\n".join(results)

    def get_category_vocabulary(self, category: str) -> str:
        """Get all vocabulary from a specific category.

        Args:
            category: Category key (e.g., 'saludos', 'familia', 'numeros').

        Returns:
            Formatted string of all entries in the category.
        """
        categories = self.dictionary.get("categories", {})
        cat_data = categories.get(category, {})

        if not cat_data:
            available = ", ".join(categories.keys())
            return f"Categoría '{category}' no encontrada. Disponibles: {available}"

        lines = [f"## {cat_data.get('name_es', category)}"]
        for entry in cat_data.get("entries", []):
            line = f"  {entry['awajun']} = {entry['spanish']}"
            if entry.get("context"):
                line += f" ({entry['context']})"
            lines.append(line)

        return "\n".join(lines)

    def get_all_vocabulary_context(self) -> str:
        """Get a summary of all available vocabulary for LLM context.

        Returns a condensed format suitable for including in
        translation prompts as few-shot reference material.
        """
        lines = []
        categories = self.dictionary.get("categories", {})

        for cat_key, category in categories.items():
            lines.append(f"\n[{category.get('name_es', cat_key)}]")
            for entry in category.get("entries", []):
                lines.append(f"  {entry['awajun']} = {entry['spanish']}")

        return "\n".join(lines)

    def get_grammar_context(self) -> str:
        """Get grammar rules formatted for LLM context."""
        if not self.grammar:
            return "No hay reglas gramaticales disponibles."

        lines = []

        word_order = self.grammar.get("word_order", {})
        if word_order:
            lines.append(f"ORDEN DE PALABRAS: {word_order.get('basic', '')} - {word_order.get('description', '')}")
            for ex in word_order.get("examples", []):
                lines.append(f"  Ejemplo: {ex['awajun']} = {ex['spanish_natural']}")

        conjugation = self.grammar.get("verb_conjugation", {})
        if conjugation:
            lines.append(f"\nCONJUGACIÓN: {conjugation.get('description', '')}")
            suffixes = conjugation.get("present_tense_suffixes", {})
            for suffix, meaning in suffixes.items():
                lines.append(f"  {suffix}: {meaning}")

        suffixes_section = self.grammar.get("suffixes", {})
        if suffixes_section:
            lines.append(f"\nSUFIJOS COMUNES:")
            for s in suffixes_section.get("common_suffixes", []):
                lines.append(f"  {s['suffix']}: {s['meaning']} (ej: {s['example']})")

        negation = self.grammar.get("negation", {})
        if negation:
            lines.append(f"\nNEGACIÓN: {negation.get('description', '')}")

        return "\n".join(lines)

    def get_matching_phrases(self, query: str) -> str:
        """Find phrases matching a query for context.

        Args:
            query: Search term to match against phrases.

        Returns:
            Formatted matching phrases.
        """
        query_lower = query.lower()
        results = []

        for section_key in ["classroom_phrases", "daily_interaction", "cultural_expressions"]:
            section = self.phrases.get(section_key, [])
            for phrase in section:
                spanish = phrase.get("spanish", "").lower()
                awajun = phrase.get("awajun", "").lower()

                if query_lower in spanish or query_lower in awajun:
                    results.append(
                        f"  ES: {phrase['spanish']}\n"
                        f"  AW: {phrase['awajun']}"
                    )
                    if phrase.get("pronunciation_guide"):
                        results.append(f"  Pronunciación: {phrase['pronunciation_guide']}")
                    results.append("")

        if not results:
            return "No se encontraron frases relevantes."
        return "\n".join(results)

    def get_classroom_phrases(self) -> list[dict]:
        """Get all classroom phrases as structured data."""
        return self.phrases.get("classroom_phrases", [])

    def get_cultural_expressions(self) -> list[dict]:
        """Get cultural expressions with their notes."""
        return self.phrases.get("cultural_expressions", [])

    def get_available_categories(self) -> list[str]:
        """List available dictionary categories."""
        return list(self.dictionary.get("categories", {}).keys())
