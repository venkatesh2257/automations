import os
import re
import io
import time
import random
import urllib.parse
import requests
from pathlib import Path
from typing import List, Optional
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from config import (
    IMAGE_WIDTH,
    IMAGE_HEIGHT,
    IMAGE_MODEL,
    TEMP_DIR,
    CACHE_DIR,
    PEXELS_API_KEY
)

# Common AI noise words to strip when searching stock libraries
AI_NOISE_WORDS = {
    "8k", "4k", "cinematic", "photorealistic", "hyperrealistic", "ultra-detailed",
    "hyper-detailed", "vertical", "9:16", "aspect", "ratio", "volumetric", "lighting",
    "chiaroscuro", "trending", "artstation", "octane", "render", "unreal", "engine",
    "detailed", "intricate", "textures", "masterpiece", "epic", "dramatic", "scene",
    "prompt", "resolution", "hd", "realism", "high"
}

def clean_text_for_search(text: str) -> str:
    """Removes punctuation and AI prompt noise words to extract clean search tokens."""
    cleaned = re.sub(r"[^a-zA-Z0-9\s]", " ", text).lower()
    tokens = [w for w in cleaned.split() if len(w) > 2 and w not in AI_NOISE_WORDS]
    return " ".join(tokens)

def extract_search_queries(prompt: str, narration: str = "") -> List[str]:
    """
    Extracts ordered candidate stock search queries tailored for Pexels / Unsplash
    from the scene visual prompt and narration.
    """
    combined = f"{prompt} {narration}".lower()
    queries = []

    # Semantic Biblical & Visual Theme Mappings
    if any(w in combined for w in ["scroll", "parchment", "scripture", "book", "verses"]):
        queries.extend(["ancient holy bible scroll", "old parchment paper texture", "open bible sunlight"])
    if any(w in combined for w in ["temple", "sanctuary", "altar", "holy place", "tabernacle"]):
        queries.extend(["ancient stone temple jerusalem", "ancient stone temple ruins", "golden rays cathedral interior"])
    if any(w in combined for w in ["space", "cosmos", "universe", "abyss", "void", "stars", "constellation", "nebula"]):
        queries.extend(["deep space cosmos stars", "galaxy nebula starry night sky", "milky way starry sky"])
    if any(w in combined for w in ["ocean", "sea", "water", "waves", "flood", "deep waters", "tsunami"]):
        queries.extend(["dramatic ocean waves sunlight", "deep blue sea water", "dramatic ocean storm waves"])
    if any(w in combined for w in ["garden", "eden", "forest", "trees", "plants", "vegetation", "flowers"]):
        queries.extend(["lush green paradise garden", "mystical ancient forest sun rays", "sunlight through forest trees"])
    if any(w in combined for w in ["sunrise", "sunset", "dawn", "morning", "golden hour"]):
        queries.extend(["golden sunrise clouds mountains", "dramatic sunset golden hour sky", "sun rays through clouds"])
    if any(w in combined for w in ["mountain", "hills", "sinai", "ararat", "plateau", "ridge"]):
        queries.extend(["majestic mountain clouds peak", "dramatic mountain landscape sunrise", "misty mountain peaks"])
    if any(w in combined for w in ["cloud", "clouds", "sky", "storm", "heavens", "thunder", "lightning"]):
        queries.extend(["dramatic storm clouds sky", "golden sunset clouds heaven", "cumulus clouds blue sky"])
    if any(w in combined for w in ["desert", "sand", "wilderness", "dunes", "arid"]):
        queries.extend(["desert sand dunes sunset", "vast golden desert landscape", "desert rocks sun"])
    if any(w in combined for w in ["fire", "flame", "burning", "smoke", "sparks", "inferno"]):
        queries.extend(["fire flames glowing dark", "burning bonfire sparks", "campfire flame night"])
    if any(w in combined for w in ["praying", "prayer", "worship", "prophet", "faith", "hope", "kneeling", "spiritual"]):
        queries.extend(["person praying mountain sunrise", "spiritual worship sunlight hands", "peaceful meditation sunrise"])
    if any(w in combined for w in ["cross", "crucifixion", "salvation", "jesus", "christ"]):
        queries.extend(["holy cross sunset silhouette", "open bible sunlight cross", "ancient church stone cross"])
    if any(w in combined for w in ["dove", "bird", "birds"]):
        queries.extend(["white dove flying sky", "dove flight peaceful sky", "birds flying golden sunset"])
    if any(w in combined for w in ["lion", "beast", "creature", "wildlife", "sheep", "flock", "shepherd"]):
        queries.extend(["majestic lion wilderness", "shepherd sheep green pasture", "wild animals nature"])
    if any(w in combined for w in ["city", "jerusalem", "ancient city", "walls", "gates"]):
        queries.extend(["ancient stone city jerusalem", "ancient middle eastern ruins", "historic stone fortress"])
    if any(w in combined for w in ["night", "moon", "darkness", "midnight"]):
        queries.extend(["full moon night clouds sky", "starry night sky landscape", "mystical dark night sky"])
    if any(w in combined for w in ["rainbow"]):
        queries.extend(["vibrant rainbow sky clouds", "rainbow over mountains landscape"])
    if any(w in combined for w in ["harvest", "wheat", "grain", "field"]):
        queries.extend(["golden wheat field sunset", "golden harvest field sunlight"])
    if any(w in combined for w in ["angel", "angels", "divine light", "holy", "brilliance", "celestial"]):
        queries.extend(["divine golden light rays heaven", "angelic golden clouds sunset", "sunbeams breaking through clouds"])

    # Extract clean tokens from the prompt as a fallback query
    clean_tokens = clean_text_for_search(prompt).split()
    if clean_tokens:
        queries.append(" ".join(clean_tokens[:4]))
        if len(clean_tokens) >= 3:
            queries.append(" ".join(clean_tokens[1:4]))

    # Universal atmospheric fallbacks
    queries.extend([
        "ancient holy bible sunlight",
        "golden sunrise mountain landscape",
        "dramatic sun rays clouds sky",
        "peaceful nature landscape sunlight"
    ])

    # Deduplicate while preserving order
    seen = set()
    unique_queries = []
    for q in queries:
        q_norm = q.strip().lower()
        if q_norm and q_norm not in seen:
            seen.add(q_norm)
            unique_queries.append(q_norm)

    return unique_queries

