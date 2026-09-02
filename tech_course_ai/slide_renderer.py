import os
from pathlib import Path
from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFont
from config import (
    VIDEO_WIDTH, VIDEO_HEIGHT,
    COLOR_CARD_BG, COLOR_HEADER_BG,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_MUTED,
    COLOR_ACCENT_CYAN, COLOR_ACCENT_GREEN, COLOR_ACCENT_YELLOW,
    COLOR_ACCENT_RED, COLOR_BORDER
)

def get_font(size: int, bold: bool = False, mono: bool = False):
    """Loads clean system TrueType font or fallback."""
    font_names = []
    if mono:
        font_names = ["DejaVuSansMono-Bold.ttf" if bold else "DejaVuSansMono.ttf", "UbuntuMono-R.ttf", "Courier"]
    else:
        font_names = ["DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf", "Ubuntu-R.ttf", "Arial"]

    for name in font_names:
        for p in [
            f"/usr/share/fonts/truetype/dejavu/{name}",
            f"/usr/share/fonts/truetype/ubuntu/{name}",
            f"/usr/share/fonts/truetype/freefont/{name}"
        ]:
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except Exception:
                    pass
    return ImageFont.load_default()

def draw_glass_header_badge(draw: ImageDraw.ImageDraw, course_title: str, lesson_str: str):
    """Draws top header category pill with glowing cyan accent."""
    badge_text = f"● {course_title.upper()}  |  {lesson_str.upper()}"
    font = get_font(22, bold=True)
    
    x, y = 80, 50
    draw.rounded_rectangle([x, y, x + 620, y + 46], radius=8, fill=(20, 26, 36, 240), outline=COLOR_ACCENT_CYAN, width=2)
    draw.text((x + 20, y + 10), badge_text, fill=COLOR_ACCENT_CYAN, font=font)

