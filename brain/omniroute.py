from openai import OpenAI
import os

client = OpenAI(
    base_url="http://localhost:20128/v1",
    api_key=os.getenv("OMNIROUTE_API_KEY")
)


def ask_omniroute(prompt):
    response = client.chat.completions.create(
        model="auto",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are JARVIS, a fast personal AI assistant. "
                    "Be helpful, natural, and concise. "
                    "For normal questions, answer in 1-3 sentences."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        stream=True
    )

    reply = ""

    print("\n🤖 JARVIS: ", end="", flush=True)

    for chunk in response:

        if not chunk.choices:
            continue

        delta = chunk.choices[0].delta.content

        if delta:
            print(delta, end="", flush=True)
            reply += delta

    print()

    return reply