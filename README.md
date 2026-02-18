# 🌿 Chicham — Voice Bridge for Indigenous Languages of Peru

> **chicham** (Awajún): *word, language, message* — The concept that encompasses all human communication.

## The Problem

Peru has **48 officially recognized indigenous languages**. However, in Amazonian indigenous communities like the **Awajún** (~70,000 people in Amazonas, San Martín, Cajamarca, Loreto, and Ucayali), the teachers assigned to their schools come from outside — speaking **Spanish, Quechua, or other more mainstream indigenous languages**, but **not Awajún**.

Because there aren't enough Awajún-speaking teachers, the state sends teachers who speak other native languages, assuming linguistic proximity is "close enough." But even when a Quechua-speaking teacher is sent to an Awajún community, the gap remains: **different language, different cosmovision, different cultural identity**. These teachers, despite their best efforts, cannot transmit knowledge in the students' mother tongue, nor can they preserve and reinforce the Awajún cultural identity — their spiritual connection to *Nugkui* (earth spirit), *Etsa* (sun), *Tsugki* (water spirit), their oral traditions, their relationship with the *ikam* (forest).

With only **24 registered interpreters** for the entire Awajún nation, the result is:
- Children lose connection with their language and culture
- Teachers struggle to communicate effectively in the classroom
- Awajún cultural identity erodes with each generation
- Fewer young Awajún pursue higher education to become teachers themselves

**This is not just a linguistic problem — it's a cultural survival crisis. And it perpetuates a cycle: without Awajún teachers, the language fades; as the language fades, fewer Awajún access higher education; without educated Awajún, there are even fewer teachers.**

## The Solution

**Chicham** is a voice-powered educational assistant built with Amazon Nova that acts as a **linguistic and cultural bridge** between teachers (who may speak Spanish, Quechua, or other languages) and Awajún students — preserving not just the language, but the cultural identity of the community.

### How It Works

```
Teacher (Voice in Spanish/Quechua) → Nova 2 Sonic → Transcribed Text
                                                          ↓
                                               Nova 2 Lite + Knowledge Base
                                               (Translation + Cultural Context
                                                + Identity Preservation)
                                                          ↓
                                    Awajún Text + Cultural Notes + Pronunciation → Student
                                                          ↓
                                              Student responds in Awajún
                                                          ↓
                                               Nova 2 Lite → Teacher understands
```

1. **Teacher speaks in Spanish or Quechua** → Amazon Nova 2 Sonic captures and transcribes audio in real-time
2. **Nova 2 Lite translates and adapts** → Using a linguistic knowledge base (dictionary, grammar, phrases) specific to Awajún, enriched with cultural context
3. **Student receives** → Text in Awajún with pronunciation guides **and cultural notes** that reinforce their identity
4. **Reverse direction** → Student communicates in Awajún and the teacher understands
5. **Lesson generator** → Creates bilingual educational material that integrates Awajún cosmovision (Nugkui, Etsa, Tsugki) alongside academic content
6. **Cultural preservation** → Every interaction reinforces Awajún identity, oral traditions, and connection to territory

### Long-Term Vision

Chicham is not just a translation tool — it's a catalyst for breaking the cycle:

1. **Now**: Help current teachers (Spanish/Quechua-speaking) communicate effectively with Awajún students while preserving cultural identity
2. **Medium-term**: Awajún students who feel connected to their culture and language stay in school longer and achieve better outcomes
3. **Long-term**: More Awajún youth access higher education and return as **bilingual Awajún teachers**, reducing dependency on external teachers and strengthening the community from within

## Features

| Feature | Description | Nova Model |
|---|---|---|
| 💬 **Bidirectional Translator** | Spanish/Quechua ↔ Awajún with cultural context | Nova 2 Lite |
| 🎤 **Voice Interface** | Teacher speaks naturally in Spanish or Quechua | Nova 2 Sonic |
| 📚 **Lesson Generator** | Bilingual educational material by level | Nova 2 Lite |
| 🗣️ **Phrase Book** | Classroom phrases with pronunciation guide | Knowledge Base |
| 📖 **Integrated Dictionary** | Categorized vocabulary with cultural context | Knowledge Base |
| 🌎 **Cultural Context** | Cultural explanations for teachers | Nova 2 Lite |

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit Web App                      │
│                    (User Interface)                       │
├─────────────┬──────────────────┬────────────────────────┤
│  Translator │  Lesson Gen.     │  Phrases / Dictionary  │
├─────────────┴──────────────────┴────────────────────────┤
│                   Translator Engine                       │
│            (Orchestrates KB + Nova 2 Lite)              │
├──────────────────┬──────────────────────────────────────┤
│  Nova 2 Sonic    │         Nova 2 Lite                   │
│  (ES/QU Voice)   │  (Translation + Cultural Reasoning)  │
│  amazon.nova-    │  amazon.nova-2-lite-v1:0             │
│  2-sonic-v1:0    │                                       │
├──────────────────┴──────────────────────────────────────┤
│              Awajún Knowledge Base                        │
│    Dictionary  │  Grammar  │  Phrases  │  Culture       │
└─────────────────────────────────────────────────────────┘
```

## Tech Stack

- **Amazon Nova 2 Sonic** — Bidirectional voice interface in Spanish (speech-to-speech)
- **Amazon Nova 2 Lite** — Translation, reasoning, and educational content generation
- **Amazon Bedrock** — Platform for accessing Nova models
- **Python 3.11+** — Primary language
- **boto3** — AWS SDK for Python
- **Streamlit** — Web framework for interactive demo

## Quick Start

### Prerequisites

- Python 3.11 or higher
- AWS account with Amazon Bedrock access
- Nova 2 Lite and Nova 2 Sonic models enabled in `us-east-1` region

### Installation

```bash
# Clone the repository
git clone https://github.com/ratalie/aws-nova.git
cd aws-nova

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or on Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your AWS credentials
```

### AWS Configuration

1. Create an account at [aws.amazon.com](https://aws.amazon.com)
2. Go to **Amazon Bedrock** in AWS console (region `us-east-1`)
3. In **Model access**, enable:
   - `Amazon Nova 2 Lite`
   - `Amazon Nova 2 Sonic`
4. Configure your AWS credentials:

```bash
aws configure
# Or set variables in the .env file
```

### Run the Application

```bash
streamlit run app/main.py
```

The application will be available at `http://localhost:8501`

