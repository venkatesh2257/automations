import asyncio
import os
import requests
from pathlib import Path
from typing import List, Tuple
from config import ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID, ELEVENLABS_MODEL
import edge_tts

def synthesize_with_elevenlabs(text: str, output_audio_path: Path) -> bool:
    """
    Synthesizes ultra-realistic human voice using ElevenLabs API.
    """
    if not ELEVENLABS_API_KEY:
        return False
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": ELEVENLABS_MODEL,
        "voice_settings": {
            "stability": 0.50,
            "similarity_boost": 0.85,
            "style": 0.15,
            "use_speaker_boost": True
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=45)
        if response.status_code == 200:
            with open(output_audio_path, "wb") as f:
                f.write(response.content)
            return True
        else:
            print(f"[!] ElevenLabs error ({response.status_code}): {response.text}")
            return False
    except Exception as e:
        print(f"[!] ElevenLabs request exception: {e}")
        return False

async def synthesize_speech_edge(text: str, output_audio_path: Path) -> Path:
    """Fallback Edge TTS."""
    communicate = edge_tts.Communicate(
        text=text,
        voice="en-US-GuyNeural",
        rate="+0%",
        pitch="+0Hz"
    )
    with open(output_audio_path, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
    return output_audio_path

def generate_teacher_narration(text: str, output_audio_path: Path) -> Path:
    """
    Generates 100% human-grade educator narration.
    Uses ElevenLabs first, with clean fallback.
    """
    success = synthesize_with_elevenlabs(text, output_audio_path)
    if success:
        return output_audio_path
    
    print("[*] Using Edge Neural fallback voice...")
    asyncio.run(synthesize_speech_edge(text, output_audio_path))
    return output_audio_path
