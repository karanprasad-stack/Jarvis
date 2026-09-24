from google import genai
import os
import time

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

for i in range(3):

    print(f"\n===== TEST {i + 1} =====")

    start = time.perf_counter()
    first_token = None
    reply = ""

    stream = client.interactions.create(
        model="gemini-3.6-flash",
        input="Say hello to JARVIS in one short sentence.",
        generation_config={
            "thinking_level": "minimal"
        },
        stream=True
    )

    for event in stream:

        if getattr(event, "event_type", None) != "step.delta":
            continue

        delta = getattr(event, "delta", None)

        if delta is None:
            continue

        text = getattr(delta, "text", None)

        if text:

            if first_token is None:
                first_token = time.perf_counter() - start

            reply += text

    total = time.perf_counter() - start

    print("Response:", reply)
    print(f"First token: {first_token:.2f}s")
    print(f"Total:       {total:.2f}s")