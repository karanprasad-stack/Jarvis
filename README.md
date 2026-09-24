# 🤖 JARVIS - Voice-Activated AI Desktop Assistant

An intelligent, real-time voice-activated desktop assistant powered by local wake-word detection, deep-learning speech recognition, dynamic intent routing, and state-of-the-art LLMs (Google Gemini & OmniRoute).

---

## 🌟 Key Features

- **🎙️ Local Wake-Word Engine:** Powered by [openWakeWord](https://github.com/dscripka/openWakeWord) for ultra-low latency, private `"Hey JARVIS"` detection without sending audio to the cloud.
- **⚡ Voice Activity Detection (VAD):** Integrated with Silero VAD to detect pauses and end of user speech seamlessly.
- **🗣️ Fast Local Speech-to-Text:** Uses [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (CTranslate2) with optional GPU/CUDA acceleration for near-instant transcription.
- **🧠 Hybrid AI Brain & Intent Router:**
  - **Direct Actions:** Controls Windows apps (Chrome, VS Code), launches websites (WhatsApp, YouTube, GitHub, Google).
  - **System Queries:** Checks system time, date, battery status, and OS metrics.
  - **Personal Memory:** Long-term context storing facts, preferences, history, and user profile (`memory/*.json`).
  - **Conversational Intelligence:** Dynamic fallback and routing to **Google Gemini** or **OmniRoute** with streaming output.

---

## 📋 Prerequisites

- **Operating System:** Windows 10/11 (64-bit) recommended
- **Python:** Python 3.10 – 3.12+ (compatible with Python 3.14)
- **Audio Hardware:** Working microphone and speakers
- **GPU (Optional but recommended):** NVIDIA GPU with CUDA support for accelerated Whisper transcription

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/karanprasad-stack/Jarvis.git
cd Jarvis
```

### 2. Create a Virtual Environment

It is strongly recommended to use a clean virtual environment:

```bash
# Windows PowerShell / CMD
python -m venv venv

# Activate on PowerShell:
.\venv\Scripts\Activate.ps1

# Activate on Command Prompt (cmd):
.\venv\Scripts\activate.bat

# Activate on Bash / Linux:
source venv/bin/activate
```

> **Note for PowerShell Users:** If you encounter execution policy restrictions, run:
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> ```

### 3. (Optional) Install PyTorch with CUDA Support

If you have an NVIDIA GPU, install PyTorch with CUDA first:

```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu124
```

For CPU-only environments, standard PyTorch will be installed automatically with the requirements file.

### 4. Install Dependencies

Install all required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables Configuration

Set your AI provider API keys in your environment or terminal session:

### On Windows PowerShell:
```powershell
# Required for Gemini LLM
$env:GEMINI_API_KEY="your-gemini-api-key-here"

# (Optional) For OmniRoute provider
$env:OMNIROUTE_API_KEY="your-omniroute-api-key-here"

# (Optional) For higher HuggingFace model download limits
$env:HF_TOKEN="your-huggingface-token-here"
```

### On Windows Command Prompt:
```cmd
set GEMINI_API_KEY="your-gemini-api-key-here"
set OMNIROUTE_API_KEY="your-omniroute-api-key-here"
```

### Permanent Windows Setup (System Environment Variables):
1. Press `Win + R`, type `sysdm.cpl`, and press Enter.
2. Go to **Advanced** > **Environment Variables**.
3. Under User Variables, click **New** and add `GEMINI_API_KEY`.

---

## 🎤 Audio & Microphone Configuration

Before starting JARVIS, calibrate your microphone device index:

1. Run the microphone diagnostic tool:
   ```bash
   python voice/mic_diagnostic.py
   ```
2. Speak `"Hey JARVIS"` to verify input levels, RMS energy, and signal clarity.
3. If your microphone device is not default index `1`, update `MICROPHONE` in [`voice/wake_listener.py`](voice/wake_listener.py) and [`voice/mic_diagnostic.py`](voice/mic_diagnostic.py).

---

## 🎮 Running JARVIS

Start the assistant's voice loop:

```bash
python voice/wake_listener.py
```

### How to Interact:
1. Wait for `JARVIS IS LISTENING`.
2. Say **"Hey JARVIS"**.
3. Once prompted, speak your command or question:
   - *"What's the current time and battery level?"*
   - *"Open Chrome"* / *"Open VS Code"*
   - *"Open YouTube"* / *"Open WhatsApp"*
   - *"What is my name?"* / *"What is my favorite color?"*
   - *"Explain quantum computing in simple terms"*
   - *"Switch to Gemini"* / *"Switch to OmniRoute"*
   - *"Goodbye"* / *"Exit"* to terminate the session.

---

## 📁 Project Structure

```text
Jarvis/
├── actions/              # System automation and OS actions
│   ├── system_tools.py   # Battery, time, date, hardware metrics
│   └── windows_actions.py# App launching, browser actions
├── brain/                # AI logic & intent classification
│   ├── core.py           # Master query router & command dispatcher
│   ├── gemini.py         # Google Gemini integration
│   ├── llm.py            # Unified LLM provider switch
│   ├── memory.py         # Persistent JSON memory management
│   ├── omniroute.py      # OmniRoute integration
│   ├── personal.py       # Personal user queries handler
│   └── router.py         # Intent classification engine
├── config/
│   └── settings.json     # Configuration file (default LLM provider)
├── memory/               # Persistent storage for user profile & context
│   ├── facts.json
│   ├── history.json
│   ├── preferences.json
│   └── profile.json
├── voice/                # Audio input/output pipeline
│   ├── listener.py       # Speech recording & transcription
│   ├── mic_diagnostic.py # Audio input test & calibration
│   ├── speech_to_text.py # Whisper wrapper
│   ├── vad.py            # Silero Voice Activity Detector
│   └── wake_listener.py  # Main wake-word and interaction loop
├── .gitignore
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

---

## 🛠️ Troubleshooting

- **Wake word not triggering?**
  - Check the microphone gain in [`voice/wake_listener.py`](voice/wake_listener.py) (`MIC_GAIN`).
  - Lower `WAKE_THRESHOLD` from `0.20` to `0.15` if your microphone input is quiet.
- **CUDA DLL errors on Windows?**
  - Ensure you have NVIDIA CUDA Toolkit installed or ensure the virtual environment's nvidia packages (`nvidia-cublas-cu12`, etc.) are on your DLL search path.
  - If running on CPU only, change `device="cuda"` to `device="cpu"` in [`voice/wake_listener.py`](voice/wake_listener.py).

---

## 📄 License

This project is licensed under the MIT License.
