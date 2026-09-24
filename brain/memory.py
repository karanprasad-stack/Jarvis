import json
import os


BASE_DIR = r"D:\Jarvis\memory"

PROFILE_FILE = os.path.join(BASE_DIR, "profile.json")
PREFERENCES_FILE = os.path.join(BASE_DIR, "preferences.json")
FACTS_FILE = os.path.join(BASE_DIR, "facts.json")
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")


def load_json(file_path, default):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def get_profile():
    return load_json(PROFILE_FILE, {})


def get_preferences():
    return load_json(PREFERENCES_FILE, {})


def get_facts():
    return load_json(FACTS_FILE, {})


def get_fact(key):
    facts = get_facts()
    return facts.get(key)


def remember_fact(key, value):
    facts = get_facts()
    facts[key] = value
    save_json(FACTS_FILE, facts)


def add_history(user_input, response):
    history = load_json(HISTORY_FILE, [])

    history.append({
        "user": user_input,
        "jarvis": response
    })

    save_json(HISTORY_FILE, history)