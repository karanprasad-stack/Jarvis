from google import genai
from google.genai import types
import os


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set.")


# Gemini timeout: 8 seconds
client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(
        timeout=8000
    )
)


def ask_gemini(prompt):

    stream = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
        generation_config={
            "thinking_level": "minimal"
        },
        stream=True
    )

    reply = ""

    print("\n🤖 JARVIS: ", end="", flush=True)

    try:

        for event in stream:

            if getattr(event, "event_type", None) != "step.delta":
                continue

            delta = getattr(event, "delta", None)

            if delta is None:
                continue

            text = getattr(delta, "text", None)

            if text:
                print(text, end="", flush=True)
                reply += text

    except Exception as error:

        error_message = str(error).lower()

        if "timed out" in error_message and reply.strip():
            print()
            return reply

        raise

    print()

    return reply