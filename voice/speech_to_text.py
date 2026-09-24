## BACKUP .............................

import os

os.add_dll_directory(
    r"D:\Jarvis\venv\Lib\site-packages\nvidia\cublas\bin"
)

os.add_dll_directory(
    r"D:\Jarvis\venv\Lib\site-packages\nvidia\cudnn\bin"
)

os.add_dll_directory(
    r"D:\Jarvis\venv\Lib\site-packages\nvidia\cuda_nvrtc\bin"
)

from faster_whisper import WhisperModel
import sounddevice as sd


SAMPLE_RATE = 16000
RECORD_SECONDS = 5
MICROPHONE = 1


print("Loading JARVIS speech model...")

model = WhisperModel(
    "base",
    device="cuda",
    compute_type="int8_float16"
)

print("✅ Speech model ready!")


def listen():
    print("\n🎙️ Listening...")

    audio = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        device=MICROPHONE
    )

    sd.wait()

    audio = audio.flatten()

    segments, info = model.transcribe(
        audio,
    )

    text = ""

    for segment in segments:
        text += segment.text

    return text.strip()


if __name__ == "__main__":

    while True:

     text = listen()

     if text:
        print(f"📝 You: {text}")

     command = text.lower().strip().replace(".", "").replace("!", "").replace("?", "")

     if command in ["exit", "quit", "shutdown"]:
        print("JARVIS: Goodbye, Boss.")
        break