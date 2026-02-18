"""Voice client — SpeechRecognition for STT, Nova 2 Sonic for conversation."""

import io
import json

import boto3
import speech_recognition as sr

from app.config import AWS_REGION, NOVA_SONIC_MODEL_ID, SONIC_VOICE_ID


class NovaSonicClient:
    """Voice interface: SpeechRecognition for STT, Nova 2 Sonic for streaming."""

    def __init__(self):
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=AWS_REGION,
        )
        self.model_id = NOVA_SONIC_MODEL_ID
        self.recognizer = sr.Recognizer()

    # ----- Speech-to-text ----- #

    def transcribe_audio(self, audio_bytes: bytes) -> str:
        """Transcribe WAV audio to Spanish text.

        Args:
            audio_bytes: WAV audio data from the browser recorder.

        Returns:
            Transcribed Spanish text.
        """
        with io.BytesIO(audio_bytes) as audio_file:
            with sr.AudioFile(audio_file) as source:
                audio_data = self.recognizer.record(source)

        return self.recognizer.recognize_google(audio_data, language="es-ES")

    # ----- Nova 2 Sonic bidirectional streaming ----- #

    def create_session_config(self, system_prompt: str) -> dict:
        """Create the session configuration for Nova Sonic streaming."""
        return {
            "sessionConfiguration": {
                "instructionEvent": {
                    "content": {
                        "text": system_prompt,
                    }
                },
                "inputAudioConfiguration": {
                    "mediaType": "audio/pcm",
                    "sampleRateHertz": 16000,
                    "sampleSizeBits": 16,
                    "channelCount": 1,
                    "audioEndpointConfiguration": {
                        "voiceActivityDetection": {
                            "silenceDurationMillis": 500,
                        }
                    },
                },
                "outputAudioConfiguration": {
                    "mediaType": "audio/pcm",
                    "sampleRateHertz": 24000,
                    "sampleSizeBits": 16,
                    "channelCount": 1,
                    "voiceId": SONIC_VOICE_ID,
                },
            }
        }

    def start_stream(self, system_prompt: str):
        """Start a bidirectional streaming session with Nova Sonic."""
        session_config = self.create_session_config(system_prompt)
        response = self.client.invoke_model_with_bidirectional_stream(
            modelId=self.model_id,
            body=json.dumps(session_config),
        )
        return response


def get_teacher_system_prompt(target_language: str) -> str:
    """Build the system prompt for the teacher-facing voice agent."""
    return (
        f"Eres Chicham, un asistente educativo de voz que ayuda a profesores "
        f"a comunicarse con estudiantes que hablan {target_language}. "
        f"Escucha lo que dice el profesor en español, confirma que entendiste "
        f"el mensaje, y prepara la traducción. Habla siempre en español con "
        f"el profesor. Sé claro, paciente y culturalmente respetuoso."
    )
