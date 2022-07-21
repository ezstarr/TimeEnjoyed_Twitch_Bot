import speech_recognition as sr


# This file will listen to the mic
# Whenever it hears/returns a KEYWORD
# Trigger a function

r = sr.Recognizer()
mic = sr.Microphone()

# print(sr.Microphone.list_microphone_names())
print(r)
print(mic)

with mic as source:
    audio = r.listen(source)
    print(audio)