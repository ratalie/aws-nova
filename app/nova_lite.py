"""Nova 2 Lite client for translation and educational content generation."""

import json
import boto3
from app.config import AWS_REGION, NOVA_LITE_MODEL_ID


class NovaLiteClient:
    """Handles translation and content generation via Nova 2 Lite.

    Nova 2 Lite is a fast, cost-effective reasoning model that supports
    200+ languages for text understanding. We use it as the translation
    and reasoning engine between Spanish and indigenous languages, enhanced
    with few-shot examples from our knowledge base.
    """

    def __init__(self):
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=AWS_REGION,
        )
        self.model_id = NOVA_LITE_MODEL_ID

    def invoke(self, system_prompt: str, user_message: str) -> str:
        """Send a message to Nova 2 Lite and get a response.

        Args:
            system_prompt: System-level instructions.
            user_message: The user's input text.

        Returns:
            The model's text response.
        """
        body = {
            "messages": [
                {"role": "user", "content": [{"text": user_message}]},
            ],
            "system": [{"text": system_prompt}],
            "inferenceConfig": {
                "maxTokens": 2048,
                "temperature": 0.3,
                "topP": 0.9,
            },
        }

        response = self.client.invoke_model(
            modelId=self.model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(body),
        )

        result = json.loads(response["body"].read())
        return result["output"]["message"]["content"][0]["text"]

    def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        dictionary_context: str = "",
        grammar_context: str = "",
    ) -> str:
        """Translate text between Spanish and an indigenous language.

        Uses few-shot examples and linguistic context from the knowledge
        base to improve translation quality for underrepresented languages.

        Args:
            text: The text to translate.
            source_lang: Source language name (e.g., "Español").
            target_lang: Target language name (e.g., "Awajún").
            dictionary_context: Relevant dictionary entries as context.
            grammar_context: Relevant grammar rules as context.

        Returns:
            Translated text.
        """
        system_prompt = self._build_translation_prompt(
            source_lang, target_lang, dictionary_context, grammar_context
        )

        user_message = (
            f"Traduce el siguiente texto de {source_lang} a {target_lang}:\n\n"
            f"{text}\n\n"
            f"Devuelve SOLO la traducción, sin explicaciones."
        )

        return self.invoke(system_prompt, user_message)

    def generate_lesson(
        self,
        topic: str,
        target_lang: str,
        difficulty: str = "básico",
        dictionary_context: str = "",
    ) -> str:
        """Generate a bilingual educational lesson.

        Creates structured educational content in both Spanish and
        the target indigenous language, suitable for classroom use.

        Args:
            topic: The lesson topic.
            target_lang: Target indigenous language name.
            difficulty: Difficulty level (básico, intermedio, avanzado).
            dictionary_context: Relevant vocabulary from the knowledge base.

        Returns:
            Formatted bilingual lesson content.
        """
        system_prompt = (
            f"Eres un experto en educación intercultural bilingüe en Perú. "
            f"Creas materiales educativos bilingües en Español y {target_lang}. "
            f"Tus lecciones son culturalmente respetuosas y pedagógicamente "
            f"apropiadas para comunidades indígenas amazónicas.\n\n"
            f"Contexto lingüístico disponible:\n{dictionary_context}"
        )

        user_message = (
            f"Crea una lección bilingüe (Español/{target_lang}) sobre: {topic}\n"
            f"Nivel: {difficulty}\n\n"
            f"La lección debe incluir:\n"
            f"1. Vocabulario clave (5-10 palabras) en ambos idiomas\n"
            f"2. Frases ejemplo en ambos idiomas\n"
            f"3. Un ejercicio práctico\n"
            f"4. Notas culturales relevantes"
        )

        return self.invoke(system_prompt, user_message)

    def explain_cultural_context(
        self, text: str, language: str, cultural_notes: str = ""
    ) -> str:
        """Provide cultural context for a translated message.

        Helps teachers understand not just the words but the cultural
        meaning and appropriate usage in the indigenous community.

        Args:
            text: The text to explain.
            language: The indigenous language name.
            cultural_notes: Additional cultural context from knowledge base.

        Returns:
            Cultural explanation text.
        """
        system_prompt = (
            f"Eres un mediador cultural especializado en la cultura {language} "
            f"de la Amazonía peruana. Ayudas a profesores hispanohablantes a "
            f"entender el contexto cultural de las comunidades indígenas.\n\n"
            f"Notas culturales disponibles:\n{cultural_notes}"
        )

        user_message = (
            f"Explica el contexto cultural de este mensaje en {language}:\n\n"
            f"\"{text}\"\n\n"
            f"Incluye:\n"
            f"1. Significado cultural más allá de la traducción literal\n"
            f"2. Consideraciones de respeto cultural\n"
            f"3. Cómo usarlo apropiadamente en el aula"
        )

        return self.invoke(system_prompt, user_message)

    def _build_translation_prompt(
        self,
        source_lang: str,
        target_lang: str,
        dictionary_context: str,
        grammar_context: str,
    ) -> str:
        """Build a detailed system prompt for translation.

        Uses few-shot examples and linguistic rules to guide the model
        toward accurate translations for underrepresented languages.
        """
        prompt = (
            f"Eres un traductor especializado entre {source_lang} y "
            f"{target_lang}. Tu tarea es producir traducciones precisas "
            f"y culturalmente apropiadas.\n\n"
            f"REGLAS IMPORTANTES:\n"
            f"- Mantén el significado original\n"
            f"- Usa vocabulario apropiado para el contexto educativo\n"
            f"- Si no conoces una palabra exacta, usa la más cercana "
            f"y marca con [aprox.]\n"
            f"- Respeta las estructuras gramaticales de {target_lang}\n"
        )

        if dictionary_context:
            prompt += (
                f"\nDICCIONARIO DE REFERENCIA:\n{dictionary_context}\n"
            )

        if grammar_context:
            prompt += (
                f"\nREGLAS GRAMATICALES:\n{grammar_context}\n"
            )

        return prompt
