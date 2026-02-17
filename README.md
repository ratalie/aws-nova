# 🌿 Chicham — Voice Bridge for Indigenous Languages of Peru

> **chicham** (Awajún): *word, language, message* — The concept that encompasses all human communication.

## The Problem

Peru has **48 officially recognized indigenous languages**. However, in Amazonian indigenous communities like the **Awajún** (~70,000 people in Amazonas, San Martín, Cajamarca, Loreto, and Ucayali), assigned teachers speak Spanish or other indigenous languages — **but not the language of the community where they teach**.

With only **24 registered interpreters** for the entire Awajún nation, classroom communication is severely limited. Children don't learn in their native language, and teachers cannot effectively transmit knowledge.

**This is not just a linguistic problem — it's an educational crisis affecting thousands of children.**

## The Solution

**Chicham** is a voice-powered educational assistant built with Amazon Nova that acts as a **linguistic and cultural bridge** between Spanish-speaking teachers and students from indigenous communities.

### How It Works

```
Teacher (Voice in Spanish) → Nova 2 Sonic → Spanish Text
                                                    ↓
                                          Nova 2 Lite + Knowledge Base
                                          (Translation + Cultural Context)
                                                    ↓
                                 Awajún Text + Pronunciation Guide → Student
```

1. **Teacher speaks in Spanish** → Amazon Nova 2 Sonic captures and transcribes audio in real-time
2. **Nova 2 Lite translates and adapts** → Using a linguistic knowledge base (dictionary, grammar, phrases) specific to Awajún
3. **Student receives** → Text in their native language with pronunciation guides
4. **Reverse direction** → Student communicates and teacher understands
5. **Lesson generator** → Creates culturally appropriate bilingual educational material

## Features

| Feature | Description | Nova Model |
|---|---|---|
| 💬 **Bidirectional Translator** | Spanish ↔ Awajún with cultural context | Nova 2 Lite |
| 🎤 **Voice Interface** | Teacher speaks naturally in Spanish | Nova 2 Sonic |
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
│  (Spanish Voice) │  (Translation + Reasoning)           │
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

- **Education**: Facilitates Bilingual Intercultural Education (EIB) in communities lacking sufficient bilingual teachers
- **Language Preservation**: Documents and promotes endangered indigenous languages
- **Scalability**: System is extensible to all 48 indigenous languages of Peru
- **Accessibility**: Web interface accessible from any device with internet

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