### Run Tests

```bash
pytest tests/ -v
```

## Project Structure

```
aws-nova/
├── app/
│   ├── __init__.py
│   ├── main.py              # Streamlit web app (main interface)
│   ├── config.py             # Application configuration
│   ├── nova_sonic.py         # Nova 2 Sonic client (voice)
│   ├── nova_lite.py          # Nova 2 Lite client (translation/reasoning)
│   ├── translator.py         # Translation engine (orchestrates KB + Nova)
│   └── knowledge_base.py     # Linguistic data manager
├── data/
│   └── awajun/
│       ├── dictionary.json   # Spanish-Awajún categorized dictionary
│       ├── grammar.json      # Awajún grammatical rules
│       └── phrases.json      # Common phrases with pronunciation
├── tests/
│   ├── __init__.py
│   └── test_knowledge_base.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## About the Awajún People

| Data | Details |
|---|---|
| **Population** | ~70,468 people |
| **Native Speakers** | ~56,584 native speakers |
| **Location** | Amazonas, San Martín, Cajamarca, Loreto, Ucayali |
| **Language Family** | Jivaroan |
| **Official Alphabet** | 21 graphemes (standardized by RM N° 2554-2009-ED) |
| **Registered Interpreters** | Only 24 for the entire nation |
| **Recognized Communities** | 245 of 488 localities |

Source: [Indigenous Peoples Database - Peru's Ministry of Culture](https://bdpi.cultura.gob.pe/pueblos/awajun)

## Educational Reference Resources (MINEDU)

The project is based on official materials from Peru's Ministry of Education for Bilingual Intercultural Education (EIB):

| Resource | Description | Link |
|---|---|---|
| **Awajún Pedagogical Vocabulary** | Technical-pedagogical terminology in Awajún | [MINEDU Repository](https://repositorio.minedu.gob.pe/handle/20.500.12799/7195) |
| **Wasugkamku Unuimajagmi** | Workbooks for initial level | [MINEDU Repository](https://repositorio.minedu.gob.pe/handle/20.500.12799/11896) |
| **Tsayag Series** | Communication texts 1st-5th grade in Awajún | MINEDU Repository |
| **Mina wakesa augtaig Teacher's Guide** | Guide for reading assessments | [MINEDU Repository](https://repositorio.minedu.gob.pe/handle/20.500.12799/6718) |
| **Kuwam etemagmau** | Stories and narratives for initial level | MINEDU Repository |
| **Awajún People Data** | Official database from Min. of Culture | [BDPI](https://bdpi.cultura.gob.pe/pueblos/awajun) |

## Potential Impact

- **Immediate**: Helps Spanish- and Quechua-speaking teachers communicate effectively with Awajún students in the classroom
- **Cultural Preservation**: Reinforces Awajún identity, cosmovision, and oral traditions through every interaction — not just translating words, but preserving meaning
- **Breaking the Cycle**: By keeping Awajún children engaged in education through their own language and culture, more will access higher education and return as Awajún-speaking teachers
- **Scalability**: System is extensible to all 48 indigenous languages of Peru, each with their own cultural knowledge base
- **Accessibility**: Web interface accessible from any device with internet, designed for rural communities

## Hackathon Category

**Voice AI** — Real-time conversational voice experiences using Amazon Nova 2 Sonic

With components of:
- **Multimodal Understanding** — Text and voice comprehension across languages
- **Agentic AI** — Autonomous educational agent that reasons about cultural context

## Team

Project developed for the **Amazon Nova AI Hackathon** #AmazonNova

## License

MIT License — See [LICENSE](LICENSE) for details.

---

*"Iina chicham — Our language is our identity"*
