from router import classify_intent
from personal import handle_personal_query


commands = [
    "What's my name?",
    "Who am I?",
    "What is your name?",
    "What languages do I prefer?",
    "What is my favorite color?",
    "What do you remember about me?"
]


print("\n========== JARVIS PERSONAL PIPELINE ==========\n")

for command in commands:

    intent = classify_intent(command)

    print(f"User   : {command}")
    print(f"Intent : {intent}")

    if intent == "PERSONAL":
        response = handle_personal_query(command)
        print(f"JARVIS : {response}")
    else:
        print("JARVIS : Router did not classify this as PERSONAL.")

    print("-" * 50)