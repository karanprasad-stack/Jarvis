from brain.router import classify_intent
from brain.personal import handle_personal_query
from brain.llm import set_provider, get_provider_name, ask_llm

from actions.system_tools import (
    get_time,
    get_date,
    get_battery,
    get_system_info
)

from actions.windows_actions import handle_action


def handle_system_query(text):
    text = text.lower().strip()

    # -------------------------
    # TIME
    # -------------------------

    if (
    "what time" in text
    or "current time" in text
    or "time is it" in text
    or "what's the time" in text
    or "whats the time" in text
    or "what is the time" in text
    or "tell me the time" in text
):
     return f"The current time is {get_time()}."

    # -------------------------
    # DATE
    # -------------------------

    if (
        "today's date" in text
        or "todays date" in text
        or "what date" in text
        or "current date" in text
    ):
        return f"Today's date is {get_date()}."

    # -------------------------
    # BATTERY
    # -------------------------

    if (
        "battery" in text
        or "battery level" in text
    ):
        battery = get_battery()

        if isinstance(battery, int):
            return f"Your battery is at {battery}%."

        return battery

    # -------------------------
    # SYSTEM INFO
    # -------------------------

    if (
        "system information" in text
        or "system info" in text
    ):
        info = get_system_info()

        return (
            f"You are running {info['operating_system']} "
            f"{info['release']} on {info['machine']}."
        )

    return None


def process_command(text):
    """
    Main JARVIS command processor.
    Routes commands to the correct subsystem.
    """

    intent = classify_intent(text)

    # -------------------------
    # LLM PROVIDER
    # -------------------------

    if intent == "LLM_PROVIDER":

        text_lower = text.lower().strip()

        if "gemini" in text_lower:
            set_provider("gemini")
            return "Switched to Gemini."

        if "omniroute" in text_lower:
            set_provider("omniroute")
            return "Switched to OmniRoute."

        if "which ai" in text_lower:
            return f"I am currently using {get_provider_name()}."

        return "I couldn't determine the AI provider."

    # -------------------------
    # PERSONAL
    # -------------------------

    if intent == "PERSONAL":
        response = handle_personal_query(text)

        if response:
            return response

    # -------------------------
    # SYSTEM
    # -------------------------

    if intent == "SYSTEM":
        response = handle_system_query(text)

        if response:
            return response

    # -------------------------
    # ACTION
    # -------------------------

    if intent == "ACTION":
        response = handle_action(text)

        if response:
            return response

        return "I don't know how to perform that action yet."

    # -------------------------
    # GENERAL / FALLBACK
    # -------------------------

    return ask_llm(text)