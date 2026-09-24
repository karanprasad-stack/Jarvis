from openai import OpenAI
import os


client = OpenAI(
    base_url="http://localhost:20128/v1",
    api_key=os.getenv("OMNIROUTE_API_KEY")
)


messages = [
    {
        "role": "system",
        "content": (
            "You are JARVIS, a fast personal voice assistant. "
            "Your name is JARVIS. "
            "Be natural, helpful, and concise. "
            "Keep normal answers to 1-3 short sentences. "
            "For simple questions, answer in one sentence. "
            "Do not over-explain unless the user asks. "
            "Match the user's language. "
            "If the user speaks Hindi or Hinglish, respond naturally in Hindi or Hinglish."
        )
    }
]


def ask_jarvis(user_input):

    messages.append({
        "role": "user",
        "content": user_input
    })

    try:

        response = client.chat.completions.create(
            model="oc/ling-3.0-flash-fin-free",
            messages=messages,
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

        messages.append({
            "role": "assistant",
            "content": reply
        })

        return reply

    except Exception as e:

        return f"JARVIS ERROR: {e}"