def crop_and_resize_to_vertical(
    img: Image.Image,
    target_w: int = IMAGE_WIDTH,
    target_h: int = IMAGE_HEIGHT
) -> Image.Image:
    """
    Center-crops and resizes an image to the vertical 9:16 target dimensions
    using high-fidelity Lanczos resampling with zero stretching.
    """
    if img.mode != "RGB":
        img = img.convert("RGB")

    orig_w, orig_h = img.size
    target_aspect = target_w / target_h
    orig_aspect = orig_w / orig_h

    if orig_aspect > target_aspect:
        # Image is wider than 9:16 -> center crop width
        new_w = int(orig_h * target_aspect)
        left = (orig_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, orig_h))
    else:
        # Image is taller than 9:16 -> center crop height
        new_h = int(orig_w / target_aspect)
        top = (orig_h - new_h) // 2
        img = img.crop((0, top, orig_w, top + new_h))

    return img.resize((target_w, target_h), Image.Resampling.LANCZOS)

def search_and_download_pexels_photo(
    queries: List[str],
    output_path: Path,
    scene_number: int = 1,
    seed_offset: int = 0
) -> bool:
    """
    Searches Pexels Photo API for high-resolution 4K/HD portrait imagery,
    processes it to 1080x1920 Lanczos, and saves to output_path.
    """
    if not PEXELS_API_KEY:
        return False

    headers = {"Authorization": PEXELS_API_KEY}

    for query in queries[:6]:
        # 1. Try portrait orientation first
        url = f"https://api.pexels.com/v1/search?query={urllib.parse.quote(query)}&orientation=portrait&per_page=15"
        try:
            r = requests.get(url, headers=headers, timeout=12)
            if r.status_code == 200:
                photos = r.json().get("photos", [])
                if not photos:
                    # Try landscape orientation as fallback (will be center cropped)
                    url_land = f"https://api.pexels.com/v1/search?query={urllib.parse.quote(query)}&per_page=10"
                    r_land = requests.get(url_land, headers=headers, timeout=10)
                    if r_land.status_code == 200:
                        photos = r_land.json().get("photos", [])

                if photos:
                    # Pick diverse photo per scene
                    pick_idx = (scene_number * 2 + seed_offset) % len(photos)
                    photo = photos[pick_idx]
                    src = photo.get("src", {})

                    # Select highest quality source URL
                    img_url = (
                        src.get("large2x")
                        or src.get("original")
                        or src.get("large")
                        or src.get("portrait")
                        or src.get("medium")
                    )

                    if img_url:
                        print(f"  [Pexels 4K] Downloading '{query}' (Photo ID: {photo.get('id')})...")
                        img_resp = requests.get(img_url, timeout=25)
                        if img_resp.status_code == 200 and len(img_resp.content) > 5000:
                            img = Image.open(io.BytesIO(img_resp.content))
                            processed_img = crop_and_resize_to_vertical(img, IMAGE_WIDTH, IMAGE_HEIGHT)
                            processed_img.save(output_path, "JPEG", quality=95)
                            print(f"  [✓] Scene {scene_number} Pexels image saved ({output_path.stat().st_size // 1024} KB).")
                            return True
        except Exception as e:
            print(f"  [!] Pexels search error for '{query}': {e}")
            continue

    return False

