import queue
import time

import numpy as np
import sounddevice as sd
import torch
from silero_vad import load_silero_vad


# ==============================
# JARVIS VAD CONFIGURATION
# ==============================

SAMPLE_RATE = 16000
MICROPHONE = 1

CHUNK_SIZE = 512

SILENCE_LIMIT = 3.0
MAX_RECORDING_TIME = 60.0

SPEECH_THRESHOLD = 0.5


# ==============================
# LOAD VAD MODEL
# ==============================

print("Loading JARVIS VAD model...")

vad_model = load_silero_vad()

print("VAD model ready!")


# ==============================
# AUDIO QUEUE
# ==============================

audio_queue = queue.Queue()


def audio_callback(indata, frames, time_info, status):

    if status:
        print(status)

    audio_queue.put(indata.copy())


# ==============================
# SMART LISTENER
# ==============================

def listen_until_silence():

    print("\nWaiting for speech...")

    recording = False
    recorded_audio = []

    speech_start_time = None
    last_speech_time = None

    # Clear any old audio before starting
    while not audio_queue.empty():

        try:
            audio_queue.get_nowait()
        except queue.Empty:
            break

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

            tensor = torch.from_numpy(audio)

            speech_probability = vad_model(
                tensor,
                SAMPLE_RATE
            ).item()

            current_time = time.time()

            # ==========================
            # WAITING FOR SPEECH
            # ==========================

            if not recording:

                if speech_probability >= SPEECH_THRESHOLD:

                    recording = True

                    speech_start_time = current_time
                    last_speech_time = current_time

                    recorded_audio.append(audio.copy())

                    print("\nSpeech detected!")
                    print("Recording...")

                continue

            # ==========================
            # RECORDING
            # ==========================

            recorded_audio.append(audio.copy())

            # Speech detected
            if speech_probability >= SPEECH_THRESHOLD:

                last_speech_time = current_time

            # ==========================
            # CHECK SILENCE
            # ==========================

            silence_duration = (
                current_time - last_speech_time
            )

            if silence_duration >= SILENCE_LIMIT:

                print("\n3 seconds of silence detected.")
                print("Recording stopped.")

                break

            # ==========================
            # MAXIMUM RECORDING TIME
            # ==========================

            recording_duration = (
                current_time - speech_start_time
            )

            if recording_duration >= MAX_RECORDING_TIME:

                print("\nMaximum 60-second recording reached.")
                print("Recording stopped.")

                break

    # ==========================
    # RETURN AUDIO
    # ==========================

    if recorded_audio:

        audio_data = np.concatenate(recorded_audio)

        return audio_data

    return None


# ==============================
# STANDALONE VAD TEST
# ==============================

if __name__ == "__main__":

    while True:

        audio = listen_until_silence()

        if audio is None:
            continue

        duration = len(audio) / SAMPLE_RATE

        print(
            f"Captured audio: {duration:.2f} seconds"
        )

        print("\nReturning to listening...")

        time.sleep(0.5)