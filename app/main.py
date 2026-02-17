"""Chicham - Streamlit web application.

Main entry point for the web demo. Provides a bilingual educational
interface for teachers and students to communicate across the
Spanish-Indigenous language barrier.

Run with: streamlit run app/main.py
"""

import streamlit as st
from app.translator import Translator
from app.knowledge_base import KnowledgeBase
from app.config import SUPPORTED_LANGUAGES

# --- Page Configuration ---
st.set_page_config(
    page_title="Chicham - Puente de Voces",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_language" not in st.session_state:
    st.session_state.selected_language = "awajun"


def get_translator() -> Translator:
    """Get or create the Translator instance."""
    lang_key = st.session_state.selected_language
    lang_config = SUPPORTED_LANGUAGES[lang_key]
    return Translator(lang_key, lang_config["name"])


def get_knowledge_base() -> KnowledgeBase:
    """Get or create the KnowledgeBase instance."""
    return KnowledgeBase(st.session_state.selected_language)


# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/amazon-web-services.png", width=60)
    st.title("Chicham")
    st.caption("Puente de Voces para Lenguas Originarias del Perú")

    st.divider()

    # Language selector
    lang_options = {k: v["name"] for k, v in SUPPORTED_LANGUAGES.items()}
    selected = st.selectbox(
        "Lengua originaria",
        options=list(lang_options.keys()),
        format_func=lambda x: f"{lang_options[x]} ({SUPPORTED_LANGUAGES[x]['speakers']:,} hablantes)",
        key="selected_language",
    )

    lang_config = SUPPORTED_LANGUAGES[selected]
    st.info(
        f"**{lang_config['name']}**\n\n"
        f"Familia: {lang_config['family']}\n\n"
        f"Código ISO: {lang_config['iso_code']}\n\n"
        f"Hablantes: {lang_config['speakers']:,}"
    )

    st.divider()
    st.caption(
        "Construido con Amazon Nova 2 Lite y Nova 2 Sonic "
        "para el Amazon Nova AI Hackathon #AmazonNova"
    )

# --- Main Content ---
st.title("🌿 Chicham — Puente de Voces")
st.markdown(
    f"Asistente educativo bilingüe **Español ↔ {lang_config['name']}** "
    f"para comunidades originarias del Perú"
)

# --- Tabs ---
tab_translate, tab_lessons, tab_phrases, tab_dictionary, tab_about = st.tabs(
    ["💬 Traductor", "📚 Lecciones", "🗣️ Frases", "📖 Diccionario", "ℹ️ Acerca de"]
)

# --- Translation Tab ---
with tab_translate:
    st.subheader("Traductor Bidireccional")

    col_direction = st.columns(2)
    with col_direction[0]:
        direction = st.radio(
            "Dirección",
            options=["es_to_indigenous", "indigenous_to_es"],
            format_func=lambda x: (
                f"Español → {lang_config['name']}"
                if x == "es_to_indigenous"
                else f"{lang_config['name']} → Español"
            ),
            horizontal=True,
        )

    col_input, col_output = st.columns(2)

    with col_input:
        source_label = (
            "Texto en Español"
            if direction == "es_to_indigenous"
            else f"Texto en {lang_config['name']}"
        )
        input_text = st.text_area(source_label, height=150, key="translate_input")

    translate_btn = st.button(
        "🔄 Traducir", type="primary", use_container_width=True
    )

    if translate_btn and input_text:
        translator = get_translator()

        with st.spinner("Traduciendo con Amazon Nova 2 Lite..."):
            try:
                if direction == "es_to_indigenous":
                    result = translator.translate_to_indigenous(input_text)
                else:
                    result = translator.translate_to_spanish(input_text)

                with col_output:
                    target_label = (
                        f"Traducción en {lang_config['name']}"
                        if direction == "es_to_indigenous"
                        else "Traducción en Español"
                    )
                    st.text_area(
                        target_label,
                        value=result["translation"],
                        height=150,
                        disabled=True,
                    )

                if result.get("dictionary_matches") and "No se encontraron" not in result.get("dictionary_matches", ""):
                    with st.expander("📖 Vocabulario relacionado"):
                        st.text(result["dictionary_matches"])

            except Exception as e:
                st.error(f"Error en la traducción: {e}")

    # Cultural context button
    if input_text:
        with st.expander("🌎 Contexto cultural"):
            if st.button("Obtener contexto cultural"):
                translator = get_translator()
                with st.spinner("Analizando contexto cultural..."):
                    try:
                        context = translator.explain_culture(input_text)
                        st.markdown(context)
                    except Exception as e:
                        st.error(f"Error: {e}")

# --- Lessons Tab ---
with tab_lessons:
    st.subheader(f"Generador de Lecciones Bilingües — Español / {lang_config['name']}")

    col_topic, col_level = st.columns([3, 1])
    with col_topic:
        topic = st.text_input(
            "Tema de la lección",
            placeholder="Ej: Los números, La familia, Los animales del bosque...",
        )
    with col_level:
        difficulty = st.selectbox(
            "Nivel",
            options=["básico", "intermedio", "avanzado"],
        )

    if st.button("📝 Generar Lección", type="primary") and topic:
        translator = get_translator()
        with st.spinner("Generando lección con Amazon Nova 2 Lite..."):
            try:
                lesson = translator.generate_lesson(topic, difficulty)
                st.markdown(lesson)
            except Exception as e:
                st.error(f"Error generando la lección: {e}")

# --- Phrases Tab ---
with tab_phrases:
    st.subheader(f"Frases Comunes — Español / {lang_config['name']}")

    phrase_category = st.radio(
        "Categoría",
        options=["classroom", "daily", "cultural"],
        format_func=lambda x: {
            "classroom": "🏫 Frases de aula",
            "daily": "🌅 Interacción diaria",
            "cultural": "🌿 Expresiones culturales",
        }[x],
        horizontal=True,
    )

    kb = get_knowledge_base()

    if phrase_category == "classroom":
        phrases = kb.get_classroom_phrases()
    elif phrase_category == "daily":
        phrases = kb.phrases.get("daily_interaction", [])
    else:
        phrases = kb.get_cultural_expressions()

    for phrase in phrases:
        with st.container():
            col_es, col_aw = st.columns(2)
            with col_es:
                st.markdown(f"**🇪🇸 {phrase.get('spanish', '')}**")
            with col_aw:
                st.markdown(f"**🌿 {phrase.get('awajun', '')}**")

            details = []
            if phrase.get("pronunciation_guide"):
                details.append(f"🔊 _{phrase['pronunciation_guide']}_")
            if phrase.get("context"):
                details.append(f"📝 {phrase['context']}")
            if phrase.get("cultural_note"):
                details.append(f"🌎 {phrase['cultural_note']}")

            if details:
                st.caption(" | ".join(details))
            st.divider()

# --- Dictionary Tab ---
with tab_dictionary:
    st.subheader(f"Diccionario — Español / {lang_config['name']}")

    kb = get_knowledge_base()
    categories = kb.get_available_categories()

    search_term = st.text_input(
        "🔍 Buscar palabra",
        placeholder=f"Buscar en Español o {lang_config['name']}...",
    )

    if search_term:
        results = kb.search_dictionary(search_term, max_results=20)
        st.text(results)
    else:
        selected_cat = st.selectbox(
            "Categoría",
            options=categories,
            format_func=lambda x: x.replace("_", " ").title(),
        )

        if selected_cat:
            vocab = kb.get_category_vocabulary(selected_cat)
            st.text(vocab)

# --- About Tab ---
with tab_about:
    st.subheader("Acerca de Chicham")

    st.markdown(
        """
        ### El Problema

        En Perú, las comunidades indígenas como los **Awajún** (~70,000 personas)
        enfrentan una barrera educativa crítica: los profesores asignados a sus
        comunidades hablan español u otras lenguas indígenas, **pero no la lengua
        de la comunidad donde enseñan**.

        Con solo **24 intérpretes registrados** para toda la nación Awajún,
        la comunicación en el aula se ve severamente limitada.

        ### La Solución

        **Chicham** (que significa "palabra/idioma" en Awajún) es un asistente
        educativo de voz que actúa como puente lingüístico:

        1. **El profesor habla en español** → Nova 2 Sonic captura y transcribe
        2. **Nova 2 Lite traduce y adapta** → Usando una base de conocimiento
           lingüístico y cultural Awajún
        3. **El estudiante recibe** → Texto en su lengua originaria con
           guías de pronunciación
        4. **Dirección inversa** → El estudiante se comunica y el profesor entiende

        ### Tecnología

        - **Amazon Nova 2 Sonic** — Interfaz de voz en español (speech-to-speech)
        - **Amazon Nova 2 Lite** — Traducción, razonamiento y generación de contenido
        - **Base de conocimiento** — Diccionario, gramática y frases Awajún
        - **Python + Streamlit** — Aplicación web accesible

        ### Impacto

        - Facilita la educación intercultural bilingüe
        - Preserva y promueve lenguas originarias en peligro
        - Reduce la barrera de comunicación profesor-estudiante
        - Escalable a las **48 lenguas originarias** reconocidas en Perú

        ---
        *Construido para el Amazon Nova AI Hackathon* **#AmazonNova**
        """
    )
