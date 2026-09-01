#!/usr/bin/env python3
import argparse
import datetime
import json
import time
from pathlib import Path
from typing import List, Optional
from config import BASE_DIR, OUTPUT_DIR, TEMP_DIR, DEFAULT_VOICE, GEMINI_API_KEY
from script_generator import generate_chapter_3part_series, BiblicalShortStory
from tts_engine import generate_narration
from image_generator import generate_scene_image
from subtitle_generator import create_ass_subtitles
from video_renderer import assemble_final_video
from youtube_uploader import upload_video_to_youtube
from instagram_uploader import upload_reel_to_instagram
from chapter_manager import (
    get_current_reading,
    mark_chapter_completed,
    set_reading_position,
    load_progress
)

# 3 Optimal daily posting slots (Morning, Midday, Evening)
DEFAULT_POSTING_HOURS = [9, 14, 19]  # 9:00 AM, 2:00 PM, 7:00 PM UTC

def calculate_publish_timestamps(start_date: datetime.date = None) -> List[datetime.datetime]:
    """Computes ISO 8601 UTC timestamps for 3 scheduled parts throughout the day."""
    if start_date is None:
        start_date = datetime.date.today()

    now = datetime.datetime.now(datetime.timezone.utc)
    slots = []
    
    for hour in DEFAULT_POSTING_HOURS:
        slot_dt = datetime.datetime(
            start_date.year, start_date.month, start_date.day,
            hour, 0, 0, tzinfo=datetime.timezone.utc
        )
        if slot_dt <= now:
            slot_dt += datetime.timedelta(days=1)
        slots.append(slot_dt)
        
    return slots

