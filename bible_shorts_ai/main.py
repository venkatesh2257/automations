#!/usr/bin/env python3
import argparse
import sys
import time
from pathlib import Path
from config import (
    BASE_DIR, OUTPUT_DIR, TEMP_DIR, DEFAULT_VOICE, GEMINI_API_KEY
)
from script_generator import generate_biblical_story
from tts_engine import generate_narration
from image_generator import generate_scene_image
from subtitle_generator import create_ass_subtitles
from video_renderer import assemble_final_video
from youtube_uploader import upload_video_to_youtube
from instagram_uploader import upload_reel_to_instagram

def run_pipeline(
    topic: str = None,
    voice: str = DEFAULT_VOICE,
    upload: bool = False,
    instagram: bool = False,
    privacy: str = "unlisted",
    output_filename: str = None
) -> Path:
    """Executes the complete Biblical Short creation and publishing pipeline."""
    start_time = time.time()
    timestamp = int(time.time())
    
    print("\n" + "=" * 60)
    print("      BIBLICAL STORIES AI YOUTUBE & INSTAGRAM GENERATOR      ")
    print("=" * 60)

    # 1. Generate Script & Visual Prompts
    print("\n[Step 1/5] Generating Biblical Story, Scenes & Moral Lesson...")
    story = generate_biblical_story(topic=topic)
    print(f"  • Topic: {story.topic}")
    print(f"  • Title: {story.title}")
    print(f"  • Moral: {story.moral}")
    print(f"  • Total Scenes: {len(story.scenes)}")
    print(f"  • Full Narration:\n    \"{story.full_narration}\"")

    # 2. Generate Audio & Timestamps
    print("\n[Step 2/5] Synthesizing Deep Narration Voiceover...")
    audio_path = TEMP_DIR / f"narration_{timestamp}.mp3"
    _, cues = generate_narration(story.full_narration, audio_path, voice=voice)
    print(f"  [✓] Audio generated: {audio_path.name} ({len(cues)} subtitle cues)")

    # 3. Generate Scene Visuals
    print("\n[Step 3/5] Generating Cinematic 9:16 Scene Images (Flux Engine)...")
    image_paths = []
    for scene in story.scenes:
        img_path = TEMP_DIR / f"scene_{timestamp}_{scene.scene_id}.jpg"
        generate_scene_image(
            prompt=scene.visual_prompt,
            output_path=img_path,
            scene_number=scene.scene_id
        )
        image_paths.append(img_path)

    # 4. Generate Subtitles
    print("\n[Step 4/5] Formatting Dynamic ASS Subtitles...")
    subtitles_path = TEMP_DIR / f"subtitles_{timestamp}.ass"
    create_ass_subtitles(cues, subtitles_path)
    print(f"  [✓] Subtitle styling ready: {subtitles_path.name}")

    # 5. Assemble and Render Video
    print("\n[Step 5/5] Compositing 1080x1920 Short with Motion & Subtitles...")
    if not output_filename:
        safe_title = "".join(c for c in story.topic if c.isalnum() or c in (" ", "_", "-")).rstrip()
        safe_title = safe_title.replace(" ", "_").lower()
        final_video_name = f"short_{safe_title}_{timestamp}.mp4"
    else:
        final_video_name = output_filename

    final_video_path = OUTPUT_DIR / final_video_name
    assemble_final_video(
        image_paths=image_paths,
        narration_audio_path=audio_path,
        subtitles_ass_path=subtitles_path,
        output_video_path=final_video_path
    )

    elapsed = time.time() - start_time
    print("\n" + "=" * 60)
    print(f" [✓] SHORT READY! Completed in {elapsed:.1f} seconds")
    print(f" [✓] Video Location: {final_video_path.resolve()}")
    print("=" * 60)

    # 6. Auto-Upload to YouTube if requested
    if upload:
        print("\n[+] Initiating YouTube Upload...")
        try:
            video_id = upload_video_to_youtube(
                video_path=final_video_path,
                title=story.youtube_title,
                description=f"{story.youtube_description}\n\nMoral: {story.moral}",
                tags=story.youtube_tags,
                privacy_status=privacy
            )
            print(f"  [✓] Live Short Link: https://youtube.com/shorts/{video_id}")
        except Exception as e:
            print(f"  [!] YouTube upload failed: {e}")

    # 7. Auto-Upload to Instagram if requested
    if instagram or upload:
        try:
            ig_caption = (
                f"{story.title} ✨\n\n"
                f"📖 Moral: {story.moral}\n\n"
                f"#bible #faith #christianity #biblestudy #jesus #god #angels #reels #biblestory #wisdom"
            )
            upload_reel_to_instagram(
                video_path=final_video_path,
                caption=ig_caption,
                thumbnail_path=image_paths[0] if image_paths else None
            )
        except Exception as e:
            print(f"  [!] Instagram upload failed: {e}")

    return final_video_path

def main():
    parser = argparse.ArgumentParser(
        description="Autonomous AI Biblical YouTube & Instagram Shorts Generator"
    )
    parser.add_argument(
        "--topic",
        type=str,
        default=None,
        help="Biblical story or topic"
    )
    parser.add_argument(
        "--voice",
        type=str,
        default=DEFAULT_VOICE,
        help=f"Edge-TTS voice name (default: {DEFAULT_VOICE})"
    )
    parser.add_argument(
        "--upload",
        action="store_true",
        help="Upload the generated short directly to YouTube and Instagram"
    )
    parser.add_argument(
        "--instagram",
        action="store_true",
        help="Upload the generated short to Instagram Reels"
    )
    parser.add_argument(
        "--privacy",
        type=str,
        default="unlisted",
        choices=["public", "unlisted", "private"],
        help="YouTube upload privacy status (default: unlisted)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Custom output MP4 filename"
    )

    args = parser.parse_args()
    run_pipeline(
        topic=args.topic,
        voice=args.voice,
        upload=args.upload,
        instagram=args.instagram,
        privacy=args.privacy,
        output_filename=args.output
    )

if __name__ == "__main__":
    main()
