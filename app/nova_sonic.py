"""Voice client — Amazon Transcribe for STT, Nova 2 Sonic for conversation."""

import asyncio
import concurrent.futures
import io
import json
import wave

import boto3

from app.config import AWS_REGION, NOVA_SONIC_MODEL_ID, SONIC_VOICE_ID


async def _transcribe_streaming(pcm_bytes: bytes, sample_rate: int) -> str:
    """Run Amazon Transcribe Streaming and return the final transcript."""
    from amazon_transcribe.client import TranscribeStreamingClient
    from amazon_transcribe.handlers import TranscriptResultStreamHandler
    from amazon_transcribe.model import TranscriptEvent

    class _Handler(TranscriptResultStreamHandler):
        def __init__(self, stream):
            super().__init__(stream)
            self.transcripts = []

        async def handle_transcript_event(self, event: TranscriptEvent):
            for result in event.transcript.results:
                if not result.is_partial:
                    for alt in result.alternatives:
                        self.transcripts.append(alt.transcript)

    client = TranscribeStreamingClient(region=AWS_REGION)
    stream = await client.start_stream_transcription(
        language_code="es-ES",
        media_sample_rate_hz=sample_rate,
        media_encoding="pcm",
    )

    # Send audio in ~1-second chunks
    chunk_size = sample_rate * 2  # 16-bit = 2 bytes per sample
    for i in range(0, len(pcm_bytes), chunk_size):
        await stream.input_stream.send_audio_event(
            audio_chunk=pcm_bytes[i : i + chunk_size]
        )
    await stream.input_stream.end_stream()

    handler = _Handler(stream.output_stream)
    await handler.handle_events()

    return " ".join(handler.transcripts)


class NovaSonicClient:
    """Voice interface: Amazon Transcribe for STT, Nova 2 Sonic for streaming."""

    def __init__(self):
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=AWS_REGION,
        )
        self.model_id = NOVA_SONIC_MODEL_ID

    # ----- Speech-to-text (Amazon Transcribe Streaming) ----- #

    def transcribe_audio(self, audio_bytes: bytes) -> str:
        """Transcribe WAV audio to Spanish text.

        Uses Amazon Transcribe Streaming for reliable real-time
        speech-to-text in Spanish.

        Args:
            audio_bytes: WAV audio data from the browser recorder.

        Returns:
            Transcribed Spanish text.
        """
        pcm_bytes, sample_rate = self._wav_to_pcm(audio_bytes)

        if not pcm_bytes:
            return ""

        # Run the async transcription — safe inside Streamlit threads
        try:
            asyncio.get_running_loop()
            # Already inside an event loop → delegate to a thread
            with concurrent.futures.ThreadPoolExecutor() as pool:
                return pool.submit(
                    asyncio.run,
                    _transcribe_streaming(pcm_bytes, sample_rate),
                ).result(timeout=30)
        except RuntimeError:
            # No running loop → just use asyncio.run
            return asyncio.run(
                _transcribe_streaming(pcm_bytes, sample_rate)
            )

    @staticmethod
    def _wav_to_pcm(wav_bytes: bytes) -> tuple:
        """Extract raw PCM data and sample rate from WAV bytes."""
        try:
            with io.BytesIO(wav_bytes) as buf:
                with wave.open(buf, "rb") as wav:
                    pcm_data = wav.readframes(wav.getnframes())
                    sample_rate = wav.getframerate()
            return pcm_data, sample_rate
        except Exception:
            # If not a valid WAV, treat as raw PCM at 16 kHz
            return wav_bytes, 16000

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
