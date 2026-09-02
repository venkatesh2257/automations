import os
import sys
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent
SOURCES_DIR = BASE_DIR / "notebooklm_sources"
AUDIO_DIR = BASE_DIR / "notebooklm_audio"
OUTPUT_DIR = BASE_DIR / "output"
TEMP_DIR = BASE_DIR / "temp"

for d in [SOURCES_DIR, AUDIO_DIR, OUTPUT_DIR, TEMP_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# 1080p Constants
WIDTH = 1920
HEIGHT = 1080
FPS = 30

# High-Tech Dark Colors
BG_COLOR = (13, 17, 23)
CARD_BG = (22, 27, 34)
BORDER_COLOR = (48, 54, 61)
TEXT_WHITE = (240, 246, 252)
TEXT_MUTED = (139, 148, 158)
ACCENT_CYAN = (0, 229, 255)
ACCENT_GREEN = (63, 185, 80)
ACCENT_YELLOW = (227, 179, 65)
ACCENT_RED = (248, 81, 73)
ACCENT_PURPLE = (188, 140, 255)

def get_font(size: int, bold: bool = False):
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in font_paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def get_audio_duration(audio_file: Path) -> float:
    """Returns audio duration in seconds using ffprobe."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_file)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def render_scene_card(title: str, subtitle: str, badge: str, bullets: list, code: str, output_img: Path):
    """Renders a pixel-perfect 1920x1080 slide for the video track."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Top Navigation Bar
    draw.rectangle([(0, 0), (WIDTH, 90)], fill=(22, 27, 34))
    draw.line([(0, 90), (WIDTH, 90)], fill=BORDER_COLOR, width=2)
    
    font_logo = get_font(32, bold=True)
    font_badge = get_font(20, bold=True)
    font_title = get_font(44, bold=True)
    font_sub = get_font(26, bold=False)
    font_body = get_font(28, bold=False)
    font_code = get_font(24, bold=True)

    # Logo
    draw.text((80, 26), "GIT MASTERCLASS", fill=ACCENT_CYAN, font=font_logo)
    draw.text((430, 32), "| Powered by Google NotebookLM", fill=TEXT_MUTED, font=font_sub)

    # Badge Top Right
    badge_w = 260
    draw.rounded_rectangle([(WIDTH - 80 - badge_w, 22), (WIDTH - 80, 68)], radius=10, fill=(35, 45, 60), outline=ACCENT_CYAN, width=2)
    draw.text((WIDTH - 80 - badge_w + 20, 32), badge, fill=ACCENT_CYAN, font=font_badge)

    # Main Center Card
    card_top = 140
    card_bottom = HEIGHT - 90
    draw.rounded_rectangle([(80, card_top), (WIDTH - 80, card_bottom)], radius=18, fill=CARD_BG, outline=BORDER_COLOR, width=2)

    # Card Title
    draw.text((130, card_top + 45), title, fill=TEXT_WHITE, font=font_title)
    draw.text((130, card_top + 105), subtitle, fill=ACCENT_YELLOW, font=font_sub)
    draw.line([(130, card_top + 150), (WIDTH - 130, card_top + 150)], fill=BORDER_COLOR, width=2)

    # Left Column: Bullets
    y = card_top + 190
    if bullets:
        for b in bullets:
            draw.ellipse([(130, y + 8), (144, y + 22)], fill=ACCENT_CYAN)
            draw.text((165, y), b, fill=TEXT_WHITE, font=font_body)
            y += 62

    # Right Column or Bottom Card: Code / Terminal
    if code:
        code_box = [(WIDTH // 2, card_top + 180), (WIDTH - 130, card_bottom - 50)]
        draw.rounded_rectangle(code_box, radius=12, fill=(13, 17, 23), outline=ACCENT_GREEN, width=2)
        
        # Terminal Header
        draw.rounded_rectangle([(code_box[0][0], code_box[0][1]), (code_box[1][0], code_box[0][1] + 45)], radius=12, fill=(30, 36, 46))
        # Terminal Dots
        draw.ellipse([(code_box[0][0] + 16, code_box[0][1] + 16), (code_box[0][0] + 28, code_box[0][1] + 28)], fill=ACCENT_RED)
        draw.ellipse([(code_box[0][0] + 36, code_box[0][1] + 16), (code_box[0][0] + 48, code_box[0][1] + 28)], fill=ACCENT_YELLOW)
        draw.ellipse([(code_box[0][0] + 56, code_box[0][1] + 16), (code_box[0][0] + 68, code_box[0][1] + 28)], fill=ACCENT_GREEN)
        draw.text((code_box[0][0] + 85, code_box[0][1] + 10), "Terminal Session", fill=TEXT_MUTED, font=font_badge)

        # Code lines
        cy = code_box[0][1] + 70
        for line in code.split("\n"):
            color = ACCENT_GREEN if line.startswith("$") else TEXT_WHITE
            draw.text((code_box[0][0] + 25, cy), line, fill=color, font=font_code)
            cy += 38

    # Bottom Progress Bar
    draw.rectangle([(0, HEIGHT - 12), (WIDTH, HEIGHT)], fill=(22, 27, 34))
    draw.rectangle([(0, HEIGHT - 12), (WIDTH, HEIGHT)], fill=ACCENT_CYAN)

    img.save(output_img)
    print(f"  [✓] Rendered synced visual slide: {output_img.name}")

def assemble_notebooklm_video(audio_path: str, lesson_id: str = "git_lesson_01"):
    """
    Takes Google NotebookLM audio and produces a 100% synchronized 1080p Video.
    """
    audio_file = Path(audio_path)
    if not audio_file.exists():
        print(f"[!] Error: Audio file {audio_file} does not exist.")
        return

    print("=" * 70)
    print(f"🎬 GOOGLE NOTEBOOKLM AUDIO-TO-VIDEO SYNC ENGINE")
    print(f" • Audio Source: {audio_file.name}")
    print(f" • Resolution  : 1920x1080 (Full HD 30fps)")
    print("=" * 70)

    total_duration = get_audio_duration(audio_file)
    print(f"[*] Detected NotebookLM Audio Duration: {total_duration:.2f} seconds")

    # Define 6 Key Educational Scenes for Lesson 1
    scenes = [
        {
            "id": 1,
            "title": "The Chaos: Life Before Version Control",
            "subtitle": "The final_v1.zip, final_v2_really_final.zip nightmare",
            "badge": "ACT 1: THE HOOK",
            "bullets": [
                "Multiple engineers overwriting each other's code",
                "2 AM critical production outage with no audit trail",
                "Zero ability to safely roll back to a working state",
                "Lost engineering hours manually diffing files"
            ],
            "code": "$ ls -la /shared_project\nauth_service_v1.py\nauth_service_v2_FINAL.py\nauth_service_v3_DO_NOT_DELETE.py\n[CRITICAL ERROR] Overwritten session handler!"
        },
        {
            "id": 2,
            "title": "The Core Mental Model: Video Game Checkpoints",
            "subtitle": "Never save over your project file again",
            "badge": "ACT 2: ANALOGY",
            "bullets": [
                "Checkpoint (Commit): Instant respawn before dangerous boss fights",
                "Branch (Alternate Slot): Explore experiments without risking main save",
                "Merge (Combine): Safely integrate victories into the main story",
                "Immutability: Every checkpoint is permanently cryptographically sealed"
            ],
            "code": "# The Mental Model\nCheckpoint 1: Project Initialized\nCheckpoint 2: Added User Login\nCheckpoint 3: Broken API Refactor\n==> Action: Rewind to Checkpoint 2 in 1 sec!"
        },
        {
            "id": 3,
            "title": "Centralized vs. Distributed Version Control",
            "subtitle": "Why Linus Torvalds engineered Git for the Linux Kernel in 2005",
            "badge": "ACT 3: ARCHITECTURE",
            "bullets": [
                "Centralized (SVN): Single point of failure; offline work is impossible",
                "Distributed (Git): Every developer has the FULL repository history",
                "100% Offline: Commit, branch, diff, and inspect with zero Wi-Fi",
                "Blazing Speed: All operations execute on local SSD in milliseconds"
            ],
            "code": "Centralized (SVN): [Laptop] ---> [Single Central Server (SPoF)]\n\nDistributed (Git):\n[Laptop A (Full Clone)] <---> [GitHub Backup]\n[Laptop B (Full Clone)] <---> [Laptop C (Full Clone)]"
        },
        {
            "id": 4,
            "title": "Under The Hood: Snapshots vs Deltas",
            "subtitle": "How Git stores data inside .git/objects",
            "badge": "ACT 4: DEEP MECHANICS",
            "bullets": [
                "Snapshots: Git takes full-filesystem pictures, not file deltas",
                "Efficiency: Unchanged files are lightweight cryptographic links",
                "Blob: Raw file content stored by hash",
                "Tree: Directory structure and filenames",
                "Commit: Top-level tree + Author + Parent Hash DAG"
            ],
            "code": "$ git cat-file -p HEAD\ntree d8329fc1cc938780ffdd9f94e0d364e0ea74f579\nauthor Alex Rivera <alex@dev.com> 1788266000\ncommitter Alex Rivera <alex@dev.com> 1788266000\n\nInitial repository architecture commit"
        },
        {
            "id": 5,
            "title": "Essential First-Time Configuration Commands",
            "subtitle": "Configuring your developer workstation properly",
            "badge": "ACT 5: TERMINAL SETUP",
            "bullets": [
                "Set global user name for commit signatures",
                "Set verified GitHub email to preserve contribution graph",
                "Standardize default branch to 'main'",
                "Set VS Code as the interactive editor",
                "Inspect all configuration file origins"
            ],
            "code": "$ git --version\ngit version 2.43.0\n\n$ git config --global user.name \"Alex Rivera\"\n$ git config --global user.email \"alex@dev.com\"\n$ git config --global init.defaultBranch main\n$ git config --list --show-origin"
        },
        {
            "id": 6,
            "title": "Senior Dev Pitfalls & Action Challenge",
            "subtitle": "Golden rules for professional production environments",
            "badge": "ACT 6: ACTION CHALLENGE",
            "bullets": [
                "⚠️ Pitfall 1: Unverified email breaks GitHub contribution streak",
                "⚠️ Pitfall 2: Forgetting .gitignore leaks API keys and .env secrets",
                "⚠️ Pitfall 3: Relying on GUI before understanding CLI plumbing",
                "🎯 Your Challenge: Run `git config --list` and verify your setup!"
            ],
            "code": "$ cat .gitignore\n.env\n*.pem\nnode_modules/\n__pycache__/\n\n# Verified & Ready for Lesson 02!"
        }
    ]

    # Calculate exact duration per scene based on audio length
    num_scenes = len(scenes)
    scene_duration = total_duration / num_scenes
    print(f"[*] Allocating {scene_duration:.2f} seconds per scene across {num_scenes} visual acts.")

    scene_video_files = []
    for s in scenes:
        img_path = TEMP_DIR / f"scene_{s['id']}.png"
        vid_path = TEMP_DIR / f"scene_{s['id']}.mp4"

        # 1. Render slide image
        render_scene_card(
            title=s["title"],
            subtitle=s["subtitle"],
            badge=s["badge"],
            bullets=s["bullets"],
            code=s["code"],
            output_img=img_path
        )

        # 2. Render timed video clip for this scene
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(img_path),
            "-c:v", "libx264", "-t", str(scene_duration),
            "-pix_fmt", "yuv420p",
            "-r", str(FPS),
            str(vid_path)
        ]
        subprocess.run(ffmpeg_cmd, capture_output=True, check=True)
        scene_video_files.append(vid_path)

    # Concat list
    concat_list = TEMP_DIR / "notebooklm_concat.txt"
    with open(concat_list, "w") as f:
        for v in scene_video_files:
            f.write(f"file '{v}'\n")

    stitched_video = TEMP_DIR / "stitched_visuals.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(stitched_video)
    ], capture_output=True, check=True)

    # Merge with exact NotebookLM audio
    final_output = OUTPUT_DIR / f"{lesson_id}_notebooklm_synced.mp4"
    mux_cmd = [
        "ffmpeg", "-y",
        "-i", str(stitched_video),
        "-i", str(audio_file),
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        str(final_output)
    ]
    subprocess.run(mux_cmd, capture_output=True, check=True)

    print("\n" + "=" * 70)
    print(f"🎉 100% PERFECTLY-SYNCED NOTEBOOKLM VIDEO IS READY!")
    print(f" • Output File: {final_output}")
    print(f" • Duration   : {total_duration:.2f} seconds")
    print("=" * 70)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        assemble_notebooklm_video(sys.argv[1])
    else:
        # Default scan for any audio in notebooklm_audio
        audio_files = list(AUDIO_DIR.glob("*.*"))
        if audio_files:
            assemble_notebooklm_video(str(audio_files[0]))
        else:
            print("Usage: python3 notebooklm_video_sync.py <path_to_notebooklm_audio_file>")
            print(f"Or drop your downloaded NotebookLM audio into: {AUDIO_DIR}")
