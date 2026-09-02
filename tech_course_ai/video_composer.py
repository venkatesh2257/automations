import subprocess
import os
from pathlib import Path
from typing import List, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor
from config import VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS, TEMP_DIR
from broll_engine import get_real_motion_broll_clip
from sound_designer import create_tech_ambient_drone

def get_audio_duration(audio_file: Path) -> float:
    """Returns audio duration in seconds using ffprobe."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_file)
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        return float(result.stdout.strip())
    except Exception:
        return 30.0

def render_cinematic_motion_section(
    broll_query: str,
    hud_overlay_png: Path,
    narration_audio: Path,
    output_clip_path: Path
) -> Tuple[Path, float]:
    """
    Composites a REAL 1080p moving video background with a transparent HUD overlay and audio.
    """
    duration = get_audio_duration(narration_audio)
    
    # 1. Fetch / Generate real 1080p moving video background
    temp_broll_path = TEMP_DIR / f"raw_broll_{output_clip_path.stem}.mp4"
    get_real_motion_broll_clip(broll_query, duration, temp_broll_path)

    # 2. Overlay HUD PNG over real moving video clip
    filter_complex = (
        f"[0:v]scale={VIDEO_WIDTH}:{VIDEO_HEIGHT},setsar=1[bg];"
        f"[1:v]scale={VIDEO_WIDTH}:{VIDEO_HEIGHT},setsar=1[hud];"
        f"[bg][hud]overlay=0:0[outv]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(temp_broll_path),
        "-i", str(hud_overlay_png),
        "-i", str(narration_audio),
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-map", "2:a",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-t", f"{duration:.3f}",
        str(output_clip_path)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_clip_path, duration

def composite_master_course_video(
    broll_queries: List[str],
    hud_overlay_paths: List[Path],
    audio_paths: List[Path],
    section_names: List[str],
    output_video_path: Path
) -> Tuple[Path, List[Dict[str, str]]]:
    """
    Composites all real moving video sections into the final 1080p Masterclass film.
    """
    num_sections = len(hud_overlay_paths)
    print(f"[*] Rendering {num_sections} cinematic real-motion video scenes in parallel...")

    clip_paths = [TEMP_DIR / f"cinematic_sec_{idx}.mp4" for idx in range(num_sections)]
    section_durations = [0.0] * num_sections

    with ThreadPoolExecutor(max_workers=min(4, num_sections)) as executor:
        futures = {
            executor.submit(
                render_cinematic_motion_section,
                query, hud, audio, clip
            ): idx
            for idx, (query, hud, audio, clip) in enumerate(
                zip(broll_queries, hud_overlay_paths, audio_paths, clip_paths)
            )
        }
        for future in futures:
            idx = futures[future]
            _, dur = future.result()
            section_durations[idx] = dur

    # Compute Chapter Markers
    chapter_markers = []
    current_seconds = 0.0
    for idx, (name, dur) in enumerate(zip(section_names, section_durations)):
        mins = int(current_seconds // 60)
        secs = int(current_seconds % 60)
        time_str = f"{mins:02d}:{secs:02d}"
        chapter_markers.append({
            "timestamp": time_str,
            "title": name,
            "seconds": current_seconds
        })
        current_seconds += dur

    total_duration = current_seconds

    # Create Concat list
    concat_list_path = TEMP_DIR / "cinematic_concat_list.txt"
    with open(concat_list_path, "w") as f:
        for clip in clip_paths:
            f.write(f"file '{clip.resolve()}'\n")

    print("[*] Stitching final cinematic 1080p masterclass film...")
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_list_path),
        "-c", "copy",
        str(output_video_path)
    ]
    subprocess.run(cmd, check=True)

    print(f"[✓] Cinematic 1080p Film Complete: {output_video_path.name} ({total_duration:.1f}s)")
    return output_video_path, chapter_markers
