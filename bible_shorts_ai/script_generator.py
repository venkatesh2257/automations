import json
import os
import random
from dataclasses import dataclass, asdict
from typing import List, Optional
import google.genai as genai
from config import GEMINI_API_KEY

@dataclass
class Scene:
    scene_id: int
    narration: str
    visual_prompt: str

@dataclass
class BiblicalShortStory:
    topic: str
    title: str
    moral: str
    scenes: List[Scene]
    full_narration: str
    youtube_title: str
    youtube_description: str
    youtube_tags: List[str]

# Rich built-in curated stories
FALLBACK_STORIES = [
    {
        "topic": "Genesis 1: The Creation of Light & Cosmos",
        "title": "Genesis 1 (Part 1/3): When God Spoke Light into the Void",
        "moral": "Even in total darkness and chaos, God's word brings divine order and light.",
        "scenes": [
            {
                "scene_id": 1,
                "narration": "In the beginning, before time or space existed, the universe was formless, empty, and wrapped in infinite black darkness.",
                "visual_prompt": "Cosmic primordial abyss of swirling dark mist and cosmic dust, deep infinite space, divine mystical light beginning to glow from a distance, 8k vertical 9:16 cinematic lighting"
            },
            {
                "scene_id": 2,
                "narration": "The Spirit of God hovered over the face of the deep waters. And then, God spoke three words: 'Let there be light.'",
                "visual_prompt": "Divine celestial aura hovering over a mysterious cosmic ocean of glowing starlight, massive golden volumetric rays piercing the dark void, majestic, 8k vertical 9:16"
            },
            {
                "scene_id": 3,
                "narration": "A blinding explosion of holy brilliance shattered the darkness, creating the first day and separating light from darkness.",
                "visual_prompt": "Magnificent cosmic supernova of pure golden divine light erupting across the cosmos, nebula clouds of blue and gold, ultra-detailed photorealistic, 8k vertical 9:16"
            },
            {
                "scene_id": 4,
                "narration": "Next, God spoke the atmosphere and skies into being, dividing the waters below from the waters above.",
                "visual_prompt": "Planet earth forming with majestic glowing blue oceans and sweeping atmosphere clouds beneath a starry heaven, cinematic space view, 8k vertical 9:16"
            },
            {
                "scene_id": 5,
                "narration": "The lesson? No matter how dark your life feels, God's light is always powerful enough to speak life into your darkness.",
                "visual_prompt": "A person standing on a mountain ridge at sunrise with golden sunlight washing over them, peaceful, uplifting, spiritual, cinematic, 8k vertical 9:16"
            }
        ],
        "youtube_title": "Genesis 1 (Part 1/3): The Creation of Light #shorts #bible #genesis",
        "youtube_description": "Chapter 1 of Genesis: When God spoke light into the void. Part 1 of our complete Genesis to Revelation series.\n\nSubscribe to read the entire Bible chapter by chapter!\n#bible #genesis #faith #shorts",
        "youtube_tags": ["genesis 1", "creation", "bible chapter", "the bible in order", "christianity", "shorts", "genesis"]
    },
    {
        "topic": "Genesis 1: Creation of Earth & Nature",
        "title": "Genesis 1 (Part 2/3): The Architecture of Earth & the Stars",
        "moral": "Everything in nature is designed with divine precision and purpose.",
        "scenes": [
            {
                "scene_id": 1,
                "narration": "On the third day of creation, God commanded the waters to gather together, and dry land surged up from the oceans.",
                "visual_prompt": "Towering ancient mountain ranges and emerald continents rising dramatically out of crystal blue oceans, waves crashing, epic cinematic scale, 8k vertical 9:16"
            },
            {
                "scene_id": 2,
                "narration": "Instantly, the earth burst into life with vibrant green vegetation, fruit trees, and blooming plants of every kind.",
                "visual_prompt": "Lush prehistoric forest bursting with ancient vibrant trees, glowing flowers, waterfalls, paradise on earth, mystical golden hour sunlight, 8k vertical 9:16"
            },
            {
                "scene_id": 3,
                "narration": "Then on the fourth day, God placed lights in the expanse of heaven: the blazing sun to rule the day, and the moon and stars for the night.",
                "visual_prompt": "Spectacular night sky filled with millions of sparkling stars, glowing milky way galaxy and a radiant golden moon overlooking pristine earth, 8k vertical 9:16"
            },
            {
                "scene_id": 4,
                "narration": "These celestial bodies were set to govern the seasons, days, and years, establishing divine rhythm across the cosmos.",
                "visual_prompt": "Orbiting sun and celestial constellations spinning gracefully around earth in cosmic harmony, hyper-detailed cosmic art, 8k vertical 9:16"
            },
            {
                "scene_id": 5,
                "narration": "The moral? If God placed every star in the sky with intention, He has an intentional purpose for your life too.",
                "visual_prompt": "A silhouette looking up in awe at the glowing starry night sky on a peaceful hillside, inspiring, awe-inspiring, 8k vertical 9:16"
            }
        ],
        "youtube_title": "Genesis 1 (Part 2/3): The Architecture of Earth & Stars #shorts #genesis",
        "youtube_description": "Genesis Chapter 1 Part 2: Creation of land, oceans, vegetation, and the celestial cosmos.\n\nFollow along as we journey through the entire Bible chapter by chapter!\n#bible #genesis #faith #history #shorts",
        "youtube_tags": ["genesis 1 part 2", "bible story", "creation of stars", "bible in 365 days", "shorts", "faith"]
    },
    {
        "topic": "Genesis 1: Creation of Living Creatures & Humanity",
        "title": "Genesis 1 (Part 3/3): The Masterpiece of Creation - Man",
        "moral": "You are not an accident. You are created in the image of God with divine dignity.",
        "scenes": [
            {
                "scene_id": 1,
                "narration": "On the fifth and sixth days, the waters teemed with living creatures, birds filled the skies, and majestic beasts walked the land.",
                "visual_prompt": "Magnificent ancient sea creatures in clear azure waters and colorful birds flying over verdant valleys, peaceful majestic wildlife, 8k vertical 9:16"
            },
            {
                "scene_id": 2,
                "narration": "Then God said something extraordinary: 'Let us make mankind in our image, in our likeness, to rule over the earth.'",
                "visual_prompt": "Divine rays of heavenly golden light beaming down onto the pristine earth, sacred holy atmosphere, angels watching in reverence, 8k vertical 9:16"
            },
            {
                "scene_id": 3,
                "narration": "God created man and woman, breathed life into them, and blessed them to be fruitful and multiply.",
                "visual_prompt": "First humans standing in the pristine radiant Garden of Eden surrounded by majestic animals and glowing nature, innocent, regal, majestic, 8k vertical 9:16"
            },
            {
                "scene_id": 4,
                "narration": "God saw everything He had made, and behold, it was not just good—it was very good. Thus the heavens and earth were completed.",
                "visual_prompt": "Panoramic sunset over the entire pristine creation, glowing golden skies, calm rivers, majestic mountains in harmony, 8k vertical 9:16"
            },
            {
                "scene_id": 5,
                "narration": "Never forget: You carry the image of the Creator. Walk with dignity, purpose, and reverence for God's creation.",
                "visual_prompt": "A close-up profile of a person looking forward with confidence and hope in golden divine sunset light, inspiring, cinematic, 8k vertical 9:16"
            }
        ],
        "youtube_title": "Genesis 1 (Part 3/3): The Creation of Man in God's Image #shorts #bible",
        "youtube_description": "Genesis Chapter 1 Part 3: The creation of living creatures, humanity, and God's divine mandate.\n\nSubscribe for the complete Chapter-by-Chapter Bible journey!\n#genesis #bible #humanity #creation #shorts",
        "youtube_tags": ["genesis 1 part 3", "creation of man", "image of god", "bible study", "shorts", "faith"]
    }
]