def render_transparent_concept_hud(
    course_name: str,
    lesson_str: str,
    slide_title: str,
    bullet_points: List[str],
    output_path: Path
) -> Path:
    """Renders a transparent glassmorphic concept HUD overlay."""
    img = Image.new("RGBA", (VIDEO_WIDTH, VIDEO_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Header Badge
    draw_glass_header_badge(draw, course_name, lesson_str)

    # Title with dark backdrop
    title_font = get_font(48, bold=True)
    draw.rounded_rectangle([80, 115, VIDEO_WIDTH - 80, 195], radius=10, fill=(15, 20, 28, 220), outline=COLOR_BORDER, width=1)
    draw.text((105, 130), slide_title, fill=COLOR_TEXT_PRIMARY, font=title_font)

    # Main Card Box (Glassmorphic dark slate)
    card_box = [80, 220, VIDEO_WIDTH - 80, VIDEO_HEIGHT - 80]
    draw.rounded_rectangle(card_box, radius=16, fill=(15, 20, 28, 230), outline=COLOR_BORDER, width=2)

    # Bullet items
    bullet_font = get_font(32, bold=False)
    icon_font = get_font(28, bold=True)
    
    start_y = 280
    spacing = 110
    
    for idx, pt in enumerate(bullet_points[:5]):
        cur_y = start_y + (idx * spacing)
        # Glow indicator pill
        draw.rounded_rectangle([120, cur_y, 165, cur_y + 44], radius=8, fill=COLOR_ACCENT_CYAN)
        draw.text((135, cur_y + 6), f"{idx+1}", fill=(13, 17, 23), font=icon_font)
        # Text
        draw.text((190, cur_y + 6), pt, fill=COLOR_TEXT_PRIMARY, font=bullet_font)

    img.save(output_path, "PNG")
    return output_path

def render_transparent_terminal_hud(
    course_name: str,
    lesson_str: str,
    slide_title: str,
    terminal_code: str,
    bullet_points: List[str],
    output_path: Path
) -> Path:
    """Renders a transparent glassmorphic macOS/Linux terminal window."""
    img = Image.new("RGBA", (VIDEO_WIDTH, VIDEO_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Header Badge
    draw_glass_header_badge(draw, course_name, lesson_str)

    # Title
    title_font = get_font(48, bold=True)
    draw.rounded_rectangle([80, 115, VIDEO_WIDTH - 80, 195], radius=10, fill=(15, 20, 28, 220), outline=COLOR_BORDER, width=1)
    draw.text((105, 130), slide_title, fill=COLOR_TEXT_PRIMARY, font=title_font)

    # Terminal Window Coordinates
    term_x1, term_y1 = 80, 220
    term_x2, term_y2 = VIDEO_WIDTH - 80, VIDEO_HEIGHT - 80

    # Draw Window Frame
    draw.rounded_rectangle([term_x1, term_y1, term_x2, term_y2], radius=14, fill=(12, 16, 22, 240), outline=COLOR_ACCENT_CYAN, width=2)
    
    # Titlebar
    titlebar_h = 48
    draw.rounded_rectangle([term_x1, term_y1, term_x2, term_y1 + titlebar_h], radius=14, fill=(25, 32, 44, 255))
    draw.rectangle([term_x1, term_y1 + 24, term_x2, term_y1 + titlebar_h], fill=(25, 32, 44, 255))
    draw.line([term_x1, term_y1 + titlebar_h, term_x2, term_y1 + titlebar_h], fill=COLOR_BORDER, width=2)

    # Traffic light buttons (Close, Minimize, Maximize)
    draw.ellipse([term_x1 + 25, term_y1 + 16, term_x1 + 41, term_y1 + 32], fill=COLOR_ACCENT_RED)
    draw.ellipse([term_x1 + 55, term_y1 + 16, term_x1 + 71, term_y1 + 32], fill=COLOR_ACCENT_YELLOW)
    draw.ellipse([term_x1 + 85, term_y1 + 16, term_x1 + 101, term_y1 + 32], fill=COLOR_ACCENT_GREEN)

    # Terminal Title
    term_title_font = get_font(20, mono=True)
    draw.text((term_x1 + 130, term_y1 + 14), "bash - terminal (pro-educator)", fill=COLOR_TEXT_MUTED, font=term_title_font)

    # Code Lines
    code_font = get_font(30, mono=True)
    lines = terminal_code.split("\n")
    cur_y = term_y1 + titlebar_h + 35

    for line in lines:
        if line.startswith("$"):
            draw.text((term_x1 + 40, cur_y), "$", fill=COLOR_ACCENT_GREEN, font=code_font)
            draw.text((term_x1 + 70, cur_y), line[1:].strip(), fill=COLOR_TEXT_PRIMARY, font=code_font)
        elif line.startswith("#"):
            draw.text((term_x1 + 40, cur_y), line, fill=COLOR_TEXT_MUTED, font=code_font)
        else:
            draw.text((term_x1 + 40, cur_y), line, fill=COLOR_ACCENT_CYAN, font=code_font)
        cur_y += 44

    img.save(output_path, "PNG")
    return output_path

def render_transparent_warning_hud(
    course_name: str,
    lesson_str: str,
    slide_title: str,
    code_snippet: str,
    bullet_points: List[str],
    output_path: Path
) -> Path:
    """Renders a transparent warning / best practice HUD overlay."""
    img = Image.new("RGBA", (VIDEO_WIDTH, VIDEO_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Header Badge
    draw_glass_header_badge(draw, course_name, lesson_str)

    # Title
    title_font = get_font(48, bold=True)
    draw.rounded_rectangle([80, 115, VIDEO_WIDTH - 80, 195], radius=10, fill=(15, 20, 28, 220), outline=COLOR_BORDER, width=1)
    draw.text((105, 130), slide_title, fill=COLOR_TEXT_PRIMARY, font=title_font)

    # Warning Box with Red Alert Border
    card_box = [80, 220, VIDEO_WIDTH - 80, VIDEO_HEIGHT - 80]
    draw.rounded_rectangle(card_box, radius=16, fill=(20, 12, 14, 240), outline=COLOR_ACCENT_RED, width=3)

    # Warning Banner
    draw.rounded_rectangle([80, 220, VIDEO_WIDTH - 80, 280], radius=16, fill=(70, 20, 20, 255))
    banner_font = get_font(26, bold=True)
    draw.text((120, 235), "⚠️  SENIOR DEVELOPER PRODUCTION WARNING", fill=COLOR_ACCENT_RED, font=banner_font)

    # Bullet items
    bullet_font = get_font(30, bold=False)
    start_y = 310
    for idx, pt in enumerate(bullet_points[:4]):
        cur_y = start_y + (idx * 60)
        draw.text((120, cur_y), f"• {pt}", fill=COLOR_TEXT_PRIMARY, font=bullet_font)

    # Code Box if present
    if code_snippet:
        code_y = start_y + (len(bullet_points[:4]) * 60) + 25
        draw.rounded_rectangle([120, code_y, VIDEO_WIDTH - 120, VIDEO_HEIGHT - 110], radius=10, fill=(12, 16, 22, 250), outline=COLOR_BORDER, width=2)
        code_font = get_font(28, mono=True)
        c_y = code_y + 20
        for line in code_snippet.split("\n")[:5]:
            color = COLOR_ACCENT_GREEN if line.startswith("$") else (COLOR_TEXT_MUTED if line.startswith("#") else COLOR_TEXT_PRIMARY)
            draw.text((150, c_y), line, fill=color, font=code_font)
            c_y += 38

    img.save(output_path, "PNG")
    return output_path

def render_slide_by_type(
    course_name: str,
    lesson_str: str,
    visual_type: str,
    slide_title: str,
    code_content: str,
    bullet_points: List[str],
    output_path: Path
) -> Path:
    """Dispatches transparent HUD overlay rendering."""
    if visual_type == "terminal":
        return render_transparent_terminal_hud(course_name, lesson_str, slide_title, code_content, bullet_points, output_path)
    elif visual_type == "warning_card":
        return render_transparent_warning_hud(course_name, lesson_str, slide_title, code_content, bullet_points, output_path)
    else:
        return render_transparent_concept_hud(course_name, lesson_str, slide_title, bullet_points, output_path)
