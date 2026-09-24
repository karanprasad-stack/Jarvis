import os
import sys
import time
import threading

import numpy as np
import sounddevice as sd
import soundfile as sf
from openwakeword.model import Model
from faster_whisper import WhisperModel


# ==========================================
# PROJECT PATH
# ==========================================

sys.path.append(r"D:\Jarvis")


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

        os.environ["PATH"] = (
            path
            + os.pathsep
            + os.environ["PATH"]
        )


# ==========================================
# JARVIS IMPORTS
# ==========================================

from voice.vad import listen_until_silence
from brain.router import classify_intent
from brain.core import process_command


# ==========================================
# CONFIGURATION
# ==========================================

SAMPLE_RATE = 16000

MICROPHONE = 1

# Wake-word audio frame
CHUNK_SIZE = 1280


# Locked wake-word configuration
MIC_GAIN = 3.0

WAKE_THRESHOLD = 0.20

WINDOW_SIZE = 5

COOLDOWN = 2.0


# Whisper configuration
WHISPER_MODEL = "small"


# Temporary command audio
AUDIO_PATH = r"D:\Jarvis\voice\temp_command.wav"


# ==========================================
# LOAD WAKE WORD MODEL
# ==========================================

print("\nLoading JARVIS wake-word model...")

wake_model = Model(
    wakeword_models=["hey_jarvis"]
)

print("Wake-word model ready!")


# ==========================================
# LOAD WHISPER
# ==========================================

print("\nLoading JARVIS speech model...")

whisper_model = WhisperModel(
    WHISPER_MODEL,
    device="cuda",
    compute_type="int8_float16"
)

print("Whisper Small ready!")


# ==========================================
# WAKE-WORD STATE
# ==========================================

score_history = []

last_detection_time = 0


# ==========================================
# WAKE-WORD DETECTOR
# ==========================================

def wait_for_wake_word():

    global last_detection_time

    detected_event = threading.Event()

    # Clear previous scores
    score_history.clear()

    print()
    print("========================================")
    print("        JARVIS IS LISTENING")
    print("========================================")
    print("Say: Hey JARVIS")
    print()

    def callback(indata, frames, time_info, status):

        global last_detection_time

        if status:

            print("Audio status:", status)

        # ----------------------------------
        # Read microphone
        # ----------------------------------

        audio = indata[:, 0].astype(
            np.float32
        )

        # ----------------------------------
        # Apply microphone gain
        # ----------------------------------

        audio = audio * MIC_GAIN

        # ----------------------------------
        # Prevent clipping
        # ----------------------------------

        audio = np.clip(
            audio,
            -1.0,
            1.0
        )

        # ----------------------------------
        # Convert to int16
        # ----------------------------------

        audio = (
            audio * 32767
        ).astype(np.int16)

        # ----------------------------------
        # Wake-word prediction
        # ----------------------------------

        prediction = wake_model.predict(
            audio
        )

        score = float(
            prediction.get(
                "hey_jarvis",
                0.0
            )
        )

        # ----------------------------------
        # Rolling score window
        # ----------------------------------

        score_history.append(score)

        if len(score_history) > WINDOW_SIZE:

            score_history.pop(0)

        window_peak = max(
            score_history
        )

        # ----------------------------------
        # Detection cooldown
        # ----------------------------------

        current_time = time.time()

        if (
            window_peak >= WAKE_THRESHOLD
            and
            current_time - last_detection_time
            >= COOLDOWN
        ):

            last_detection_time = (
                current_time
            )

            print(
                f"\nWake score: "
                f"{window_peak:.3f}"
            )

            # Clear old scores
            score_history.clear()

            # Signal detection
            detected_event.set()

    # ======================================
    # OPEN MICROPHONE
    # ======================================

    with sd.InputStream(

        device=MICROPHONE,

        samplerate=SAMPLE_RATE,

        channels=1,

        dtype="int16",

        blocksize=CHUNK_SIZE,

        callback=callback

    ):

        while not detected_event.is_set():

            time.sleep(0.05)

    return True


# ==========================================
# WHISPER TRANSCRIPTION
# ==========================================

def transcribe(audio):

    print("\nProcessing speech...")

    start_time = time.perf_counter()

    # --------------------------------------
    # Whisper
    # --------------------------------------

    segments, info = whisper_model.transcribe(

        audio,

        beam_size=5

    )

    text = ""

    for segment in segments:

        text += segment.text

    elapsed = (
        time.perf_counter()
        - start_time
    )

    # --------------------------------------
    # Diagnostics
    # --------------------------------------

    print(
        f"Detected language: "
        f"{info.language}"
    )

    print(
        f"Language probability: "
        f"{info.language_probability:.2f}"
    )

    print(
        f"Whisper processing: "
        f"{elapsed:.2f} seconds"
    )

    return text.strip()


# ==========================================
# MAIN JARVIS LOOP
# ==========================================

def main():

    print("\n=================================")
    print("       JARVIS WAKE MODE")
    print("=================================")
    print("Say 'Hey JARVIS' to activate.")
    print("Say 'exit' after activation to shut down.")
    print("=================================")


    while True:

        # ==================================
        # WAIT FOR WAKE WORD
        # ==================================

        wait_for_wake_word()


        print()
        print("========================================")
        print("       HEY JARVIS DETECTED!")
        print("       JARVIS ACTIVATED")
        print("========================================")


        # ==================================
        # LISTEN FOR COMMAND
        # ==================================

        print("\nListening for your command...")

        audio = listen_until_silence()


        if audio is None:

            print(
                "No command detected."
            )

            continue


        # ==================================
        # AUDIO INFORMATION
        # ==================================

        duration = (
            len(audio)
            / SAMPLE_RATE
        )

        print(
            f"\nCaptured audio: "
            f"{duration:.2f} seconds"
        )


        # ==================================
        # SAVE TEMP AUDIO
        # ==================================

        try:

            sf.write(
                AUDIO_PATH,
                audio,
                SAMPLE_RATE
            )

        except Exception as error:

            print(
                f"Audio save error: "
                f"{error}"
            )


        # ==================================
        # WHISPER
        # ==================================

        text = transcribe(audio)


        if not text:

            print(
                "\nNo speech recognized."
            )

            continue


        # ==================================
        # SHOW USER COMMAND
        # ==================================

        print(
            f"\nYou: {text}"
        )


        # ==================================
        # NORMALIZE COMMAND
        # ==================================

        command = (

            text
            .lower()
            .strip()
            .replace(".", "")
            .replace("!", "")
            .replace("?", "")
            .replace(",", "")

        )


        # ==================================
        # EXIT COMMAND
        # ==================================

        if any(

            word in command.split()

            for word in [
                "exit",
                "quit",
                "shutdown"
            ]

        ):

            print(
                "\nJARVIS: Goodbye, Boss."
            )

            break


        # ==================================
        # JARVIS BRAIN
        # ==================================

        print(
            "\nJARVIS is thinking..."
        )


        reply = process_command(text)


        # ==================================
        # LOCAL RESPONSE DISPLAY
        # ==================================

        intent = classify_intent(text)


        # General LLM responses already
        # print themselves while streaming.

        if (
            reply
            and intent != "GENERAL"
        ):

            print(
                f"\nJARVIS: {reply}"
            )


        # ==================================
        # RETURN TO WAKE WORD MODE
        # ==================================

        print(
            "\nReturning to wake-word mode..."
        )


# ==========================================
# ENTRY POINT
# ==========================================

if __name__ == "__main__":

    main()