import json
import datetime
from pathlib import Path
from typing import Tuple, Dict
from config import BASE_DIR
from bible_index import get_next_chapter

PROGRESS_FILE = BASE_DIR / "bible_progress.json"

def init_progress() -> Dict:
    """Initializes default progress tracking at Genesis Chapter 1."""
    default_data = {
        "current_book": "Genesis",
        "current_chapter": 1,
        "total_videos_created": 0,
        "last_updated": None,
        "completed_chapters": []
    }
    save_progress(default_data)
    return default_data

def load_progress() -> Dict:
    """Loads current Bible chapter progress from JSON."""
    if not PROGRESS_FILE.exists():
        return init_progress()
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return init_progress()

def save_progress(data: Dict):
    """Saves progress dictionary to JSON."""
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def get_current_reading() -> Tuple[str, int]:
    """Returns the current book and chapter to process."""
    data = load_progress()
    return data.get("current_book", "Genesis"), data.get("current_chapter", 1)

def set_reading_position(book: str, chapter: int):
    """Allows jumping or resetting to a specific book and chapter."""
    data = load_progress()
    data["current_book"] = book
    data["current_chapter"] = int(chapter)
    data["last_updated"] = datetime.datetime.now().isoformat()
    save_progress(data)
    print(f"[*] Bible progress set to: {book} Chapter {chapter}")

def mark_chapter_completed(book: str, chapter: int, video_count: int = 3):
    """Marks the current chapter as completed and moves progress to the next chapter."""
    data = load_progress()
    now_str = datetime.datetime.now().isoformat()
    
    data["completed_chapters"].append({
        "book": book,
        "chapter": chapter,
        "completed_at": now_str,
        "parts_generated": video_count
    })
    data["total_videos_created"] = data.get("total_videos_created", 0) + video_count
    data["last_updated"] = now_str
    
    # Calculate next chapter in sequence
    next_book, next_ch = get_next_chapter(book, chapter)
    data["current_book"] = next_book
    data["current_chapter"] = next_ch
    
    save_progress(data)
    print(f"[✓] Completed {book} Chapter {chapter}!")
    print(f"[*] Next Up for Tomorrow: {next_book} Chapter {next_ch}")
    return next_book, next_ch
