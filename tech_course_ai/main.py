#!/usr/bin/env python3
import argparse
import sys
import time
import json
from pathlib import Path
from config import BASE_DIR, OUTPUT_DIR, TEMP_DIR, VIDEO_WIDTH, VIDEO_HEIGHT
from curricula import AVAILABLE_COURSES, get_course
from script_engine import generate_pro_teacher_script, TechLessonScript
from tts_engine import generate_teacher_narration
from slide_renderer import render_slide_by_type
from video_composer import composite_master_course_video
from course_manager import (
    get_active_course_and_lesson,
    mark_lesson_completed,
    set_course_and_lesson,
    load_progress
)

def run_course_pipeline(
    course_name: str = None,
    lesson_number: int = None,
    output_name: str = None
) -> Path:
    """
    Executes the complete Pro-Teacher Technical Course Video Generation Pipeline.
    Uses 100% Real Human Voice (ElevenLabs) + Real 1080p Motion Video Footage.
    """
    start_time = time.time()
    timestamp = int(time.time())

    # 1. Determine Course and Lesson
    active_course_id, active_lesson_num = get_active_course_and_lesson()
    target_course_id = course_name.lower() if course_name else active_course_id
    target_lesson_num = lesson_number if lesson_number else active_lesson_num

    course_data = get_course(target_course_id)
    lessons_list = course_data.get("lessons", [])
    
    # Find matching lesson info
    matching_lessons = [l for l in lessons_list if l["lesson_number"] == target_lesson_num]
    if matching_lessons:
        lesson_data = matching_lessons[0]
    else:
        lesson_data = lessons_list[0] if lessons_list else {
            "lesson_number": 1,
            "title": "Introduction to Architecture",
            "concept": "Foundational technical mechanics",
            "analogy": "Building blocks of modern software",
            "key_commands": ["tech --version"],
            "difficulty": "Beginner"
        }

    print("\n" + "=" * 68)
    print("   PRO-TEACHER CINEMATIC TECH VIDEO ENGINE (ELEVENLABS + 1080P MOTION)")
    print("=" * 68)
    print(f"  • Course : {course_data.get('title')}")
    print(f"  • Lesson : #{lesson_data.get('lesson_number')} - {lesson_data.get('title')}")
    print(f"  • Voice  : ElevenLabs 100% Human Studio Voice")
    print(f"  • Visual : Real 1080p Motion Video + Glassmorphic HUD Overlays")
    print("=" * 68)

    # 2. Generate Pro-Teacher Feynman Script
    print("\n[Step 1/4] Writing High-Clarity Feynman Script & Storyboard...")
    script: TechLessonScript = generate_pro_teacher_script(course_data, lesson_data)
    print(f"  [✓] Script Ready: {len(script.sections)} Educational Acts")
    print(f"  • Analogy: {script.analogy}")

    # 3. Generate 100% Human Studio Voiceover (ElevenLabs)
    print("\n[Step 2/4] Synthesizing 100% Human Studio Voiceover (ElevenLabs)...")
    audio_paths = []
    for idx, sec in enumerate(script.sections):
        audio_file = TEMP_DIR / f"sec_audio_{target_course_id}_{target_lesson_num}_{sec.section_id}_{timestamp}.mp3"
        generate_teacher_narration(sec.narration, audio_file)
        audio_paths.append(audio_file)
        print(f"  [+] Section {sec.section_id} (ElevenLabs Voice): {sec.section_name}")

    # 4. Render Razor-Sharp Transparent Glassmorphic HUD Overlays
    print("\n[Step 3/4] Rendering Transparent Code & Terminal Glassmorphic HUDs...")
    hud_paths = []
    section_titles = []
    broll_queries = []
    
    for idx, sec in enumerate(script.sections):
        hud_file = TEMP_DIR / f"sec_hud_{target_course_id}_{target_lesson_num}_{sec.section_id}_{timestamp}.png"
        render_slide_by_type(
            course_name=course_data.get("title", "Masterclass"),
            lesson_str=f"Lesson {target_lesson_num}: {sec.section_name}",
            visual_type=sec.visual_type,
            slide_title=sec.visual_title,
            code_content=sec.code_content,
            bullet_points=sec.bullet_points,
            output_path=hud_file
        )
        hud_paths.append(hud_file)
        section_titles.append(sec.section_name)
        broll_queries.append(sec.broll_query if sec.broll_query else "technology server network")
        print(f"  [+] HUD {sec.section_id} ({sec.visual_type}): {sec.visual_title}")

    # 5. Composite Real Motion Video & Chapter Markers
    print("\n[Step 4/4] Compositing 1080p Real-Motion Video + Audio + Glassmorphism HUD...")
    safe_course = "".join(c for c in target_course_id if c.isalnum()).lower()
    if not output_name:
        final_video_name = f"{safe_course}_lesson_{target_lesson_num}_cinematic_{timestamp}.mp4"
    else:
        final_video_name = output_name

    final_video_path = OUTPUT_DIR / final_video_name
    master_video, chapters = composite_master_course_video(
        broll_queries=broll_queries,
        hud_overlay_paths=hud_paths,
        audio_paths=audio_paths,
        section_names=section_titles,
        output_video_path=final_video_path
    )

    # 6. Advance Course Progression
    max_lessons = len(lessons_list) if lessons_list else 15
    next_lesson = mark_lesson_completed(target_course_id, target_lesson_num, max_lessons)

    # 7. Print YouTube Description & Timestamps
    print("\n" + "=" * 68)
    print(" 🎬 CINEMATIC 1080P VIDEO READY FOR YOUTUBE / INSTAGRAM!")
    print(f" • File Path : {final_video_path.resolve()}")
    print("=" * 68)
    print("\n📋 GENERATED YOUTUBE CHAPTER TIMESTAMPS:")
    print("-" * 50)
    for ch in chapters:
        print(f"{ch['timestamp']} {ch['title']}")
    print("-" * 50)

    elapsed = time.time() - start_time
    print(f"\n[✓] Completed in {elapsed:.1f} seconds! Ready to publish.\n")
    return final_video_path

