import assemblyai as __aai
import config as __cfg


__aai.settings.api_key = __cfg.speech_recognition_token

__config = __aai.TranscriptionConfig(
    language_detection=False,
    language_code="ru"
)

__transcriber = __aai.Transcriber(config=__config)


def recognize(audio_file):
    result = __transcriber.transcribe(audio_file).text
    return result
