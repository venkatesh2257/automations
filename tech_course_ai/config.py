import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
CURRICULA_DIR = BASE_DIR / "curricula"
ASSETS_DIR = BASE_DIR / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"
AUDIO_DIR = BASE_DIR / "notebooklm_audio"
SOURCES_DIR = BASE_DIR / "notebooklm_sources"
BROLL_DIR = ASSETS_DIR / "broll"
OUTPUT_DIR = BASE_DIR / "output"
TEMP_DIR = BASE_DIR / "temp"

for directory in [CURRICULA_DIR, ASSETS_DIR, FONTS_DIR, AUDIO_DIR, SOURCES_DIR, BROLL_DIR, OUTPUT_DIR, TEMP_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Video Dimensions & Formatting
VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
VIDEO_FPS = 30

# Colors (16:9 Dark Mode + Glassmorphism HUD)
COLOR_BG = (13, 17, 23)
COLOR_CARD_BG = (22, 27, 34, 235)
COLOR_HEADER_BG = (30, 36, 46, 255)
COLOR_TEXT_PRIMARY = (240, 246, 252)
COLOR_TEXT_MUTED = (139, 148, 158)
COLOR_ACCENT_CYAN = (0, 229, 255)
COLOR_ACCENT_GREEN = (63, 185, 80)
COLOR_ACCENT_YELLOW = (227, 179, 65)
COLOR_ACCENT_RED = (248, 81, 73)
COLOR_ACCENT_PURPLE = (188, 140, 255)
COLOR_BORDER = (48, 54, 61)

# Load .env
env_file = BASE_DIR / ".env"
if env_file.exists():
    with open(env_file, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()

# OpenRouter Settings (DeepSeek R1 / DeepSeek V3 / Qwen)
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = "deepseek/deepseek-chat"

# Google Pro & Gemini Settings
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-3.6-flash"

# ElevenLabs Studio Voice Settings
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = "pNInz6obpgDQGcFmaJgB" # Adam
ELEVENLABS_VOICE_ID_SARAH = "EXAVITQu4vr4xnSDxMaL" # Sarah
ELEVENLABS_MODEL = "eleven_multilingual_v2"

# Real Video Settings
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")

