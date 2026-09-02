import json
import datetime
from pathlib import Path
from typing import Dict, Tuple
from config import BASE_DIR
from curricula import AVAILABLE_COURSES

PROGRESS_FILE = BASE_DIR / "course_progress.json"

def init_progress() -> Dict:
    """Initializes course tracking with Git Masterclass at Lesson 1."""
    data = {
        "active_course": "git_masterclass",
        "current_lesson": 1,
        "courses_progress": {
            "git_masterclass": {"current_lesson": 1, "completed": []},
            "devops_cloud": {"current_lesson": 1, "completed": []},
            "mobile_dev": {"current_lesson": 1, "completed": []}
        },
        "total_videos_created": 0,
        "last_updated": None
    }
    save_progress(data)
    return data

def load_progress() -> Dict:
    """Loads course progress from JSON."""
    if not PROGRESS_FILE.exists():
        return init_progress()
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return init_progress()

def save_progress(data: Dict):
    """Saves course progress to JSON."""
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def get_active_course_and_lesson() -> Tuple[str, int]:
    """Returns the current active course ID and lesson number."""
    data = load_progress()
    course_id = data.get("active_course", "git_masterclass")
    course_data = data.get("courses_progress", {}).get(course_id, {})
    lesson_num = course_data.get("current_lesson", 1)
    return course_id, lesson_num

def set_course_and_lesson(course_id: str, lesson_num: int):
    """Sets active course and lesson number."""
    data = load_progress()
    course_id = course_id.lower()
    data["active_course"] = course_id
    if course_id not in data.get("courses_progress", {}):
        data["courses_progress"][course_id] = {"current_lesson": 1, "completed": []}
    data["courses_progress"][course_id]["current_lesson"] = int(lesson_num)
    data["last_updated"] = datetime.datetime.now().isoformat()
    save_progress(data)
    print(f"[*] Course tracker set to: {course_id} Lesson {lesson_num}")

def mark_lesson_completed(course_id: str, lesson_num: int, max_lessons: int):
    """Marks lesson completed and advances pointer to next lesson."""
    data = load_progress()
    now_str = datetime.datetime.now().isoformat()
    
    c_data = data["courses_progress"].setdefault(course_id, {"current_lesson": 1, "completed": []})
    c_data["completed"].append({
        "lesson_number": lesson_num,
        "completed_at": now_str
    })
    
    data["total_videos_created"] = data.get("total_videos_created", 0) + 1
    data["last_updated"] = now_str

    if lesson_num < max_lessons:
        c_data["current_lesson"] = lesson_num + 1
        next_lesson = lesson_num + 1
    else:
        # Course finished!
        c_data["current_lesson"] = 1
        next_lesson = 1
        print(f"\n🎉 CONGRATULATIONS! You have completed the entire {course_id} course!")

    save_progress(data)
    print(f"[✓] Marked {course_id} Lesson {lesson_num} as Completed!")
    print(f"[*] Next Scheduled Lesson: Lesson {next_lesson}")
    return next_lesson