def run_daily_chapter(
    book: Optional[str] = None,
    chapter: Optional[int] = None,
    upload: bool = True,
    voice: str = DEFAULT_VOICE
):
    """
    Generates 3 sequential Short/Reel videos covering 1 Bible Chapter (Genesis to Revelation),
    publishes them to YouTube & Instagram across peak hours, and updates progress for tomorrow.
    """
    # 1. Determine book and chapter
    if not book or not chapter:
        curr_book, curr_ch = get_current_reading()
    else:
        curr_book, curr_ch = book, chapter

    print("\n" + "=" * 65)
    print(f"   BIBLE CHAPTER-BY-CHAPTER DAILY SERIES: {curr_book.upper()} CHAPTER {curr_ch}")
    print(f"   (Generating 3 Daily Videos: Part 1/3, Part 2/3, Part 3/3)")
    print("=" * 65)

    publish_slots = calculate_publish_timestamps()
    
    # 2. Generate 3-part script series for this chapter
    series_stories: List[BiblicalShortStory] = generate_chapter_3part_series(curr_book, curr_ch)
    log_records = []

    for idx, story in enumerate(series_stories):
        slot_time = publish_slots[idx]
        timestamp = int(time.time())
        iso_publish_at = slot_time.strftime("%Y-%m-%dT%H:%M:%SZ")

        print(f"\n[Part {idx+1}/3] -------------------------------------------------")
        print(f"  • Scheduled Release Time : {slot_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"  • Title                  : {story.title}")
        print(f"  • Moral                  : {story.moral}")

        # A. Narration
        audio_path = TEMP_DIR / f"batch_{curr_book}_{curr_ch}_p{idx+1}_{timestamp}.mp3"
        _, cues = generate_narration(story.full_narration, audio_path, voice=voice)

        # B. Visuals
        image_paths = []
        for scene in story.scenes:
            img_path = TEMP_DIR / f"scene_{curr_book}_{curr_ch}_p{idx+1}_{scene.scene_id}_{timestamp}.jpg"
            generate_scene_image(
                prompt=scene.visual_prompt,
                output_path=img_path,
                scene_number=scene.scene_id
            )
            image_paths.append(img_path)

        # C. Subtitles
        subtitles_path = TEMP_DIR / f"subtitles_{curr_book}_{curr_ch}_p{idx+1}_{timestamp}.ass"
        create_ass_subtitles(cues, subtitles_path)

        # D. Composite Final Video
        safe_book = "".join(c for c in curr_book if c.isalnum()).lower()
        final_video_name = f"{safe_book}_ch{curr_ch}_part{idx+1}_{timestamp}.mp4"
        final_video_path = OUTPUT_DIR / final_video_name

        assemble_final_video(
            image_paths=image_paths,
            narration_audio_path=audio_path,
            subtitles_ass_path=subtitles_path,
            output_video_path=final_video_path
        )

        record = {
            "book": curr_book,
            "chapter": curr_ch,
            "part": idx + 1,
            "title": story.youtube_title,
            "moral": story.moral,
            "video_path": str(final_video_path.resolve()),
            "scheduled_time_utc": iso_publish_at,
            "uploaded_youtube": False,
            "uploaded_instagram": False,
            "youtube_id": None,
            "instagram_url": None
        }

        # E. Upload to YouTube Shorts
        if upload:
            try:
                print(f"  [+] Uploading and scheduling to YouTube for {iso_publish_at}...")
                video_id = upload_video_to_youtube(
                    video_path=final_video_path,
                    title=story.youtube_title,
                    description=f"{story.youtube_description}\n\n📖 Chapter Moral: {story.moral}",
                    tags=story.youtube_tags,
                    publish_at=iso_publish_at
                )
                record["uploaded_youtube"] = True
                record["youtube_id"] = video_id
                record["shorts_url"] = f"https://youtube.com/shorts/{video_id}"
                print(f"  [✓] YouTube Short scheduled! Video ID: {video_id}")
            except Exception as e:
                print(f"  [!] YouTube upload error: {e}")

            # F. Upload to Instagram Reels
            try:
                ig_caption = (
                    f"📖 {story.title}\n\n"
                    f"✨ Moral: {story.moral}\n\n"
                    f"Follow @biblewithai7 to journey through the entire Bible chapter by chapter from Genesis to Revelation!\n\n"
                    f"#bible #genesis #{curr_book.lower()} #christianity #faith #god #jesus #scripture #biblewisdom #reels #viral"
                )
                reel_url = upload_reel_to_instagram(
                    video_path=final_video_path,
                    caption=ig_caption,
                    thumbnail_path=image_paths[0] if image_paths else None
                )
                if reel_url:
                    record["uploaded_instagram"] = True
                    record["instagram_url"] = reel_url
            except Exception as e:
                print(f"  [!] Instagram upload error: {e}")

        log_records.append(record)

    # 3. Mark Chapter as Completed and Advance Pointer for Tomorrow
    next_book, next_ch = mark_chapter_completed(curr_book, curr_ch, video_count=len(series_stories))

    # Save summary
    log_file = OUTPUT_DIR / "daily_schedule_log.json"
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(log_records, f, indent=2)

    print("\n" + "=" * 65)
    print(f" [✓] COMPLETED {curr_book} CHAPTER {curr_ch} (3 Videos Created & Published)!")
    print(f" [✓] Next Scheduled Chapter for Tomorrow: {next_book} Chapter {next_ch}")
    print(f" [✓] Log saved to: {log_file.resolve()}")
    print("=" * 65)

def main():
    parser = argparse.ArgumentParser(
        description="Bible Chapter-by-Chapter Daily 3-Shorts Generator & Publisher"
    )
    parser.add_argument(
        "--book",
        type=str,
        default=None,
        help="Specify a Bible book to generate (e.g. Genesis, Exodus, Revelation)"
    )
    parser.add_argument(
        "--chapter",
        type=int,
        default=None,
        help="Specify a Bible chapter number (e.g. 1, 2, 3)"
    )
    parser.add_argument(
        "--set-position",
        nargs=2,
        metavar=("BOOK", "CHAPTER"),
        help="Set the Bible reading tracker position (e.g. --set-position Genesis 1)"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Display current Bible progress tracking position"
    )
    parser.add_argument(
        "--no-upload",
        action="store_true",
        help="Generate 3 videos locally without uploading to YouTube/Instagram"
    )
    parser.add_argument(
        "--voice",
        type=str,
        default=DEFAULT_VOICE,
        help=f"Voice name (default: {DEFAULT_VOICE})"
    )

    args = parser.parse_args()

    if args.status:
        progress = load_progress()
        print("\n" + "=" * 50)
        print("          BIBLE PROGRESS TRACKER STATUS           ")
        print("=" * 50)
        print(f"  • Current Book    : {progress.get('current_book', 'Genesis')}")
        print(f"  • Current Chapter : {progress.get('current_chapter', 1)}")
        print(f"  • Total Videos    : {progress.get('total_videos_created', 0)}")
        print(f"  • Completed Count : {len(progress.get('completed_chapters', []))} chapters")
        print("=" * 50 + "\n")
        return

    if args.set_position:
        set_reading_position(args.set_position[0], int(args.set_position[1]))
        return

    run_daily_chapter(
        book=args.book,
        chapter=args.chapter,
        upload=not args.no_upload,
        voice=args.voice
    )

if __name__ == "__main__":
    main()
