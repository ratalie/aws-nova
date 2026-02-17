"""Application configuration."""

import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
NOVA_SONIC_MODEL_ID = os.getenv("NOVA_SONIC_MODEL_ID", "amazon.nova-2-sonic-v1:0")
NOVA_LITE_MODEL_ID = os.getenv("NOVA_LITE_MODEL_ID", "amazon.nova-2-lite-v1:0")

SUPPORTED_LANGUAGES = {
    "awajun": {
        "name": "Awajún",
        "iso_code": "agr",
        "family": "Jíbaro",
        "speakers": 56584,
        "alphabet": list("abchdeghi jkmnprstuwy") + ["ch", "sh", "ts"],
        "data_path": "data/awajun",
    }
}

SOURCE_LANGUAGE = "es"  # Spanish
SOURCE_LANGUAGE_NAME = "Español"

SONIC_VOICE_ID = "tomas"  # Spanish male voice
SONIC_SAMPLE_RATE = 16000
SONIC_CHANNELS = 1
