import os
import subprocess
from pathlib import Path
from typing import List
from PIL import Image, ImageDraw, ImageFont
from config import VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS, TEMP_DIR, OUTPUT_DIR, FONTS_DIR

# Dimensions
WIDTH = VIDEO_WIDTH
HEIGHT = VIDEO_HEIGHT
FPS = VIDEO_FPS

# Palette: Slate Chalkboard & Pastel Sticky Notes
CHALKBOARD_BG = (22, 27, 36)
CHALKBOARD_GRID = (38, 46, 60)
HEADER_BAR_BG = (28, 34, 46)
HEADER_BORDER = (55, 68, 92)

# Chalk Colors
CHALK_WHITE = (245, 245, 247)
CHALK_MUTED = (160, 175, 195)
CHALK_YELLOW = (255, 224, 102)
CHALK_CYAN = (112, 230, 255)
CHALK_MAGENTA = (255, 120, 190)
CHALK_GREEN = (116, 232, 151)
CHALK_RED = (255, 107, 107)

# Sticky Note Pastel Colors & Text Colors
STICKY_PALETTES = {
    "yellow": {"bg": (254, 240, 138), "text": (28, 25, 23), "pin": (220, 38, 38)},
    "cyan":   {"bg": (186, 230, 253), "text": (15, 23, 42),  "pin": (37, 99, 235)},
    "pink":   {"bg": (254, 205, 211), "text": (136, 19, 55), "pin": (225, 29, 72)},
    "lime":   {"bg": (217, 249, 157), "text": (20, 83, 45),  "pin": (22, 163, 74)},
    "purple": {"bg": (233, 213, 255), "text": (88, 28, 135), "pin": (147, 51, 234)}
}

def get_handwritten_font(size: int, font_type: str = "kalam"):
    if font_type == "kalam":
        p = FONTS_DIR / "Kalam-Bold.ttf"
    elif font_type == "patrick":
        p = FONTS_DIR / "PatrickHand-Regular.ttf"
    elif font_type == "architect":
        p = FONTS_DIR / "ArchitectsDaughter.ttf"
    else:
        p = FONTS_DIR / "PatrickHand-Regular.ttf"

    if p.exists():
        return ImageFont.truetype(str(p), size)
    
    # Fallback to system fonts
    fallbacks = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
    ]
    for fb in fallbacks:
        if os.path.exists(fb):
            return ImageFont.truetype(fb, size)
    return ImageFont.load_default()

def draw_chalkboard_background(draw):
    """Draws a slate chalkboard texture with chalk grid dots."""
    draw.rectangle([(0, 0), (WIDTH, HEIGHT)], fill=CHALKBOARD_BG)
    for x in range(50, WIDTH, 50):
        for y in range(50, HEIGHT, 50):
            draw.point((x, y), fill=CHALKBOARD_GRID)

    # Top Slate Header
    draw.rectangle([(0, 0), (WIDTH, 85)], fill=HEADER_BAR_BG)
    draw.line([(0, 85), (WIDTH, 85)], fill=HEADER_BORDER, width=3)

