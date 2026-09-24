from router import classify_intent


test_commands = [
    "What's my name?",
    "Who am I?",
    "What do you remember about me?",
    "What is my favorite color?",
    "What time is it?",
    "What's today's date?",
    "What is my battery level?",
    "Open WhatsApp",
    "Launch Chrome",
    "Open VS Code",
    "Restart my computer",
    "Explain blockchain",
    "Why is the sky blue?",
    "Tell me a joke",
    "How does AI work?"
]


print("\n========== JARVIS ROUTER TEST ==========\n")

for command in test_commands:
    intent = classify_intent(command)

    print(f"Command : {command}")
    print(f"Intent  : {intent}")
    print("-" * 45)