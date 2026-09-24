import json

from brain.gemini import ask_gemini
from brain.omniroute import ask_omniroute


SETTINGS_FILE = r"D:\Jarvis\config\settings.json"


def get_provider():

    try:

        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            settings = json.load(file)

        return settings.get("llm_provider", "gemini").lower()

    except (FileNotFoundError, json.JSONDecodeError):

        return "gemini"


def set_provider(provider):

    provider = provider.lower().strip()

    if provider not in ["gemini", "omniroute"]:
        return False

    try:

        with open(SETTINGS_FILE, "w", encoding="utf-8") as file:

            json.dump(
                {
                    "llm_provider": provider
                },
                file,
                indent=4
            )

        return True

    except Exception:

        return False


def get_provider_name():

    return get_provider().capitalize()


def ask_llm(prompt):

    provider = get_provider()

    # ==========================================
    # GEMINI PRIMARY
    # ==========================================

    if provider == "gemini":

        try:

            response = ask_gemini(prompt)

            if response and response.strip():
                return response

            print("\n⚠️ Gemini returned an empty response.")
            print("🔄 Switching to OmniRoute...")

        except Exception as error:

            print(f"\n⚠️ Gemini failed: {error}")
            print("🔄 Switching to OmniRoute...")

        # ==========================================
        # OMNIROUTE FALLBACK
        # ==========================================

        try:

            return ask_omniroute(prompt)

        except Exception as error:

            return (
                "I'm sorry, both Gemini and OmniRoute "
                f"are currently unavailable. Error: {error}"
            )

    # ==========================================
    # OMNIROUTE DIRECT
    # ==========================================

    if provider == "omniroute":

        try:

            return ask_omniroute(prompt)

        except Exception as error:

            return (
                "OmniRoute is currently unavailable. "
                f"Error: {error}"
            )

    return "I couldn't determine which AI provider to use."