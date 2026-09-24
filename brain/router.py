def classify_intent(text):
    """
    Classifies a user command without using an LLM.

    Returns:
        PERSONAL  -> Personal memory/profile
        SYSTEM    -> System information
        ACTION    -> Computer/app actions
        GENERAL   -> General AI/LLM request
    """

    text = text.lower().strip()

    # -------------------------
    # PERSONAL MEMORY
    # -------------------------

    personal_keywords = [
    "my name",
    "who am i",
    "about me",
    "know about me",
    "my favorite",
    "my preference",
    "my preferences",
    "what do you remember",
    "remember about me",
    "my details",

    # Assistant identity
    "your name",
    "who are you",

    # Personal languages
    "my language",
    "my languages",
    "languages do i prefer",
    "language do i prefer",
    "what languages do i prefer"
]

    if any(keyword in text for keyword in personal_keywords):
        return "PERSONAL"

    # -------------------------
    # SYSTEM INFORMATION
    # -------------------------

    system_keywords = [
    "what time",
    "current time",
    "time is it",
    "what's the time",
    "whats the time",
    "what is the time",
    "what's the time it is",
    "whats the time it is",
    "what is the time it is",
    "tell me the time",
    "current date",
    "what date",
    "today's date",
    "todays date",
    "what day is it",
    "today",
    "battery",
    "battery level",
    "system information",
    "system info"
]
    

    if any(keyword in text for keyword in system_keywords):
        return "SYSTEM"

    # -------------------------
    # COMPUTER / APP ACTIONS
    # -------------------------

    action_keywords = [
        "open ",
        "close ",
        "launch ",
        "start ",
        "run ",
        "shutdown",
        "restart",
        "lock my pc",
        "lock computer",
        "open whatsapp",
        "open chrome",
        "open browser",
        "open vscode",
        "open vs code"
    ]

    if any(keyword in text for keyword in action_keywords):
        return "ACTION"

    provider_keywords = [
       "switch to gemini",
       "use gemini",
       "switch to omniroute",
       "use omniroute",
       "which ai are you using",
       "which ai are you using right now"
    ]

    if any(keyword in text for keyword in provider_keywords):
     return "LLM_PROVIDER"

    # -------------------------
    # DEFAULT
    # -------------------------

    return "GENERAL"


def route_command(text):
    """
    Returns both the detected intent and original command.
    """

    intent = classify_intent(text)

    return {
        "intent": intent,
        "text": text
    }