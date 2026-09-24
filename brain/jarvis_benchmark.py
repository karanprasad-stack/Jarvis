import time
import os
from openai import OpenAI


client = OpenAI(
    base_url="http://localhost:20128/v1",
    api_key=os.getenv("OMNIROUTE_API_KEY")
)


MODELS = [
    "oc/ling-3.0-flash-fin-free",
    "oc/laguna-s-2.1-free",
    "oc/mimo-v2.5-free",
]


TESTS = [
    ("English", "What's my name?"),
    ("Reasoning", "Why is the sky blue? Explain briefly."),
    ("Hindi", "क्या तुम हिंदी समझ सकते हो?"),
    ("Hinglish", "Bhai kal mujhe college jaana hai, subah kitne baje uthna chahiye?"),
    ("JARVIS", "You are my AI assistant. Tell me briefly what you can do for me."),
]


SYSTEM_PROMPT = (
    "You are JARVIS, a fast voice assistant. "
    "Be helpful, natural, and concise. "
    "For normal questions, answer in 1-3 sentences. "
    "Do not over-explain unless asked."
)


print("\n==============================================")
print("       JARVIS REAL-WORLD MODEL TEST 🤖")
print("==============================================\n")


all_results = []


for model in MODELS:

    print(f"\n{'=' * 46}")
    print(f"MODEL: {model}")
    print(f"{'=' * 46}")

    model_results = []

    for test_name, prompt in TESTS:

        print(f"\n🧪 {test_name}")
        print(f"📝 {prompt}")

        start = time.perf_counter()
        first_token = None
        reply = ""

        try:

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                stream=True
            )

            for chunk in response:

                if not chunk.choices:
                    continue

                delta = chunk.choices[0].delta.content

                if delta:

                    if first_token is None:
                        first_token = time.perf_counter() - start

                    reply += delta

            total = time.perf_counter() - start

            print(f"⚡ First token: {first_token:.2f}s")
            print(f"⏱️ Total:       {total:.2f}s")
            print(f"🤖 Response:    {reply.strip()}")

            model_results.append({
                "test": test_name,
                "first": first_token,
                "total": total,
                "reply": reply.strip()
            })

        except Exception as e:

            print(f"❌ ERROR: {e}")

            model_results.append({
                "test": test_name,
                "first": None,
                "total": None,
                "reply": f"ERROR: {e}"
            })

    all_results.append({
        "model": model,
        "results": model_results
    })


print("\n\n==============================================")
print("              SPEED SUMMARY 🏆")
print("==============================================\n")

print(
    f"{'MODEL':<40}"
    f"{'AVG FIRST':>12}"
    f"{'AVG TOTAL':>12}"
)

print("-" * 66)


for item in all_results:

    valid = [
        r for r in item["results"]
        if r["first"] is not None
    ]

    if not valid:
        continue

    avg_first = sum(r["first"] for r in valid) / len(valid)
    avg_total = sum(r["total"] for r in valid) / len(valid)

    print(
        f"{item['model']:<40}"
        f"{avg_first:>10.2f}s"
        f"{avg_total:>10.2f}s"
    )


print("\n==============================================")
print("             TEST COMPLETE 🤖")
print("==============================================")