import urllib.parse
import random
import time
import requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from config import IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_MODEL, TEMP_DIR

def enhance_biblical_prompt(prompt: str) -> str:
    """Enhances a prompt with cinematic keywords for high-fidelity biblical imagery."""
    keywords = [
        "cinematic biblical art",
        "volumetric golden rays",
        "dramatic chiaroscuro lighting",
        "photorealistic 8k",
        "hyper-detailed intricate textures",
        "vertical 9:16 aspect ratio"
    ]
    base = prompt.strip()
    return f"{base}, {', '.join(keywords)}"

def create_fallback_image(prompt: str, output_path: Path, scene_number: int):
    """Creates a high-resolution aesthetic fallback image if internet/API fails."""
    img = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), color=(15, 12, 28))
    draw = ImageDraw.Draw(img)

    for y in range(IMAGE_HEIGHT):
        r = int(15 + (y / IMAGE_HEIGHT) * 45)
        g = int(12 + (y / IMAGE_HEIGHT) * 35)
        b = int(28 + (y / IMAGE_HEIGHT) * 65)
        draw.line([(0, y), (IMAGE_WIDTH, y)], fill=(r, g, b))

    center_x, center_y = IMAGE_WIDTH // 2, IMAGE_HEIGHT // 3
    for radius in range(350, 0, -20):
        gold_color = (255, 215, 0)
        draw.ellipse(
            [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
            outline=gold_color,
            width=2
        )

    try:
        font = ImageFont.load_default()
    except Exception:
        font = None

    draw.text(
        (IMAGE_WIDTH // 2 - 80, IMAGE_HEIGHT // 2 + 100),
        f"SCENE {scene_number}",
        fill=(255, 255, 255),
        font=font
    )
    img.save(output_path, "JPEG", quality=95)

def generate_scene_image(
    prompt: str,
    output_path: Path,
    scene_number: int = 1,
    width: int = IMAGE_WIDTH,
    height: int = IMAGE_HEIGHT,
    model: str = "turbo",
    max_retries: int = 2
) -> Path:
    """
    Downloads an AI-generated vertical image from Pollinations API.
    Saves to output_path.
    """
    enhanced = enhance_biblical_prompt(prompt)
    encoded_prompt = urllib.parse.quote(enhanced)
    seed = random.randint(10000, 999999)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&model={model}&nologo=true&seed={seed}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for attempt in range(1, max_retries + 1):
        try:
            print(f"  [+] Generating scene {scene_number} image (attempt {attempt}/{max_retries})...")
            response = requests.get(url, headers=headers, timeout=35)
            if response.status_code == 200 and len(response.content) > 1000:
                with open(output_path, "wb") as f:
                    f.write(response.content)
                with Image.open(output_path) as img:
                    img.verify()
                print(f"  [✓] Scene {scene_number} image saved.")
                return output_path
        except Exception as e:
            print(f"  [!] Error on attempt {attempt}: {e}")
            time.sleep(1)

    print(f"  [!] Generation failed after {max_retries} attempts. Using fallback visual.")
    create_fallback_image(prompt, output_path, scene_number)
    return output_path
