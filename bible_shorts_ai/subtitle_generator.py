import datetime
from pathlib import Path
from typing import List, Any
from config import (
    FONT_NAME, FONT_SIZE, PRIMARY_COLOR, HIGHLIGHT_COLOR, 
    OUTLINE_COLOR, OUTLINE_WIDTH, SHADOW_DEPTH, VIDEO_WIDTH, VIDEO_HEIGHT
)

def format_ass_time(seconds: float) -> str:
    """Converts seconds into ASS timestamp format: H:MM:SS.cs"""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    csecs = int((seconds - int(seconds)) * 100)
    return f"{hrs}:{mins:02d}:{secs:02d}.{csecs:02d}"

def create_ass_subtitles(cues: List[Any], output_path: Path) -> Path:
    """
    Creates an ASS subtitle file from Subtitle cues
    with bold, centered, viral TikTok/Shorts styling.
    """
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {VIDEO_WIDTH}
PlayResY: {VIDEO_HEIGHT}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: ViralShorts,{FONT_NAME},{FONT_SIZE},{PRIMARY_COLOR},{HIGHLIGHT_COLOR},{OUTLINE_COLOR},&H80000000,-1,0,0,0,100,100,0,0,1,{OUTLINE_WIDTH},{SHADOW_DEPTH},2,40,40,460,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    
    # Process cues into words
    words = []
    for cue in cues:
        try:
            if hasattr(cue, "start") and hasattr(cue, "end") and hasattr(cue, "content"):
                start_sec = cue.start.total_seconds()
                end_sec = cue.end.total_seconds()
                text = str(cue.content).strip()
            elif isinstance(cue, (list, tuple)) and len(cue) >= 3:
                start_sec = cue[0] / 10_000_000
                end_sec = cue[1] / 10_000_000
                text = str(cue[2]).strip()
            else:
                continue

            if text:
                words.append({"start": start_sec, "end": end_sec, "text": text})
        except Exception:
            continue

    if not words:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(header)
        return output_path

    # Group words into 3-4 word punchy phrases
    chunk_size = 3
    for i in range(0, len(words), chunk_size):
        chunk = words[i:i + chunk_size]
        chunk_start = chunk[0]["start"]
        chunk_end = chunk[-1]["end"]
        
        full_text = " ".join([w["text"].upper() for w in chunk])
        
        start_str = format_ass_time(chunk_start)
        end_str = format_ass_time(chunk_end)
        
        events.append(f"Dialogue: 0,{start_str},{end_str},ViralShorts,,0,0,0,,{full_text}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")

    return output_path
