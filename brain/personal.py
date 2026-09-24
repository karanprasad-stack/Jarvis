from .memory import get_profile, get_preferences, get_facts


def handle_personal_query(text):
    text = text.lower().strip()

    profile = get_profile()
    preferences = get_preferences()
    facts = get_facts()

    # -------------------------
    # NAME
    # -------------------------

    if "my name" in text or "who am i" in text:
        name = profile.get("name")

        if name:
            return f"Your name is {name}."

        return "I don't have your name saved yet."

    # -------------------------
    # ASSISTANT NAME
    # -------------------------

    if "your name" in text or "who are you" in text:
        assistant_name = profile.get("assistant_name", "JARVIS")

        return f"My name is {assistant_name}."

    # -------------------------
    # LANGUAGES
    # -------------------------

    if (
        "language" in text
        or "languages" in text
        or "speak" in text
    ):
        languages = profile.get("preferred_languages", [])

        if languages:
            return "You prefer " + ", ".join(languages) + "."

    # -------------------------
    # PREFERENCES
    # -------------------------

    if "response style" in text:
        style = preferences.get("response_style")

        if style:
            return f"Your preferred response style is {style}."

    if "tone" in text:
        tone = preferences.get("preferred_tone")

        if tone:
            return f"Your preferred tone is {tone}."

    # -------------------------
    # SAVED FACTS
    # -------------------------

    if "favorite color" in text:
        color = facts.get("favorite_color")

        if color:
            return f"Your favorite color is {color}."

        return "You haven't told me your favorite color yet."

    # -------------------------
    # MEMORY SUMMARY
    # -------------------------

    if (
        "what do you remember" in text
        or "what do you know about me" in text
        or "about me" in text
    ):
        details = []

        if profile.get("name"):
            details.append(f"your name is {profile['name']}")

        if profile.get("preferred_languages"):
            languages = ", ".join(profile["preferred_languages"])
            details.append(f"you prefer {languages}")

        for key, value in facts.items():
            details.append(f"{key.replace('_', ' ')} is {value}")

        if details:
            return "I remember that " + ", ".join(details) + "."

        return "I don't have much personal information saved yet."

    # -------------------------
    # UNKNOWN PERSONAL QUERY
    # -------------------------

    return None