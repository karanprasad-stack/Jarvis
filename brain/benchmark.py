import time
import os
from openai import OpenAI


client = OpenAI(
    base_url="http://localhost:20128/v1",
    api_key=os.getenv("OMNIROUTE_API_KEY")
)


MODELS = [
    "oc/deepseek-v4-flash-free",
    "oc/nemotron-3.5-lightning-free",
    "oc/mimo-v2.5-free",
    "oc/ling-3.0-flash-fin-free",
    "oc/muse-spark-1.2-contributor-free",
    "oc/hy3-free",
    "oc/north-mini-code-free",
    "oc/nemotron-3-ultra-free",
    "oc/laguna-s-2.1-free",
]


PROMPT = "Say hello in one short sentence."


print("\n========================================")
print("       JARVIS MODEL SPEED TEST 🤖")
print("========================================")
print(f"Test prompt: {PROMPT}")
print()


results = []


for model in MODELS:

    print(f"🧪 Testing: {model}")

    start = time.perf_counter()

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are JARVIS, a fast voice assistant. "
                        "Keep responses extremely short."
                    )
                },
                {
                    "role": "user",
                    "content": PROMPT
                }
            ],
            stream=True
        )

        first_token_time = None
        full_response = ""

        for chunk in response:

            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta.content

            if delta:

                if first_token_time is None:
                    first_token_time = time.perf_counter() - start

                full_response += delta

        total_time = time.perf_counter() - start

        print(f"   ⚡ First token: {first_token_time:.2f}s")
        print(f"   ⏱️ Total:       {total_time:.2f}s")
        print(f"   🤖 Response:    {full_response.strip()}")
        print()

        results.append(
            (model, first_token_time, total_time)
        )

    except Exception as e:

        print(f"   ❌ ERROR: {e}")
        print()

        results.append(
            (model, None, None)
        )


print("\n========================================")
print("             RESULTS 🏆")
print("========================================")

valid_results = [
    r for r in results
    if r[1] is not None
]

valid_results.sort(key=lambda x: x[1])


print(
    f"{'MODEL':<42}"
    f"{'FIRST':>10}"
    f"{'TOTAL':>10}"
)

print("-" * 62)

for model, first, total in valid_results:

    print(
        f"{model:<42}"
        f"{first:>9.2f}s"
        f"{total:>9.2f}s"
    )


print("\n🏆 FASTEST FIRST TOKEN:")

if valid_results:
    winner = valid_results[0]
    print(f"   {winner[0]}")
    print(f"   First token: {winner[1]:.2f}s")
    print(f"   Total:       {winner[2]:.2f}s")