import asyncio
import edge_tts
from pathlib import Path
from typing import Tuple, List, Any
from config import DEFAULT_VOICE, VOICE_RATE, VOICE_PITCH, TEMP_DIR

async def generate_speech_async(
    text: str,
    output_audio_path: Path,
    voice: str = DEFAULT_VOICE,
    rate: str = VOICE_RATE,
    pitch: str = VOICE_PITCH
) -> Tuple[Path, List[Any]]:
    """
    Generates audio and extracts word-boundary subtitle cues using edge-tts.
    Returns (audio_path, cues_list).
    """
    communicate = edge_tts.Communicate(
        text, voice, rate=rate, pitch=pitch, boundary="WordBoundary"
    )
    submaker = edge_tts.SubMaker()
    
    with open(output_audio_path, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                submaker.feed(chunk)

    return output_audio_path, submaker.cues

def generate_narration(
    text: str,
    output_audio_path: Path,
    voice: str = DEFAULT_VOICE,
    rate: str = VOICE_RATE,
    pitch: str = VOICE_PITCH
) -> Tuple[Path, List[Any]]:
    """Synchronous wrapper for generate_speech_async."""
    return asyncio.run(
        generate_speech_async(text, output_audio_path, voice=voice, rate=rate, pitch=pitch)
    )