def main():
    parser = argparse.ArgumentParser(
        description="Autonomous Pro-Teacher Cinematic Technical Course Video Generator"
    )
    parser.add_argument(
        "--course",
        type=str,
        default=None,
        help="Course ID (e.g. git, devops, mobile)"
    )
    parser.add_argument(
        "--lesson",
        type=int,
        default=None,
        help="Lesson number to generate (e.g. 1, 2, 3)"
    )
    parser.add_argument(
        "--set-position",
        nargs=2,
        metavar=("COURSE", "LESSON"),
        help="Set course tracker position (e.g. --set-position git 1)"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="View current course progression status"
    )
    parser.add_argument(
        "--list-courses",
        action="store_true",
        help="List all available courses and total lessons"
    )

    args = parser.parse_args()

    if args.list_courses:
        print("\n" + "=" * 60)
        print("           AVAILABLE TECHNICAL MASTERCLASSES            ")
        print("=" * 60)
        for c_id, c_data in AVAILABLE_COURSES.items():
            if not c_id.endswith("_masterclass") and not c_id.endswith("_cloud"):
                lessons_cnt = len(c_data.get("lessons", []))
                print(f"  • [{c_id.upper()}] {c_data.get('title')} ({lessons_cnt} Lessons)")
                print(f"    Category: {c_data.get('category')}")
                print(f"    Description: {c_data.get('description')}\n")
        print("=" * 60 + "\n")
        return

    if args.status:
        prog = load_progress()
        print("\n" + "=" * 55)
        print("          TECHNICAL COURSE TRACKER STATUS          ")
        print("=" * 55)
        print(f"  • Active Course       : {prog.get('active_course', 'git_masterclass').upper()}")
        print(f"  • Total Videos Made   : {prog.get('total_videos_created', 0)}")
        print("\n  Course Breakdown:")
        for cid, cinfo in prog.get("courses_progress", {}).items():
            completed_cnt = len(cinfo.get("completed", []))
            print(f"    - {cid.upper()}: Current Lesson #{cinfo.get('current_lesson', 1)} ({completed_cnt} completed)")
        print("=" * 55 + "\n")
        return

    if args.set_position:
        set_course_and_lesson(args.set_position[0], int(args.set_position[1]))
        return

    run_course_pipeline(
        course_name=args.course,
        lesson_number=args.lesson
    )

if __name__ == "__main__":
    main()
