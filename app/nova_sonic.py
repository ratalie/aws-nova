"""Nova 2 Sonic client for bidirectional Spanish voice streaming."""

import json
import boto3
from app.config import AWS_REGION, NOVA_SONIC_MODEL_ID, SONIC_VOICE_ID


class NovaSonicClient:
    """Handles speech-to-text and text-to-speech via Nova 2 Sonic.

    Nova 2 Sonic provides bidirectional streaming for real-time
    conversational AI. We use it for the Spanish voice interface,
    allowing teachers to speak naturally and receive spoken responses.
    """

    def __init__(self):
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=AWS_REGION,
        )
        self.model_id = NOVA_SONIC_MODEL_ID

    def create_session_config(self, system_prompt: str) -> dict:
        """Create the session configuration for Nova Sonic streaming.

        Args:
            system_prompt: Instructions for the voice agent's behavior.

        Returns:
            Session configuration dict for the bidirectional stream.
        """
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
        """Start a bidirectional streaming session with Nova Sonic.

        Args:
            system_prompt: The system instructions for the voice agent.

        Returns:
            The stream response object for sending/receiving audio events.
        """
        session_config = self.create_session_config(system_prompt)

        response = self.client.invoke_model_with_bidirectional_stream(
            modelId=self.model_id,
            body=json.dumps(session_config),
        )
        return response

    def transcribe_audio(self, audio_bytes: bytes) -> str:
        """Transcribe Spanish audio to text using Nova Sonic.

        For simpler use cases where we only need transcription,
        we use Nova Sonic in a single-turn mode.

        Args:
            audio_bytes: Raw PCM audio data (16kHz, 16-bit, mono).

        Returns:
            Transcribed Spanish text.
        """
        system_prompt = (
            "Eres un asistente de transcripción. Escucha el audio en español "
            "y transcríbelo exactamente. Solo devuelve el texto transcrito, "
            "sin comentarios adicionales."
        )

        session_config = self.create_session_config(system_prompt)
        session_config["inputAudio"] = {
            "content": audio_bytes,
            "mediaType": "audio/pcm",
        }

        response = self.client.invoke_model_with_bidirectional_stream(
            modelId=self.model_id,
            body=json.dumps(session_config),
        )

        transcription = ""
        for event in response["body"]:
            if "contentBlockDelta" in event:
                delta = event["contentBlockDelta"].get("delta", {})
                if "text" in delta:
                    transcription += delta["text"]

        return transcription.strip()

    def synthesize_speech(self, text: str) -> bytes:
        """Convert Spanish text to speech using Nova Sonic.

        Args:
            text: Spanish text to synthesize.

        Returns:
            Raw PCM audio data.
        """
        system_prompt = (
            "Lee el siguiente texto en español con una pronunciación "
            "clara y natural, como un profesor hablando con sus estudiantes."
        )

        session_config = self.create_session_config(system_prompt)
        session_config["textInput"] = {"text": text}

        response = self.client.invoke_model_with_bidirectional_stream(
            modelId=self.model_id,
            body=json.dumps(session_config),
        )

        audio_chunks = []
        for event in response["body"]:
            if "audioOutput" in event:
                audio_chunks.append(event["audioOutput"]["content"])

        return b"".join(audio_chunks)


def get_teacher_system_prompt(target_language: str) -> str:
    """Build the system prompt for the teacher-facing voice agent.

    Args:
        target_language: Name of the indigenous language being taught.

    Returns:
        System prompt string for Nova Sonic.
    """
    return (
        f"Eres Chicham, un asistente educativo de voz que ayuda a profesores "
        f"a comunicarse con estudiantes que hablan {target_language}. "
        f"Escucha lo que dice el profesor en español, confirma que entendiste "
        f"el mensaje, y prepara la traducción. Habla siempre en español con "
        f"el profesor. Sé claro, paciente y cultural mente respetuoso."
    )
