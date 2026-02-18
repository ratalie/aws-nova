"""Chicham - Streamlit web application.

Main entry point for the web demo. Provides a bilingual educational
interface for teachers and students to communicate across the
Spanish-Indigenous language barrier.

Run with: streamlit run app/main.py
"""

import io
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from app.translator import Translator
from app.knowledge_base import KnowledgeBase
from app.nova_sonic import NovaSonicClient
from app.config import SUPPORTED_LANGUAGES

# --- Page Configuration ---
st.set_page_config(
    page_title="Chicham - Voice Bridge",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS ---
st.markdown("""
<style>
/* ---- Global theme ---- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.stApp { font-family: 'Inter', sans-serif; }

/* ---- Hero banner ---- */
.hero-banner {
    background: linear-gradient(135deg, #0d4f2b 0%, #1a7a4a 40%, #2ecc71 100%);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    margin-bottom: 1.5rem;
    color: white;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-banner h1 {
    font-size: 2.4rem;
    font-weight: 700;
    margin: 0 0 0.5rem 0;
    letter-spacing: -0.5px;
}
.hero-banner p {
    font-size: 1.1rem;
    opacity: 0.92;
    margin: 0;
    font-weight: 300;
}
.hero-subtitle {
    font-size: 0.95rem;
    opacity: 0.75;
    margin-top: 0.8rem;
    font-style: italic;
}

/* ---- EN button (top-right) ---- */
.en-button {
    position: fixed;
    top: 70px;
    right: 20px;
    z-index: 9999;
    background: linear-gradient(135deg, #1a5276, #2980b9);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    transition: all 0.3s ease;
    letter-spacing: 0.5px;
}
.en-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.3);
}

/* ---- Stat cards ---- */
.stat-card {
    background: linear-gradient(135deg, #f8f9fa, #ffffff);
    border: 1px solid #e9ecef;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    transition: transform 0.2s ease;
}
.stat-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
}
.stat-number {
    font-size: 1.8rem;
    font-weight: 700;
    color: #0d4f2b;
    margin: 0;
}
.stat-label {
    font-size: 0.8rem;
    color: #6c757d;
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ---- Phrase cards ---- */
.phrase-card {
    background: white;
    border: 1px solid #e9ecef;
    border-left: 4px solid #2ecc71;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    transition: all 0.2s ease;
}
.phrase-card:hover {
    border-left-color: #0d4f2b;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}

/* ---- Flow diagram ---- */
.flow-step {
    background: linear-gradient(135deg, #0d4f2b, #1a7a4a);
    color: white;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    font-weight: 500;
    font-size: 0.9rem;
}
.flow-arrow {
    text-align: center;
    font-size: 1.5rem;
    color: #2ecc71;
    padding: 0.3rem;
}

/* ---- Tab styling ---- */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0;
    padding: 10px 20px;
    font-weight: 500;
}

/* ---- Powered by badge ---- */
.powered-by {
    background: linear-gradient(135deg, #232f3e, #37475a);
    color: white;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    font-size: 0.75rem;
    text-align: center;
    margin-top: 1rem;
}

/* ---- Modal overlay for EN ---- */
.en-modal-overlay {
    background: rgba(0,0,0,0.6);
    backdrop-filter: blur(4px);
}
</style>
""", unsafe_allow_html=True)

# --- State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_language" not in st.session_state:
    st.session_state.selected_language = "awajun"
if "show_en" not in st.session_state:
    st.session_state.show_en = False


def get_translator() -> Translator:
    lang_key = st.session_state.selected_language
    lang_config = SUPPORTED_LANGUAGES[lang_key]
    return Translator(lang_key, lang_config["name"])


def get_knowledge_base() -> KnowledgeBase:
    return KnowledgeBase(st.session_state.selected_language)


# --- Sidebar ---
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0;">
        <div style="font-size: 2.5rem;">🌿</div>
        <div style="font-size: 1.5rem; font-weight: 700; color: #0d4f2b; letter-spacing: -0.5px;">Chicham</div>
        <div style="font-size: 0.8rem; color: #6c757d; margin-top: 4px;">Voice Bridge for Indigenous Languages</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    lang_options = {k: v["name"] for k, v in SUPPORTED_LANGUAGES.items()}
    selected = st.selectbox(
        "Lengua originaria",
        options=list(lang_options.keys()),
        format_func=lambda x: f"{lang_options[x]} ({SUPPORTED_LANGUAGES[x]['speakers']:,} hablantes)",
        key="selected_language",
    )

    lang_config = SUPPORTED_LANGUAGES[selected]

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f0fdf4, #dcfce7); border-radius: 10px; padding: 1rem; border: 1px solid #bbf7d0;">
        <div style="font-weight: 600; color: #0d4f2b; font-size: 1.1rem;">{lang_config['name']}</div>
        <div style="font-size: 0.85rem; color: #4a5568; margin-top: 6px;">
            Familia: {lang_config['family']}<br>
            ISO: <code>{lang_config['iso_code']}</code><br>
            Hablantes: <strong>{lang_config['speakers']:,}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div class="powered-by">
        Powered by <strong>Amazon Nova 2</strong><br>
        Lite + Sonic on AWS Bedrock<br>
        <span style="opacity:0.7">#AmazonNova Hackathon</span>
    </div>
    """, unsafe_allow_html=True)


# --- [EN] Button ---
en_col1, en_col2 = st.columns([9, 1])
with en_col2:
    if st.button("🇬🇧 EN", help="Read about this project in English"):
        st.session_state.show_en = not st.session_state.show_en

# --- English Explanation Popup ---
if st.session_state.show_en:
    st.info("**🇬🇧 About Chicham — For English Speakers**", icon="🌍")
    with st.container():
        st.markdown("""
### The Problem

In Peru, **70,000+ Awajun indigenous people** face an educational crisis. Teachers assigned to their
communities speak **Spanish or Quechua** — but **not Awajun**. The state sends teachers who speak other
native languages, assuming "close enough" works. It doesn't.

Even a Quechua-speaking teacher in an Awajun community cannot transmit knowledge in the students'
mother tongue, nor preserve their **cultural identity** — their spiritual connection to *Nugkui*
(earth spirit), *Etsa* (sun), *Tsugki* (water spirit), their oral traditions, and their sacred
relationship with the forest (*ikam*).

With only **24 registered interpreters** for the entire Awajun nation, the result is a vicious cycle:
no Awajun teachers → language fades → fewer youth access higher education → even fewer teachers.

### The Solution

**Chicham** ("word/language" in Awajun) is a **voice-powered AI educational assistant** that bridges
this gap using **Amazon Nova**:

1. **Teacher speaks** in Spanish or Quechua → **Nova 2 Sonic** transcribes in real-time
2. **Nova 2 Lite** translates using an Awajun knowledge base (dictionary, grammar, cultural context)
3. **Student receives** text in Awajun with pronunciation guides and **cultural notes**
4. **Reverse direction** works too — student speaks Awajun, teacher understands
5. **Lesson generator** creates bilingual content integrating Awajun cosmovision

### Long-Term Vision

- **Now**: Help current teachers communicate while preserving cultural identity
- **Medium-term**: Awajun students stay in school longer through cultural connection
- **Long-term**: More Awajun youth access higher education and return as **bilingual teachers**,
  breaking the cycle

### Tech: Amazon Nova 2 Sonic (voice) + Nova 2 Lite (translation & reasoning) on AWS Bedrock
        """)
    if st.button("Close / Cerrar"):
        st.session_state.show_en = False


# --- Hero Banner ---
st.markdown(f"""
<div class="hero-banner">
    <h1>🌿 Chicham</h1>
    <p>Puente de voces entre profesores y comunidades originarias del Peru</p>
    <p>Espanol/Quechua ↔ {lang_config['name']} — preservando lengua, cultura e identidad</p>
    <div class="hero-subtitle">"Iina chicham — Nuestro idioma es nuestra identidad"</div>
</div>
""", unsafe_allow_html=True)

# --- Stats Row ---
s1, s2, s3, s4 = st.columns(4)
with s1:
    st.markdown("""<div class="stat-card"><p class="stat-number">70,468</p><p class="stat-label">Poblacion Awajun</p></div>""", unsafe_allow_html=True)
with s2:
    st.markdown("""<div class="stat-card"><p class="stat-number">56,584</p><p class="stat-label">Hablantes nativos</p></div>""", unsafe_allow_html=True)
with s3:
    st.markdown("""<div class="stat-card"><p class="stat-number">24</p><p class="stat-label">Interpretes registrados</p></div>""", unsafe_allow_html=True)
with s4:
    st.markdown("""<div class="stat-card"><p class="stat-number">48</p><p class="stat-label">Lenguas originarias Peru</p></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Tabs ---
tab_translate, tab_lessons, tab_phrases, tab_dictionary, tab_about = st.tabs(
    ["🎤 Traductor + Voz", "📚 Lecciones", "🗣️ Frases", "📖 Diccionario", "ℹ️ Acerca de"]
)

# --- Translation Tab ---
with tab_translate:
    # Flow diagram
    f1, f2, f3, f4, f5 = st.columns([2, 0.5, 2, 0.5, 2])
    with f1:
        st.markdown('<div class="flow-step">🎤 Profesor habla<br><small>Espanol / Quechua</small></div>', unsafe_allow_html=True)
    with f2:
        st.markdown('<div class="flow-arrow">→</div>', unsafe_allow_html=True)
    with f3:
        st.markdown('<div class="flow-step">🧠 Nova 2 Lite<br><small>Traduce + Contexto Cultural</small></div>', unsafe_allow_html=True)
    with f4:
        st.markdown('<div class="flow-arrow">→</div>', unsafe_allow_html=True)
    with f5:
        st.markdown(f'<div class="flow-step">📝 Estudiante recibe<br><small>{lang_config["name"]} + Pronunciacion</small></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_direction = st.columns(2)
    with col_direction[0]:
        source_lang = st.radio(
            "Idioma del profesor",
            options=["Espanol", "Quechua"],
            horizontal=True,
        )
    with col_direction[1]:
        direction = st.radio(
            "Direccion",
            options=["to_indigenous", "from_indigenous"],
            format_func=lambda x: (
                f"{source_lang} → {lang_config['name']}"
                if x == "to_indigenous"
                else f"{lang_config['name']} → {source_lang}"
            ),
            horizontal=True,
        )

    # --- Voice Input ---
    st.markdown("---")
    st.markdown("#### 🎤 Entrada por voz")
    st.caption("Presiona el boton para grabar, habla, y presiona de nuevo para parar")

    voice_col1, voice_col2 = st.columns([1, 4])
    with voice_col1:
        audio_bytes = audio_recorder(
            text="",
            recording_color="#e74c3c",
            neutral_color="#2ecc71",
            icon_size="3x",
            pause_threshold=2.0,
            sample_rate=16000,
        )
    with voice_col2:
        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")

    voice_text = ""
    if audio_bytes:
        with st.spinner("🎤 Transcribiendo con Amazon Transcribe..."):
            try:
                sonic = NovaSonicClient()
                voice_text = sonic.transcribe_audio(audio_bytes)
                st.success(f"**Transcripcion:** {voice_text}")
            except Exception as e:
                st.warning(f"Transcripcion no disponible: {e}. Usa el campo de texto.")

    st.markdown("---")

    # --- Text Input ---
    st.markdown("#### 💬 Texto para traducir")
    col_input, col_output = st.columns(2)

    with col_input:
        source_label = (
            f"Texto en {source_lang}"
            if direction == "to_indigenous"
            else f"Texto en {lang_config['name']}"
        )
        default_text = voice_text if voice_text else ""
        input_text = st.text_area(
            source_label, value=default_text, height=150, key="translate_input"
        )

    translate_btn = st.button(
        "🔄 Traducir con Amazon Nova", type="primary", use_container_width=True
    )

    if translate_btn and input_text:
        translator = get_translator()
        with st.spinner("Traduciendo con Amazon Nova 2 Lite..."):
            try:
                if direction == "to_indigenous":
                    result = translator.translate_to_indigenous(
                        input_text, source_lang_override=source_lang
                    )
                else:
                    result = translator.translate_to_spanish(
                        input_text, target_lang_override=source_lang
                    )

                with col_output:
                    target_label = (
                        f"Traduccion en {lang_config['name']}"
                        if direction == "to_indigenous"
                        else f"Traduccion en {source_lang}"
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
                st.error(f"Error en la traduccion: {e}")

    if input_text:
        with st.expander("🌎 Contexto cultural — Mas alla de la traduccion"):
            if st.button("Obtener contexto cultural"):
                translator = get_translator()
                with st.spinner("Analizando contexto cultural con Nova 2 Lite..."):
                    try:
                        context = translator.explain_culture(input_text)
                        st.markdown(context)
                    except Exception as e:
                        st.error(f"Error: {e}")

# --- Lessons Tab ---
with tab_lessons:
    st.markdown(f"### 📚 Generador de Lecciones Bilingues")
    st.caption(f"Crea material educativo en Espanol y {lang_config['name']} con contexto cultural integrado")

    col_topic, col_level = st.columns([3, 1])
    with col_topic:
        topic = st.text_input(
            "Tema de la leccion",
            placeholder="Ej: Los numeros, La familia, Los animales del bosque, Nugkui y la tierra...",
        )
    with col_level:
        difficulty = st.selectbox(
            "Nivel",
            options=["basico", "intermedio", "avanzado"],
        )

    if st.button("📝 Generar Leccion con Amazon Nova", type="primary") and topic:
        translator = get_translator()
        with st.spinner("Generando leccion bilingue con Amazon Nova 2 Lite..."):
            try:
                lesson = translator.generate_lesson(topic, difficulty)
                st.markdown(lesson)
            except Exception as e:
                st.error(f"Error generando la leccion: {e}")

# --- Phrases Tab ---
with tab_phrases:
    st.markdown(f"### 🗣️ Libro de Frases")
    st.caption(f"Frases esenciales en Espanol y {lang_config['name']} con guia de pronunciacion")

    phrase_category = st.radio(
        "Categoria",
        options=["classroom", "daily", "cultural"],
        format_func=lambda x: {
            "classroom": "🏫 Frases de aula",
            "daily": "🌅 Interaccion diaria",
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
        st.markdown(f"""
        <div class="phrase-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <span style="color:#6c757d; font-size:0.8rem;">ES</span>
                    <strong> {phrase.get('spanish', '')}</strong>
                </div>
                <div>
                    <span style="color:#0d4f2b; font-size:0.8rem;">{lang_config['name'].upper()}</span>
                    <strong style="color:#0d4f2b;"> {phrase.get('awajun', '')}</strong>
                </div>
            </div>
            {"<div style='margin-top:6px; font-size:0.8rem; color:#888;'>🔊 " + phrase.get('pronunciation_guide', '') + "</div>" if phrase.get('pronunciation_guide') else ""}
            {"<div style='margin-top:4px; font-size:0.8rem; color:#5a8a6a;'>🌎 " + phrase.get('cultural_note', '') + "</div>" if phrase.get('cultural_note') else ""}
        </div>
        """, unsafe_allow_html=True)

# --- Dictionary Tab ---
with tab_dictionary:
    st.markdown(f"### 📖 Diccionario Espanol — {lang_config['name']}")
    st.caption("Vocabulario categorizado con contexto cultural")

    kb = get_knowledge_base()
    categories = kb.get_available_categories()

    search_term = st.text_input(
        "🔍 Buscar palabra",
        placeholder=f"Buscar en Espanol o {lang_config['name']}...",
    )

    if search_term:
        results = kb.search_dictionary(search_term, max_results=20)
        st.text(results)
    else:
        cat_cols = st.columns(len(categories))
        for i, cat in enumerate(categories):
            with cat_cols[i]:
                if st.button(cat.replace("_", " ").title(), use_container_width=True):
                    st.session_state.selected_cat = cat

        selected_cat = st.session_state.get("selected_cat", categories[0] if categories else None)
        if selected_cat:
            vocab = kb.get_category_vocabulary(selected_cat)
            st.text(vocab)

# --- About Tab ---
with tab_about:
    st.markdown("""
### Acerca de Chicham

#### El Problema

En Peru, las comunidades indigenas como los **Awajun** (~70,000 personas)
enfrentan una crisis educativa: los profesores asignados a sus comunidades
hablan **espanol, quechua u otras lenguas nativas mas "mainstream"** —
pero **no la lengua de la comunidad donde ensenan**.

Incluso cuando el Estado envia profesores que hablan otras lenguas
originarias, la brecha persiste: **diferente idioma, diferente cosmovision,
diferente identidad cultural**. Estos profesores, a pesar de su esfuerzo,
no pueden transmitir conocimiento en la lengua materna de los estudiantes,
ni preservar la identidad cultural Awajun — su conexion espiritual con
*Nugkui* (espiritu de la tierra), *Etsa* (sol), *Tsugki* (espiritu del agua),
sus tradiciones orales, su relacion con el *ikam* (bosque).

Con solo **24 interpretes registrados** para toda la nacion Awajun,
el resultado es un ciclo que se perpetua: sin maestros Awajun, el idioma
se debilita; al debilitarse el idioma, menos jovenes Awajun acceden a
educacion superior; sin profesionales Awajun, hay aun menos maestros.

#### La Solucion

**Chicham** (que significa "palabra/idioma" en Awajun) es un asistente
educativo de voz que actua como **puente linguistico y cultural**:

1. **El profesor habla en espanol o quechua** → Nova 2 Sonic captura y transcribe
2. **Nova 2 Lite traduce y adapta** → Usando una base de conocimiento linguistico y cultural Awajun
3. **El estudiante recibe** → Texto en su lengua originaria con guias de pronunciacion y **notas culturales**
4. **Direccion inversa** → El estudiante se comunica y el profesor entiende
5. **Generador de lecciones** → Material bilingue que integra la cosmovision Awajun

#### Vision a Largo Plazo

Chicham no es solo una herramienta de traduccion — es un catalizador:

- **Ahora**: Ayudar a los profesores actuales a comunicarse efectivamente
- **Mediano plazo**: Estudiantes Awajun conectados con su cultura permanecen mas tiempo en la escuela
- **Largo plazo**: Mas jovenes Awajun acceden a educacion superior y regresan como **maestros bilingues Awajun**, fortaleciendo la comunidad desde adentro

#### Tecnologia

- **Amazon Nova 2 Sonic** — Reconocimiento de voz en espanol/quechua (speech-to-text)
- **Amazon Nova 2 Lite** — Traduccion, razonamiento cultural y generacion de contenido
- **Base de conocimiento** — Diccionario, gramatica, frases y cultura Awajun
- **Python + Streamlit** — Aplicacion web accesible

---
*Construido para el Amazon Nova AI Hackathon* **#AmazonNova**
    """)
