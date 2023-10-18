import speech_recognition as sr
from pathlib import Path
import asyncio
import json
from count_database import trigger_a_count

# This makes the directory that the module is loaded from as "source path"
source_path = Path(__file__).resolve()
source_dir = source_path.parent


recognizer = sr.Recognizer()
microphone = sr.Microphone()

print(sr.Microphone.list_microphone_names())

# TODO: While ON (make "on" command).
# TODO: End when off (make "off" command).



async def recognize_speech_from_mic(recognizer, microphone):

    """Transcribe speech from recorded from `microphone`.

    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone

    # audio_status = True

    hello = 0
    stop = 0
    with microphone as source:
        while True:
            recognizer.adjust_for_ambient_noise(source)
            audio = await recognizer.listen(source)

            response = {
                "success": True,
                "error": None,
                "transcription": None
                }

            try:
                response["transcription"] = recognizer.recognize_google(audio)
                if "hello" in response["transcription"].lower():
                    print(json.dumps(response))
                    hello += 1
                    sr_counts = trigger_a_count()
                    print(f"the number of hello's is {hello}")
                if "stop listening" in response["transcription"].lower():
                    print("it's stopping now")
                    break
            except sr.RequestError:
                # API was unreachable or unresponsive
                response["success"] = False
                response["error"] = "API unavailable"
            except sr.UnknownValueError:
                # speech was unintelligible
                response["error"] = "Unable to recognize speech"

            print(response)
            return(sr_counts)


recognize_speech_from_mic()

if __name__ == "__main__":
    recognize_speech_from_mic(recognizer, microphone)
print(__name__)