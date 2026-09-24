import time
from collections import deque

import numpy as np
import sounddevice as sd

from openwakeword.model import Model


# =========================
# CONFIGURATION
# =========================

SAMPLE_RATE = 16000
MICROPHONE = 1
CHUNK_SIZE = 1280

# Software microphone gain
MIC_GAIN = 3.0

# Wake-word sensitivity
WAKE_THRESHOLD = 0.20

# Number of recent prediction scores to remember
WINDOW_SIZE = 5

# Prevent repeated detections
COOLDOWN = 2.0


# =========================
# LOAD MODEL
# =========================

print("Loading JARVIS wake-word model...")

wake_model = Model(
    wakeword_models=["hey_jarvis"]
)

print("✅ Wake-word model ready!")


# =========================
# VARIABLES
# =========================

last_detection_time = 0
highest_score = 0.0
last_score_print = time.time()

score_history = deque(maxlen=WINDOW_SIZE)


# =========================
# AUDIO CALLBACK
# =========================

def audio_callback(indata, frames, time_info, status):

    global last_detection_time
    global highest_score
    global last_score_print

    if status:
        print("Audio status:", status)

    # ---------------------------------
    # Read microphone audio
    # ---------------------------------

    audio = indata[:, 0].astype(np.float32)

    # ---------------------------------
    # Apply software gain
    # ---------------------------------

    audio = audio * MIC_GAIN

    # ---------------------------------
    # Check for clipping
    # ---------------------------------

    clipped_samples = np.sum(np.abs(audio) > 32767)

    if clipped_samples > 0:
        print(
            f"⚠️ Clipping detected: "
            f"{clipped_samples} samples"
        )

    # ---------------------------------
    # Prevent values outside int16 range
    # ---------------------------------

    audio = np.clip(audio, -32768, 32767)

    # ---------------------------------
    # Convert back to int16
    # ---------------------------------

    audio = audio.astype(np.int16)

    # ---------------------------------
    # Wake-word prediction
    # ---------------------------------

    prediction = wake_model.predict(audio)

    score = float(
        prediction.get("hey_jarvis", 0.0)
    )

    # ---------------------------------
    # Store recent scores
    # ---------------------------------

    score_history.append(score)

    # Track global highest score
    if score > highest_score:
        highest_score = score

    # Highest score in recent window
    window_peak = max(score_history)

    # ---------------------------------
    # Display diagnostic information
    # ---------------------------------

    if time.time() - last_score_print >= 1:

        print(
            f"Current: {score:.3f} | "
            f"Window peak: {window_peak:.3f} | "
            f"Overall peak: {highest_score:.3f}"
        )

        last_score_print = time.time()

    # ---------------------------------
    # Wake detection
    # ---------------------------------

    current_time = time.time()

    if (
        window_peak >= WAKE_THRESHOLD
        and current_time - last_detection_time >= COOLDOWN
    ):

        print()
        print("🔥 ===============================")
        print("🔥 HEY JARVIS DETECTED!")
        print(f"🔥 Current score: {score:.3f}")
        print(f"🔥 Window peak:   {window_peak:.3f}")
        print(f"🔥 Overall peak:  {highest_score:.3f}")
        print("🔥 ===============================")
        print()

        last_detection_time = current_time

        # Clear the window so the same wake word
        # doesn't immediately trigger again.
        score_history.clear()


# =========================
# START MICROPHONE
# =========================

print()
print("========================================")
print("       JARVIS WAKE WORD TEST")
print("========================================")
print()
print("Say:")
print()
print("        Hey JARVIS")
print()
print("Speak naturally.")
print("Do NOT deliberately shout or speak slowly.")
print()
print("Try approximately 15 times.")
print("Wait about 2 seconds between attempts.")
print()
print(f"Microphone gain: {MIC_GAIN}x")
print(f"Wake threshold:  {WAKE_THRESHOLD}")
print(f"Score window:    {WINDOW_SIZE} frames")
print(f"Cooldown:        {COOLDOWN}s")
print()
print("Press Ctrl+C to stop.")
print("========================================")
print()


# =========================
# RUN
# =========================

try:

    with sd.InputStream(
        device=MICROPHONE,
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
        blocksize=CHUNK_SIZE,
        callback=audio_callback
    ):

        print("🎙️ Listening...")
        print()

        while True:
            time.sleep(0.1)


except KeyboardInterrupt:

    print()
    print("========================================")
    print("🛑 Test stopped.")
    print("========================================")
    print()
    print(f"🏆 Highest score: {highest_score:.3f}")
    print()