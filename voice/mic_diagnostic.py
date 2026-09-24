import time
import numpy as np
import sounddevice as sd


SAMPLE_RATE = 16000
MICROPHONE = 1
CHUNK_SIZE = 1280


print("========================================")
print("       JARVIS MICROPHONE DIAGNOSTIC")
print("========================================")
print()
print(f"Microphone: {MICROPHONE}")
print(f"Sample rate: {SAMPLE_RATE} Hz")
print()
print("First stay SILENT for about 5 seconds.")
print("Then say:")
print()
print("        Hey JARVIS")
print()
print("normally 5 times.")
print()
print("Then say it slowly/loudly 5 times.")
print()
print("Press Ctrl+C when finished.")
print("========================================")
print()


last_print = time.time()


def audio_callback(indata, frames, time_info, status):
    global last_print

    if status:
        print("Audio status:", status)

    audio = indata[:, 0].astype(np.float32)

    # Normalize int16 audio to -1.0 ... +1.0
    audio = audio / 32768.0

    # RMS = average signal energy
    rms = np.sqrt(np.mean(audio ** 2))

    # Peak = loudest sample
    peak = np.max(np.abs(audio))

    # Convert RMS to approximate dBFS
    if rms > 0:
        db = 20 * np.log10(rms)
    else:
        db = -100

    if time.time() - last_print >= 0.5:
        print(
            f"RMS: {rms:.4f} | "
            f"Peak: {peak:.4f} | "
            f"Level: {db:.1f} dBFS"
        )

        last_print = time.time()


try:

    with sd.InputStream(
        device=MICROPHONE,
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
        blocksize=CHUNK_SIZE,
        callback=audio_callback
    ):

        print("🎙️ Microphone listening...")
        print()

        while True:
            time.sleep(0.1)


except KeyboardInterrupt:

    print()
    print("🛑 Diagnostic stopped.")