def search_and_download_unsplash_photo(
    queries: List[str],
    output_path: Path,
    scene_number: int = 1
) -> bool:
    """
    Downloads high-resolution photography from Unsplash Source API.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for query in queries[:4]:
        clean_q = urllib.parse.quote(query)
        search_url = f"https://source.unsplash.com/featured/{IMAGE_WIDTH}x{IMAGE_HEIGHT}?{clean_q}"
        try:
            resp = requests.get(search_url, headers=headers, timeout=15, allow_redirects=True)
            if resp.status_code == 200 and len(resp.content) > 20000:
                img = Image.open(io.BytesIO(resp.content))
                processed_img = crop_and_resize_to_vertical(img, IMAGE_WIDTH, IMAGE_HEIGHT)
                processed_img.save(output_path, "JPEG", quality=95)
                print(f"  [✓] Scene {scene_number} Unsplash photo saved.")
                return True
        except Exception:
            continue

    return False

def search_and_download_wikimedia_art(
    queries: List[str],
    output_path: Path,
    scene_number: int = 1
) -> bool:
    """
    Searches Wikimedia Commons for high-resolution public-domain historic Biblical art
    (Gustave Doré, Michelangelo, Rembrandt, Caravaggio, etc.).
    """
    headers = {"User-Agent": "BibleShortsBot/2.0 (contact@example.com)"}
    for q in queries[:3]:
        search_term = f"{q} painting"
        api_url = (
            f"https://commons.wikimedia.org/w/api.php?action=query&generator=search"
            f"&gsrsearch={urllib.parse.quote(search_term)}&gsrlimit=5&prop=imageinfo"
            f"&iiprop=url|size&format=json"
        )
        try:
            r = requests.get(api_url, headers=headers, timeout=10)
            if r.status_code == 200:
                pages = r.json().get("query", {}).get("pages", {})
                for page_id, page in pages.items():
                    info_list = page.get("imageinfo", [])
                    if info_list:
                        file_url = info_list[0].get("url")
                        if file_url and any(file_url.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png"]):
                            img_resp = requests.get(file_url, headers=headers, timeout=20)
                            if img_resp.status_code == 200 and len(img_resp.content) > 30000:
                                img = Image.open(io.BytesIO(img_resp.content))
                                processed_img = crop_and_resize_to_vertical(img, IMAGE_WIDTH, IMAGE_HEIGHT)
                                processed_img.save(output_path, "JPEG", quality=95)
                                print(f"  [✓] Scene {scene_number} Wikimedia Biblical Art saved.")
                                return True
        except Exception:
            continue
    return False

def generate_ai_3d_cartoon(
    prompt: str,
    output_path: Path,
    scene_number: int = 1,
    width: int = IMAGE_WIDTH,
    height: int = IMAGE_HEIGHT,
    max_retries: int = 2
) -> bool:
    """
    Generates viral 3D Disney/Pixar & Dreamworks animation style cartoon visuals
    using AI models with vivid volumetric lighting and expressive characters.
    """
    style_keywords = (
        "3d disney pixar animation movie style, cute expressive 3d character design, "
        "vibrant saturated colors, volumetric golden sunbeams, magical atmosphere, "
        "unreal engine 5 3d cartoon render, vertical 9:16"
    )
    full_prompt = f"{prompt.strip()}, {style_keywords}"
    encoded = urllib.parse.quote(full_prompt)
    seed = random.randint(1000, 999999)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # Cascade through supported models
    for model in ["flux", "turbo", "sana"]:
        url = f"https://image.pollinations.ai/prompt/{encoded}?width=576&height=1024&model={model}&nologo=true&seed={seed}"
        try:
            print(f"  [AI 3D Cartoon] Generating Scene {scene_number} with model={model}...")
            response = requests.get(url, headers=headers, timeout=22)
            if response.status_code == 200 and len(response.content) > 10000:
                img = Image.open(io.BytesIO(response.content)).convert("RGB")
                img_hd = crop_and_resize_to_vertical(img, width, height)
                # Boost vibrance & sharpness for animated pop
                img_hd = ImageEnhance.Color(img_hd).enhance(1.15)
                img_hd = ImageEnhance.Sharpness(img_hd).enhance(1.20)
                img_hd.save(output_path, "JPEG", quality=95)
                print(f"  [✓] Scene {scene_number} AI 3D Cartoon saved ({output_path.stat().st_size // 1024} KB).")
                return True
        except Exception as e:
            print(f"  [!] AI Cartoon model {model} error: {e}")
            continue

    return False

def generate_flux_ai_image(
    prompt: str,
    output_path: Path,
    scene_number: int = 1,
    width: int = IMAGE_WIDTH,
    height: int = IMAGE_HEIGHT,
    max_retries: int = 2
) -> bool:
    """
    Generates high-fidelity AI imagery using the Pollinations FLUX.1 engine.
    """
    return generate_ai_3d_cartoon(prompt, output_path, scene_number=scene_number, width=width, height=height, max_retries=max_retries)

def create_fallback_image(prompt: str, output_path: Path, scene_number: int):
    """
    Creates a high-resolution aesthetic dark/golden geometric visual as ultimate fallback.
    """
    img = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), color=(12, 10, 24))
    draw = ImageDraw.Draw(img)

    # Vertical gradient
    for y in range(IMAGE_HEIGHT):
        r = int(12 + (y / IMAGE_HEIGHT) * 45)
        g = int(10 + (y / IMAGE_HEIGHT) * 35)
        b = int(24 + (y / IMAGE_HEIGHT) * 60)
        draw.line([(0, y), (IMAGE_WIDTH, y)], fill=(r, g, b))

    # Sacred golden rings
    center_x, center_y = IMAGE_WIDTH // 2, IMAGE_HEIGHT // 3
    for radius in range(360, 40, -30):
        gold = (255, 215, 0)
        draw.ellipse(
            [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
            outline=gold,
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
    narration: str = "",
    width: int = IMAGE_WIDTH,
    height: int = IMAGE_HEIGHT,
    model: str = IMAGE_MODEL,
    max_retries: int = 2
) -> Path:
    """
    Main Visual Generator Engine:
    1. Primary: AI 3D Cartoon / Animation Visual Generator (Pixar / Disney 3D style for viral engagement).
    2. Tier 2: Pexels 4K / 3D Animated Stock Visuals.
    3. Tier 3: Unsplash & Wikimedia Classical Fine Art Masterpieces.
    4. Tier 4: Sacred Procedural Canvas.
    """
    # 1. Primary: AI 3D Cartoon Generator
    if generate_ai_3d_cartoon(prompt, output_path, scene_number=scene_number, width=width, height=height, max_retries=max_retries):
        return output_path

    # 2. Tier 2: Pexels 4K / 3D Animation Stock Fallback
    queries = extract_search_queries(prompt, narration=narration)
    if PEXELS_API_KEY:
        if search_and_download_pexels_photo(queries, output_path, scene_number=scene_number):
            return output_path

    # 3. Tier 3: Unsplash
    if search_and_download_unsplash_photo(queries, output_path, scene_number=scene_number):
        return output_path

    # 4. Tier 4: Wikimedia Classical Art
    if search_and_download_wikimedia_art(queries, output_path, scene_number=scene_number):
        return output_path

    # 5. Ultimate Fallback
    print(f"  [!] Using aesthetic procedural canvas for Scene {scene_number}.")
    create_fallback_image(prompt, output_path, scene_number)
    return output_path


