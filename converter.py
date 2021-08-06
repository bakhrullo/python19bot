import subprocess
from gtts import gTTS
import speech_recognition as sr
from aiogram.types import Message
from pydub import AudioSegment
from aiogram.types import InputFile
import pathlib
def text_to_mp3(txt, name):
    text = txt
    language = "en"
    speech = gTTS(text = text, lang = language, slow = False)
    speech.save(name)

def mp3_to_text(name, id):
    # convert mp3 file to wav
    src = name
    dst = id + '.wav'
    subprocess.call(['ffmpeg', '-i', src,
                     dst])
    filename = dst
    # initialize the recognizer
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        try:
            text = r.recognize_google(audio_data)
        except:
            return "Sorry, but i dont understund you?"

        file_delete = pathlib.Path(str(dst))
        file_delete.unlink()
        return text
