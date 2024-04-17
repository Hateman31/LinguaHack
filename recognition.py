import assemblyai as __aai
import config as __cfg


__aai.settings.api_key = __cfg.speech_recognition_token

__config = __aai.TranscriptionConfig(
    language_detection=False,
    language_code=__aai.LanguageCode.en
)

__transcriber = __aai.Transcriber(config=__config)


async def recognize(audio_file) -> str | None:
    """
    RECOGNIZE FUNCTION

    :param audio_file: file with audio to recognize
    :return:
    """
    result = __transcriber.transcribe(audio_file).text
    if result == "":
        return "empty_message"
    return result