def generate_chapter_3part_series(book: str, chapter: int) -> List[BiblicalShortStory]:
    """
    Generates 3 sequential YouTube Shorts / Instagram Reels covering 1 Bible Chapter.
    Part 1: Setting, Context & Opening Verses (Hook)
    Part 2: The Core Event / Conflict / Divine Revelation
    Part 3: Climax, Resolution & Moral Life Lesson
    """
    print(f"\n[*] Generating 3-Part Series for: {book} Chapter {chapter}...")

    if GEMINI_API_KEY:
        try:
            client = genai.Client(api_key=GEMINI_API_KEY)
            prompt = f"""You are a master biblical scholar and viral video scriptwriter.
Write a 3-part YouTube Shorts / Instagram Reels series covering the entire chapter of {book} Chapter {chapter}.

Break the chapter into EXACTLY 3 connected parts:
- Part 1: The opening setting, hook, and initial dramatic events of {book} Chapter {chapter}.
- Part 2: The core conflict, pivotal verses, or divine action in {book} Chapter {chapter}.
- Part 3: The climax, resolution of the chapter, and the ultimate moral takeaway for modern life.

Return a JSON array of EXACTLY 3 objects with this structure:
[
  {{
    "part_number": 1,
    "topic": "{book} {chapter} (Part 1/3): Subtitle",
    "title": "{book} {chapter} (Part 1/3): Viral Short Title",
    "moral": "Concise profound moral takeaway",
    "scenes": [
      {{
        "scene_id": 1,
        "narration": "Viral retention hook sentence (under 12 words).",
        "visual_prompt": "Detailed cinematic prompt for AI image generator, vertical 9:16, cinematic biblical art, 8k, dramatic lighting..."
      }},
      {{
        "scene_id": 2,
        "narration": "Story development sentence.",
        "visual_prompt": "Detailed cinematic prompt..."
      }},
      {{
        "scene_id": 3,
        "narration": "Building tension sentence.",
        "visual_prompt": "Detailed cinematic prompt..."
      }},
      {{
        "scene_id": 4,
        "narration": "Cliffhanger or transition sentence to Part 2.",
        "visual_prompt": "Detailed cinematic prompt..."
      }},
      {{
        "scene_id": 5,
        "narration": "Moral takeaway and subscribe call to action.",
        "visual_prompt": "Uplifting spiritual cinematic prompt..."
      }}
    ],
    "youtube_title": "{book} {chapter} (Part 1/3): Viral Title #shorts #bible",
    "youtube_description": "2-3 sentence engaging description covering {book} {chapter} Part 1. Subscribe to follow the Bible chapter by chapter!",
    "youtube_tags": ["{book.lower()} {chapter}", "bible chapter", "{book.lower()}", "shorts", "bible in order", "christianity"]
  }},
  {{
    "part_number": 2,
    "topic": "{book} {chapter} (Part 2/3): Subtitle",
    "title": "{book} {chapter} (Part 2/3): Viral Short Title",
    "moral": "...",
    "scenes": [... 4 to 5 scenes ...],
    "youtube_title": "{book} {chapter} (Part 2/3): ... #shorts",
    "youtube_description": "...",
    "youtube_tags": [...]
  }},
  {{
    "part_number": 3,
    "topic": "{book} {chapter} (Part 3/3): Subtitle",
    "title": "{book} {chapter} (Part 3/3): Viral Short Title",
    "moral": "...",
    "scenes": [... 4 to 5 scenes ...],
    "youtube_title": "{book} {chapter} (Part 3/3): ... #shorts",
    "youtube_description": "...",
    "youtube_tags": [...]
  }}
]

Strict Rules:
1. Total scenes per part: 4 to 5 scenes.
2. Narration for each part must take ~40-45 seconds when read aloud.
3. Keep the storytelling accurate to scripture while deeply captivating for Shorts/Reels viewers.
4. Output ONLY valid JSON array without backticks or markdown fences.
"""
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            raw_text = response.text.strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            data_list = json.loads(raw_text.strip())
            
            stories = []
            for item in data_list:
                scenes = [Scene(**s) for s in item["scenes"]]
                full_narration = " ".join(s.narration for s in scenes)
                stories.append(BiblicalShortStory(
                    topic=item.get("topic", f"{book} {chapter}"),
                    title=item.get("title", f"{book} {chapter}"),
                    moral=item.get("moral", "Walk in faith and wisdom."),
                    scenes=scenes,
                    full_narration=full_narration,
                    youtube_title=item.get("youtube_title", f"{book} {chapter} #shorts"),
                    youtube_description=item.get("youtube_description", "Subscribe for the complete Chapter-by-Chapter Bible series!"),
                    youtube_tags=item.get("youtube_tags", ["bible", book.lower(), "shorts"])
                ))
            if len(stories) == 3:
                return stories
        except Exception as e:
            print(f"[!] Gemini chapter generator error ({e}), generating structured chapter series...")

    # Built-in contextual fallback for Genesis 1 or generic chapters
    if book.lower() == "genesis" and chapter == 1:
        stories = []
        for s in FALLBACK_STORIES:
            scenes = [Scene(**sc) for sc in s["scenes"]]
            full_narration = " ".join(sc.narration for sc in scenes)
            stories.append(BiblicalShortStory(
                topic=s["topic"],
                title=s["title"],
                moral=s["moral"],
                scenes=scenes,
                full_narration=full_narration,
                youtube_title=s["youtube_title"],
                youtube_description=s["youtube_description"],
                youtube_tags=s["youtube_tags"]
            ))
        return stories

    # Procedural 3-part fallback for any chapter
    part_themes = [
        ("The Beginning & The Divine Setting", "God reveals Himself in every circumstance.", "Listen closely to the word of God."),
        ("The Core Event & Pivotal Moment", "Faith is tested in the moments of trial.", "Stand firm in righteous action."),
        ("The Resolution & Eternal Moral", "God's promises never fail for those who trust Him.", "Honor God in all that you do.")
    ]

    stories = []
    for p_idx, (theme, moral, hook) in enumerate(part_themes, 1):
        scenes = [
            Scene(1, f"Welcome to {book} Chapter {chapter}, Part {p_idx}. {hook}", f"Ancient parchment biblical scroll of {book} glowing with divine golden starlight, 8k vertical 9:16 cinematic"),
            Scene(2, f"In this chapter, we discover profound events recorded for our wisdom and spiritual growth.", f"Ancient holy temple in biblical Jerusalem with volumetric light rays, dramatic lighting, 8k vertical 9:16"),
            Scene(3, f"The scripture reveals the sovereign hand of God guiding history and leading His people.", f"Biblical prophet speaking truth with authority on a desert plateau under divine clouds, 8k vertical 9:16"),
            Scene(4, f"Every verse of {book} {chapter} reminds us of our divine calling and purpose on earth.", f"Radiant golden light shining through storm clouds over ancient biblical land, epic scale, 8k vertical 9:16"),
            Scene(5, f"The lesson of {book} {chapter}? {moral} Follow for Part {p_idx+1 if p_idx < 3 else 'the next chapter'}!", f"Peaceful sunrise over the hills of Galilee, uplifting, hopeful, inspirational, 8k vertical 9:16")
        ]
        full_narration = " ".join(s.narration for s in scenes)
        stories.append(BiblicalShortStory(
            topic=f"{book} {chapter} (Part {p_idx}/3): {theme}",
            title=f"{book} {chapter} (Part {p_idx}/3) - The Bible in Order",
            moral=moral,
            scenes=scenes,
            full_narration=full_narration,
            youtube_title=f"{book} {chapter} (Part {p_idx}/3): {theme} #shorts #bible",
            youtube_description=f"Journey through the Bible from Genesis to Revelation! Here is {book} Chapter {chapter} Part {p_idx}/3.\n\nSubscribe to read the entire Bible chapter by chapter with us!\n#bible #{book.lower()} #faith #shorts",
            youtube_tags=["bible", book.lower(), f"{book.lower()} {chapter}", "bible in order", "shorts", "faith"]
        ))

    return stories

def generate_biblical_story(topic: str = None) -> BiblicalShortStory:
    """Wrapper for single story generation."""
    stories = generate_chapter_3part_series("Genesis", 1)
    return stories[0]