def draw_sticky_note(draw, x: int, y: int, w: int, h: int, palette_key: str, title: str, bullets: List[str]):
    """Draws an authentic, high-quality sticky note with drop shadow, tape, and pushpin."""
    palette = STICKY_PALETTES.get(palette_key, STICKY_PALETTES["yellow"])
    bg_color = palette["bg"]
    text_color = palette["text"]
    pin_color = palette["pin"]

    # 1. Drop Shadow
    draw.rectangle([(x + 8, y + 8), (x + w + 8, y + h + 8)], fill=(12, 15, 20))
    # 2. Main Note Body
    draw.rectangle([(x, y), (x + w, y + h)], fill=bg_color)

    # 3. Top Center Masking Tape / Pin
    tape_w = 60
    draw.rectangle([(x + w//2 - tape_w//2, y - 8), (x + w//2 + tape_w//2, y + 10)], fill=(240, 240, 240))
    draw.ellipse([(x + w//2 - 6, y - 5), (x + w//2 + 6, y + 7)], fill=pin_color)

    # 4. Note Header
    font_title = get_handwritten_font(28, "kalam")
    font_bullets = get_handwritten_font(24, "patrick")

    draw.text((x + 20, y + 22), title, fill=text_color, font=font_title)
    draw.line([(x + 20, y + 62), (x + w - 20, y + 62)], fill=(180, 180, 180), width=2)

    # 5. Bullets
    by = y + 78
    for b in bullets[:4]:
        # Bullet dot
        draw.ellipse([(x + 20, by + 6), (x + 28, by + 14)], fill=pin_color)
        draw.text((x + 36, by), b, fill=text_color, font=font_bullets)
        by += 44

def draw_chalk_terminal(draw, x: int, y: int, w: int, h: int, title: str, code_lines: str):
    """Draws a hand-drawn chalkboard style terminal box with chalk code."""
    # Terminal Body
    draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=12, fill=(15, 18, 25), outline=CHALK_GREEN, width=3)
    # Header bar
    draw.rounded_rectangle([(x, y), (x + w, y + 42)], radius=12, fill=(28, 34, 46))
    
    # Dots
    draw.ellipse([(x + 16, y + 14), (x + 26, y + 24)], fill=CHALK_RED)
    draw.ellipse([(x + 34, y + 14), (x + 44, y + 24)], fill=CHALK_YELLOW)
    draw.ellipse([(x + 52, y + 14), (x + 62, y + 24)], fill=CHALK_GREEN)
    
    font_badge = get_handwritten_font(20, "kalam")
    font_code = get_handwritten_font(24, "architect")
    draw.text((x + 80, y + 8), f"⌨️  {title}", fill=CHALK_MUTED, font=font_badge)

    cy = y + 58
    for line in code_lines.split("\n")[:7]:
        color = CHALK_GREEN if line.startswith("$") or line.startswith("#") else CHALK_WHITE
        draw.text((x + 20, cy), line, fill=color, font=font_code)
        cy += 36

def render_board_frame(act_data, turn_data: dict, output_image: Path):
    """
    Renders an authentic, handwritten chalkboard & sticky notes scene.
    """
    img = Image.new("RGB", (WIDTH, HEIGHT), CHALKBOARD_BG)
    draw = ImageDraw.Draw(img)

    draw_chalkboard_background(draw)

    font_logo = get_handwritten_font(34, "kalam")
    font_sub = get_handwritten_font(24, "patrick")
    font_act_title = get_handwritten_font(32, "kalam")
    font_speaker = get_handwritten_font(26, "kalam")
    font_quote = get_handwritten_font(26, "patrick")

    # 1. Top Logo Bar
    draw.text((80, 20), "📝 GIT MASTERCLASS — BOARD EXPLANATION", fill=CHALK_YELLOW, font=font_logo)
    draw.text((800, 28), "| Visual Board & Sticky Notes Series", fill=CHALK_MUTED, font=font_sub)

    speaker = turn_data["speaker"]
    text = turn_data["text"]
    speaker_color = CHALK_CYAN if speaker == "Alex" else CHALK_MAGENTA

    # Top Right Act Badge
    badge_w = 260
    draw.rounded_rectangle([(WIDTH - 80 - badge_w, 18), (WIDTH - 80, 68)], radius=10, fill=(35, 45, 60), outline=speaker_color, width=2)
    draw.text((WIDTH - 80 - badge_w + 20, 25), act_data.badge, fill=speaker_color, font=font_speaker)

    # 2. Main Board Content
    is_summary_act = (act_data.act_id == 6)

    if is_summary_act:
        # Act 6: FULL STICKY NOTES SUMMARY BOARD LAYOUT (4 Sticky Notes Pinboard)
        draw.text((80, 105), "📌 Lesson Summary & Master Pinboard", fill=CHALK_YELLOW, font=font_act_title)

        draw_sticky_note(80, 150, 410, 440, "yellow", "📌 Core Takeaway", [
            "• Version control is time travel",
            "• Never save final_v2.zip again",
            "• Every commit is permanent",
            "• Rewind errors in 1 second"
        ])
        draw_sticky_note(520, 150, 410, 440, "cyan", "⚡ Git Architecture", [
            "• 100% Distributed system",
            "• Full offline repository clone",
            "• Snapshot data model",
            "• SHA cryptographic hashes"
        ])
        draw_sticky_note(960, 150, 410, 440, "pink", "⚠️ Senior Pitfalls", [
            "• Unverified email breaks streak",
            "• Missing .gitignore leaks secrets",
            "• Standardize main branch",
            "• Learn CLI before GUI"
        ])
        draw_sticky_note(1400, 150, 440, 440, "lime", "🎯 Action Challenge", [
            "• Open your terminal now",
            "• Run git config --list",
            "• Verify name & email setup",
            "• Ready for Lesson 02!"
        ])

    else:
        # Standard Acts: Sticky Note on Left + Chalkboard Terminal / Diagrams on Right
        palette_map = {1: "yellow", 2: "cyan", 3: "purple", 4: "lime", 5: "yellow"}
        pal = palette_map.get(act_data.act_id, "yellow")

        # Left Column: Sticky Note
        draw_sticky_note(
            draw=draw,
            x=80,
            y=120,
            w=780,
            h=470,
            palette_key=pal,
            title=f"📌 {act_data.visual_title}",
            bullets=act_data.bullet_points
        )

        # Right Column: Chalkboard Code Terminal
        if act_data.code_content:
            draw_chalk_terminal(
                draw=draw,
                x=900,
                y=120,
                w=940,
                h=470,
                title="Interactive Board Terminal",
                code_lines=act_data.code_content
            )

    # 3. Dynamic Speaker Dialogue Board (Bottom)
    dialogue_box = [(80, 620), (WIDTH - 80, HEIGHT - 65)]
    draw.rounded_rectangle(dialogue_box, radius=14, fill=(28, 34, 46), outline=speaker_color, width=3)

    # Speaker Pin Badge
    speaker_title = "Alex (Lead Architect)" if speaker == "Alex" else "Sarah (Senior Staff Engineer)"
    draw.rounded_rectangle([(110, 642), (480, 690)], radius=10, fill=(18, 22, 30), outline=speaker_color, width=2)
    draw.text((130, 650), f"🎙️  {speaker_title}", fill=speaker_color, font=font_speaker)

    # Wrap dialogue quote text
    words = text.split()
    lines = []
    curr = ""
    for w in words:
        if len(curr + " " + w) < 90:
            curr += (" " if curr else "") + w
        else:
            lines.append(curr)
            curr = w
    if curr:
        lines.append(curr)

    qy = 708
    for l in lines[:3]:
        draw.text((120, qy), f"“{l}”" if qy == 708 else f" {l}", fill=CHALK_WHITE, font=font_quote)
        qy += 40

    # Bottom Progress Line
    draw.rectangle([(0, HEIGHT - 10), (WIDTH, HEIGHT)], fill=speaker_color)

    img.save(output_image)

def compose_act_video(act_data, timed_turns: List[dict], act_audio_file: Path, output_video: Path):
    """
    Renders timed handwritten board video clips for each turn and stitches with audio.
    """
    turn_video_files = []

    for t in timed_turns:
        t_idx = t["turn_index"]
        t_dur = t["duration"]
        t_img = TEMP_DIR / f"board_act_{act_data.act_id}_turn_{t_idx}.png"
        t_vid = TEMP_DIR / f"board_clip_act_{act_data.act_id}_turn_{t_idx}.mp4"

        # 1. Render handwritten board frame
        render_board_frame(act_data, t, t_img)

        # 2. Render timed video segment
        subprocess.run([
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(t_img),
            "-c:v", "libx264", "-t", str(t_dur),
            "-pix_fmt", "yuv420p",
            "-r", str(FPS),
            str(t_vid)
        ], capture_output=True, check=True)

        turn_video_files.append(t_vid)

    # Concat video turns
    act_vconcat = TEMP_DIR / f"board_act_{act_data.act_id}_vconcat.txt"
    with open(act_vconcat, "w") as f:
        for tv in turn_video_files:
            f.write(f"file '{tv}'\n")

    act_stitched_video = TEMP_DIR / f"board_act_{act_data.act_id}_stitched.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(act_vconcat),
        "-c", "copy",
        str(act_stitched_video)
    ], capture_output=True, check=True)

    # Mux with act audio
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(act_stitched_video),
        "-i", str(act_audio_file),
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        str(output_video)
    ], capture_output=True, check=True)

def stitch_master_deepdive_film(act_video_files: List[Path], output_film: Path):
    """
    Stitches all 6 educational acts into the final master 1080p handwritten board film.
    """
    master_concat = TEMP_DIR / "master_board_concat.txt"
    with open(master_concat, "w") as f:
        for av in act_video_files:
            f.write(f"file '{av}'\n")

    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(master_concat),
        "-c", "copy",
        str(output_film)
    ], capture_output=True, check=True)
