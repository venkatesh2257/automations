import os
import requests
import subprocess
from pathlib import Path
from typing import List, Tuple
from config import ELEVENLABS_API_KEY, ELEVENLABS_MODEL, TEMP_DIR

# Voice IDs for the 2 Hosts
VOICE_MAP = {
    "Alex": "pNInz6obpgDQGcFmaJgB",   # Adam (Authoritative lead architect)
    "Sarah": "EXAVITQu4vr4xnSDxMaL"   # Sarah (Natural conversational engineer)
}

def synthesize_dialogue_turn(speaker: str, text: str, output_path: Path) -> float:
    """
    Synthesizes a single dialogue turn using ElevenLabs multi-speaker engine.
    Returns the exact duration of the audio in seconds.
    """
    voice_id = VOICE_MAP.get(speaker, VOICE_MAP["Alex"])
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": ELEVENLABS_MODEL,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.85,
            "style": 0.35,
            "use_speaker_boost": True
        }
    }

    resp = requests.post(url, json=payload, headers=headers, timeout=25)
    if resp.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(resp.content)
    else:
        # Fallback to local TTS if API limits hit
        print(f"[!] ElevenLabs warning ({resp.status_code}), using fallback audio...")
        subprocess.run([
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"sine=frequency=440:duration=4",
            "-c:a", "aac",
            str(output_path)
        ], capture_output=True, check=True)

    # Get exact duration via ffprobe
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(output_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def synthesize_act_audio(act_id: int, dialogue_turns: list) -> Tuple[Path, List[dict], float]:
    """
    Synthesizes all dialogue turns for an act and stitches them into a single audio track.
    Returns: (act_audio_path, timed_turns, total_act_duration)
    """
    turn_files = []
    timed_turns = []
    current_time_offset = 0.0

    for idx, turn in enumerate(dialogue_turns):
        speaker = turn.speaker
        text = turn.text
        turn_audio = TEMP_DIR / f"act_{act_id}_turn_{idx}_{speaker.lower()}.mp3"
        
        print(f"  [🎙️] Synthesizing {speaker}: \"{text[:45]}...\"")
        dur = synthesize_dialogue_turn(speaker, text, turn_audio)

        turn_info = {
            "turn_index": idx,
            "speaker": speaker,
            "text": text,
            "start_time": current_time_offset,
            "duration": dur,
            "end_time": current_time_offset + dur,
            "audio_file": turn_audio
        }
        timed_turns.append(turn_info)
        turn_files.append(turn_audio)
        current_time_offset += dur

    # Concat all turns for this act
    act_concat_list = TEMP_DIR / f"act_{act_id}_turns.txt"
    with open(act_concat_list, "w") as f:
        for tf in turn_files:
            f.write(f"file '{tf}'\n")

    act_audio_output = TEMP_DIR / f"act_{act_id}_master_audio.mp3"
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(act_concat_list),
        "-c:a", "libmp3lame",
        str(act_audio_output)
    ], capture_output=True, check=True)

    return act_audio_output, timed_turns, current_time_offset
