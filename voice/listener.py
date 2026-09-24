import os
import sys
sys.path.append(r"D:\Jarvis")

from brain.router import classify_intent

# ==========================================
# CUDA DLL PATHS
# ==========================================

CUDA_PATHS = [
    r"D:\Jarvis\venv\Lib\site-packages\nvidia\cublas\bin",
    r"D:\Jarvis\venv\Lib\site-packages\nvidia\cudnn\bin",
    r"D:\Jarvis\venv\Lib\site-packages\nvidia\cuda_nvrtc\bin",
]

for path in CUDA_PATHS:
    if os.path.exists(path):
        os.add_dll_directory(path)
        os.environ["PATH"] = path + os.pathsep + os.environ["PATH"]


import queue
import time


sys.path.append(r"D:\Jarvis")

import numpy as np
import sounddevice as sd
import torch

from silero_vad import load_silero_vad
from faster_whisper import WhisperModel

from brain.core import process_command


# ==========================================
# CUDA DLL PATHS
# ==========================================

os.add_dll_directory(
    r"D:\Jarvis\venv\Lib\site-packages\nvidia\cublas\bin"
)

os.add_dll_directory(
    r"D:\Jarvis\venv\Lib\site-packages\nvidia\cudnn\bin"
)

os.add_dll_directory(
    r"D:\Jarvis\venv\Lib\site-packages\nvidia\cuda_nvrtc\bin"
)


# ==========================================
# CONFIGURATION
# ==========================================

SAMPLE_RATE = 16000
MICROPHONE = 1
CHUNK_SIZE = 512

SPEECH_THRESHOLD = 0.5

SILENCE_LIMIT = 3.0
MAX_RECORDING_TIME = 60.0

PRE_BUFFER_SECONDS = 0.5


# ==========================================
# LOAD MODELS
# ==========================================

print("Loading JARVIS VAD model...")

vad_model = load_silero_vad()

print("✅ VAD model ready!")

print("\nLoading JARVIS speech model...")

whisper_model = WhisperModel(
    "small",
    device="cuda",
    compute_type="int8_float16" 
)

print("✅ Whisper Small ready!")


# ==========================================
# AUDIO QUEUE
# ==========================================

audio_queue = queue.Queue()


def audio_callback(indata, frames, time_info, status):

    if status:
        print(status)

    audio_queue.put(indata.copy())


# ==========================================
# SMART LISTENER
# ==========================================

def listen():

    print("\n🤖 Waiting for speech...")

    recorded_audio = []

    pre_buffer = []

    recording = False

    speech_start_time = None
    last_speech_time = None

    max_pre_buffer_chunks = int(
        PRE_BUFFER_SECONDS * SAMPLE_RATE / CHUNK_SIZE
    )

    # Clear anything left in the queue
    while not audio_queue.empty():
        audio_queue.get_nowait()

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        blocksize=CHUNK_SIZE,
        channels=1,
        dtype="float32",
        device=MICROPHONE,
        callback=audio_callback
    ):

        while True:

            audio_chunk = audio_queue.get()

            audio = audio_chunk[:, 0]

            # ----------------------------------
            # PRE-BUFFER
            # ----------------------------------

            if not recording:

                pre_buffer.append(audio.copy())

                if len(pre_buffer) > max_pre_buffer_chunks:
                    pre_buffer.pop(0)

            # ----------------------------------
            # VAD
            # ----------------------------------

            tensor = torch.from_numpy(audio)

            speech_probability = vad_model(
                tensor,
                SAMPLE_RATE
            ).item()

            current_time = time.time()

            # ==================================
            # WAITING FOR SPEECH
            # ==================================

            if not recording:

                if speech_probability >= SPEECH_THRESHOLD:

                    recording = True

                    speech_start_time = current_time
                    last_speech_time = current_time

                    # Add pre-buffer so we don't lose
                    # the beginning of the sentence.
                    recorded_audio.extend(pre_buffer)

                    recorded_audio.append(audio.copy())

                    print("\n🎙️ Speech detected!")
                    print("🔴 Recording...")

                continue

            # ==================================
            # RECORDING
            # ==================================

            recorded_audio.append(audio.copy())

            # ----------------------------------
            # SPEECH DETECTED
            # ----------------------------------

            if speech_probability >= SPEECH_THRESHOLD:

                last_speech_time = current_time

            # ----------------------------------
            # SILENCE CHECK
            # ----------------------------------

            silence_duration = (
                current_time - last_speech_time
            )

            if silence_duration >= SILENCE_LIMIT:

                print("\n🤫 3 seconds of silence detected.")
                print("⏹️ Recording stopped.")

                break

            # ----------------------------------
            # MAXIMUM RECORDING TIME
            # ----------------------------------

            recording_duration = (
                current_time - speech_start_time
            )

            if recording_duration >= MAX_RECORDING_TIME:

                print("\n⏰ 60-second maximum reached.")
                print("⏹️ Recording stopped.")

                break

    if not recorded_audio:
        return None

    audio_data = np.concatenate(recorded_audio)

    return audio_data


# ==========================================
# WHISPER TRANSCRIPTION
# ==========================================

def transcribe(audio):

    print("\n🧠 Processing speech...")

    start_time = time.perf_counter()

    segments, info = whisper_model.transcribe(
        audio,
        beam_size=5
    )

    text = ""

    for segment in segments:
        text += segment.text

    elapsed = time.perf_counter() - start_time

    print(f"🌐 Detected language: {info.language}")
    print(f"📊 Language probability: {info.language_probability:.2f}")
    print(f"⏱️ Whisper processing: {elapsed:.2f} seconds")

    return text.strip()


# ==========================================
# MAIN JARVIS LISTENER
# ==========================================

if __name__ == "__main__":

    print("\n=================================")
    print("       JARVIS VOICE MODE 🤖")
    print("=================================")
    print("Speak naturally.")
    print("Say 'exit' to shut down.")
    print("=================================")

    while True:

        audio = listen()

        if audio is None:
            continue

        duration = len(audio) / SAMPLE_RATE

        print(f"📊 Captured: {duration:.2f} seconds")

        text = transcribe(audio)

        if not text:
            print("🤫 No speech recognized.")
            continue

        print(f"\n📝 You: {text}")

        command = (
            text
            .lower()
            .strip()
            .replace(".", "")
            .replace("!", "")
            .replace("?", "")
            .replace(",", "")
        )

        # ==============================
        # EXIT COMMAND
        # ==============================

        if any(
            word in command.split()
            for word in ["exit", "quit", "shutdown"]
        ):
            print("\n🤖 JARVIS: Goodbye, Boss.")
            break

        # ==============================
        # SEND TO JARVIS BRAIN
        # ==============================

        print("\n🧠 JARVIS is thinking...")

        reply = process_command(text)

        if reply and classify_intent(text) != "GENERAL":
         print(f"\n🤖 JARVIS: {reply}")


       