from pathlib import Path
import speech_recognition as sr
from pydub import AudioSegment

from files_managing import recursive_file_finder_and_creator

# Convert OGG to WAV (pydub handles it via ffmpeg)

all_sound_files = recursive_file_finder_and_creator(path=Path("/home/jrojo/Descargas/whatsapp_files"))

for sound_file in all_sound_files:
    sound = AudioSegment.from_ogg(sound_file)
    sound.export(f"./tmp_wavs/{sound_file.stem}.wav", format="wav")

    r = sr.Recognizer()
    with sr.AudioFile(f"./tmp_wavs/{sound_file.stem}.wav") as source:
        audio = r.record(source)

    try:
        print("Transcription:")
        transcription = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"API error: {e}")

    with open(f"./tmp_transcribed_file/{sound_file.stem}.txt", "w") as f:
        f.write(transcription)
