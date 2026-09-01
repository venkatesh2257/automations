import subprocess
import os
import shutil
from pathlib import Path
from typing import List
from concurrent.futures import ThreadPoolExecutor
from config import VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS, TEMP_DIR, AUDIO_DIR

def get_media_duration(file_path: Path) -> float:
    """Gets audio or video duration in seconds using ffprobe."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        return float(result.stdout.strip())
    except ValueError:
        return 45.0

def create_ambient_bg_audio(duration: float, output_path: Path):
    """
    Generates a harmonic sacred ambient drone using FFmpeg sine waves
    if no custom background music is in assets/audio.
    """
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"sine=frequency=108:duration={duration+3},aformat=channel_layouts=stereo",
        "-f", "lavfi",
        "-i", f"sine=frequency=216:duration={duration+3},aformat=channel_layouts=stereo",
        "-filter_complex", f"[0:a]volume=0.08[a0];[1:a]volume=0.04[a1];[a0][a1]amix=inputs=2:duration=first,lowpass=f=400,afade=t=in:ss=0:d=1,afade=t=out:st={duration}:d=2[outa]",
        "-map", "[outa]",
        "-c:a", "aac",
        "-b:a", "128k",
        str(output_path)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def render_scene_clip(image_path: Path, duration: float, output_clip_path: Path) -> Path:
    """
    Renders a single image into a vertical 1080x1920 video clip with smooth Ken Burns zoom.
    """
    total_frames = int(duration * VIDEO_FPS)
    filter_graph = (
        f"zoompan=z='min(zoom+0.0006,1.15)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={VIDEO_WIDTH}x{VIDEO_HEIGHT}:fps={VIDEO_FPS}"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(image_path),
        "-vf", filter_graph,
        "-c:v", "libx264",
        "-preset", "fast",
        "-pix_fmt", "yuv420p",
        "-t", f"{duration:.3f}",
        str(output_clip_path)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_clip_path

def assemble_final_video(
    image_paths: List[Path],
    narration_audio_path: Path,
    subtitles_ass_path: Path,
    output_video_path: Path,
    bg_music_path: Path = None
) -> Path:
    """
    Combines scene clips, mixes audio and burns dynamic ASS subtitles.
    """
    total_duration = get_media_duration(narration_audio_path)
    num_images = len(image_paths)
    scene_duration = total_duration / num_images

    print(f"[*] Rendering {num_images} scene clips in parallel ({scene_duration:.2f}s each, total {total_duration:.2f}s)...")
    clip_paths = [TEMP_DIR / f"clip_{idx}.mp4" for idx in range(num_images)]

    # Render scene clips concurrently
    with ThreadPoolExecutor(max_workers=min(4, num_images)) as executor:
        futures = [
            executor.submit(render_scene_clip, img, scene_duration, clip)
            for img, clip in zip(image_paths, clip_paths)
        ]
        for f in futures:
            f.result()

    concat_list_path = TEMP_DIR / "concat_list.txt"
    with open(concat_list_path, "w") as f:
        for clip in clip_paths:
            f.write(f"file '{clip.resolve()}'\n")

    # Background audio
    ambient_audio = TEMP_DIR / "ambient_bg.aac"
    if bg_music_path and bg_music_path.exists():
        bg_audio_file = bg_music_path
    else:
        available_bg = list(AUDIO_DIR.glob("*.mp3")) + list(AUDIO_DIR.glob("*.wav"))
        if available_bg:
            bg_audio_file = available_bg[0]
        else:
            create_ambient_bg_audio(total_duration, ambient_audio)
            bg_audio_file = ambient_audio

    sub_path_escaped = str(subtitles_ass_path.resolve()).replace(":", "\\:").replace("\\", "/")

    print("[*] Assembling master video and burning dynamic subtitles...")
    filter_complex = (
        f"[0:v]subtitles='{sub_path_escaped}'[v];"
        f"[1:a]volume=1.0[voice];"
        f"[2:a]volume=0.12,afade=t=in:ss=0:d=1,afade=t=out:st={total_duration-2}:d=2[bg];"
        f"[voice][bg]amix=inputs=2:duration=first:dropout_transition=2[a]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_list_path),
        "-i", str(narration_audio_path),
        "-i", str(bg_audio_file),
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "[a]",
        "-t", f"{total_duration:.3f}",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "19",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        str(output_video_path)
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"[!] Subtitle overlay warning: {result.stderr[:200]} Retrying without subtitles filter...")
        cmd_fallback = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0", "-i", str(concat_list_path),
            "-i", str(narration_audio_path),
            "-t", f"{total_duration:.3f}",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "19",
            "-c:a", "aac",
            str(output_video_path)
        ]
        subprocess.run(cmd_fallback, check=True)

    print(f"[✓] Master Video Ready: {output_video_path}")
    return output_video_path
