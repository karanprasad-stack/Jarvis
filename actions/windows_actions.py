import os
import subprocess
import webbrowser


APP_PATHS = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "vscode": r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe"
}


WEBSITES = {
    "whatsapp": "https://web.whatsapp.com",
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "github": "https://github.com"
}


def open_application(app_name):
    app_name = app_name.lower().strip()

    if app_name == "chrome":
        path = os.path.expandvars(APP_PATHS["chrome"])

        if os.path.exists(path):
            subprocess.Popen([path])
            return "Opening Chrome."

        return "I couldn't find Chrome at the expected location."

    if app_name in ["vscode", "vs code"]:
        path = os.path.expandvars(APP_PATHS["vscode"])

        if os.path.exists(path):
            subprocess.Popen([path])
            return "Opening VS Code."

        return "I couldn't find VS Code at the expected location."

    return None


def open_website(site_name):
    site_name = site_name.lower().strip()

    if site_name in WEBSITES:
        webbrowser.open(WEBSITES[site_name])
        return f"Opening {site_name}."

    return None


def handle_action(text):
    text = text.lower().strip()

    # -------------------------
    # WHATSAPP
    # -------------------------

    if "whatsapp" in text:
        return open_website("whatsapp")

    # -------------------------
    # YOUTUBE
    # -------------------------

    if "youtube" in text:
        return open_website("youtube")

    # -------------------------
    # GOOGLE
    # -------------------------

    if "google" in text:
        return open_website("google")

    # -------------------------
    # GITHUB
    # -------------------------

    if "github" in text:
        return open_website("github")

    # -------------------------
    # CHROME
    # -------------------------

    if "chrome" in text:
        return open_application("chrome")

    # -------------------------
    # VS CODE
    # -------------------------

    if "vscode" in text or "vs code" in text:
        return open_application("vscode")

    return None