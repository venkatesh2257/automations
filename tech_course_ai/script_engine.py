import json
import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import google.genai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL

@dataclass
class LessonSection:
    section_id: int
    section_name: str
    narration: str
    visual_type: str
    visual_title: str
    code_language: str
    code_content: str
    bullet_points: List[str]
    broll_query: str

@dataclass
class TechLessonScript:
    course_id: str
    lesson_number: int
    title: str
    concept: str
    analogy: str
    difficulty: str
    sections: List[LessonSection]
    full_narration: str
    youtube_title: str
    youtube_description: str
    youtube_tags: List[str]
    chapter_markers: List[Dict[str, str]]

def generate_pro_teacher_script(course_info: Dict, lesson_info: Dict) -> TechLessonScript:
    """
    Generates a world-class technical lesson script using Google Pro (Gemini 3.6 Flash)
    and the Feynman pedagogical framework.
    """
    course_title = course_info.get("title", "Technical Masterclass")
    lesson_num = lesson_info.get("lesson_number", 1)
    lesson_title = lesson_info.get("title", "Core Concepts")
    concept = lesson_info.get("concept", "Technical architecture")
    analogy = lesson_info.get("analogy", "Intuitive comparison")
    commands = lesson_info.get("key_commands", [])

    print(f"\n[*] Generating Pro-Teacher Script with Google Pro ({GEMINI_MODEL}) for: Lesson {lesson_num} - {lesson_title}...")

    if GEMINI_API_KEY:
        try:
            client = genai.Client(api_key=GEMINI_API_KEY)
            prompt = f"""You are an elite Lead Principal Software Engineer and world-renowned Computer Science educator (like Richard Feynman meets Fireship).
Write an extraordinary, high-clarity technical course video script for:

Course: {course_title}
Lesson {lesson_num}: {lesson_title}
Core Concept to Explain: {concept}
Analogy to Use: {analogy}
Key Commands/Code: {', '.join(commands)}

Follow the 6-Stage "Pro-Teacher" Structure:
1. Act 1: The Hook & The Problem (Why does this exist? What disaster occurs without it?)
2. Act 2: The Real-World Analogy (Explain intuitively so a beginner instantly grasps it)
3. Act 3: Under The Hood (Technical architecture, mechanics, data flow)
4. Act 4: Live Code / Terminal Walkthrough (Exact syntax, commands, and expected output)
5. Act 5: Senior Dev Traps & Best Practices (Common pitfalls, security warnings, production tips)
6. Act 6: Summary & Actionable Mini-Challenge (Clear recap + exercise for the viewer)

Return a JSON object with this EXACT structure:
{{
  "course_id": "{course_info.get('id', 'tech')}",
  "lesson_number": {lesson_num},
  "title": "{lesson_title}",
  "concept": "{concept}",
  "analogy": "{analogy}",
  "difficulty": "{lesson_info.get('difficulty', 'Beginner')}",
  "sections": [
    {{
      "section_id": 1,
      "section_name": "The Hook & The Core Problem",
      "narration": "Natural, spoken conversational narration (~30-40 seconds). Explain clearly with zero confusing fluff.",
      "visual_type": "concept_card",
      "visual_title": "Slide Title",
      "code_language": "",
      "code_content": "",
      "bullet_points": ["Point 1", "Point 2", "Point 3", "Point 4"],
      "broll_query": "4k tech visual search query e.g. frustrated developer looking at code screen"
    }},
    {{
      "section_id": 2,
      "section_name": "The Real-World Analogy",
      "narration": "...",
      "visual_type": "diagram",
      "visual_title": "...",
      "code_language": "",
      "code_content": "",
      "bullet_points": [...],
      "broll_query": "server room with glowing blue fiber optic cables"
    }},
    {{
      "section_id": 3,
      "section_name": "Under The Hood Architecture",
      "narration": "...",
      "visual_type": "concept_card",
      "visual_title": "...",
      "code_language": "",
      "code_content": "",
      "bullet_points": [...],
      "broll_query": "microchip circuit board macro zoom"
    }},
    {{
      "section_id": 4,
      "section_name": "Live Code & Terminal Walkthrough",
      "narration": "...",
      "visual_type": "terminal",
      "visual_title": "...",
      "code_language": "bash",
      "code_content": "$ exact command\\noutput line 1\\noutput line 2",
      "bullet_points": [...],
      "broll_query": "cyberpunk computer screen green code typing"
    }},
    {{
      "section_id": 5,
      "section_name": "Senior Dev Traps & Best Practices",
      "narration": "...",
      "visual_type": "warning_card",
      "visual_title": "...",
      "code_language": "bash",
      "code_content": "",
      "bullet_points": [...],
      "broll_query": "futuristic data security holographic interface"
    }},
    {{
      "section_id": 6,
      "section_name": "Summary & Mini Challenge",
      "narration": "...",
      "visual_type": "concept_card",
      "visual_title": "...",
      "code_language": "",
      "code_content": "",
      "bullet_points": [...],
      "broll_query": "glowing digital earth with network nodes"
    }}
  ],
  "youtube_title": "{lesson_title} | {course_title} (Lesson {lesson_num})",
  "youtube_description": "Complete description with timestamps and key takeaways.",
  "youtube_tags": ["{course_info.get('id', 'tech')}", "tutorial", "programming", "coding", "masterclass"]
}}

Strict Rules:
- Output ONLY valid JSON without markdown code fences or backticks.
- Total 6 sections.
- Narration must sound like a friendly, incredibly smart senior engineer speaking directly to the viewer.
"""
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )
            raw_text = response.text.strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            data = json.loads(raw_text.strip())

            sections = [LessonSection(**s) for s in data["sections"]]
            full_narration = " ".join(s.narration for s in sections)
            
            markers = [{"title": s.section_name, "section_id": s.section_id} for s in sections]

            return TechLessonScript(
                course_id=data.get("course_id", course_info.get("id", "tech")),
                lesson_number=data.get("lesson_number", lesson_num),
                title=data.get("title", lesson_title),
                concept=data.get("concept", concept),
                analogy=data.get("analogy", analogy),
                difficulty=data.get("difficulty", "Beginner"),
                sections=sections,
                full_narration=full_narration,
                youtube_title=data.get("youtube_title", f"{lesson_title} (Lesson {lesson_num})"),
                youtube_description=data.get("youtube_description", f"Master {lesson_title} in this lesson."),
                youtube_tags=data.get("youtube_tags", ["tech", "coding", "tutorial"]),
                chapter_markers=markers
            )
        except Exception as e:
            print(f"[!] Google Pro generation error ({e}), using curated lesson blueprint...")

    # Fallback to Curated
    from curricula.git_masterclass import GIT_COURSE
    l_data = GIT_COURSE["lessons"][0]
    sections = [
        LessonSection(1, "The Hook & The Core Problem", "Have you ever saved a project as final_v1.zip and then final_v2_really_final.zip? Without version control, managing code turns into an absolute nightmare.", "concept_card", "Why Version Control Exists", "", "", ["The final_v2 disaster", "Accidental overwrites", "Zero audit trail", "Impossible rollbacks"], "frustrated developer looking at code screen"),
        LessonSection(2, "The Real-World Analogy", "Think of Git like the checkpoint system in a video game. Instead of saving over your single game file, Git lets you create instant checkpoints at every major milestone.", "diagram", "The Checkpoint Mental Model", "", "", ["Checkpoint 1: Setup", "Checkpoint 2: Added Login", "Checkpoint 3: Crashed feature", "-> Git Action: Rewind in 1 second"], "server room with glowing blue fiber optic cables"),
        LessonSection(3, "Under The Hood: Distributed Architecture", "Git is a Distributed Version Control System. Every single developer has a full copy of the entire project history on their own laptop.", "concept_card", "Distributed Version Control", "", "", ["100% Offline Capability", "Every machine is a backup", "Cryptographic integrity", "Fast branching"], "microchip circuit board macro zoom"),
        LessonSection(4, "Live Terminal Walkthrough", "Let us set up Git right now. Check your version with git --version, then set your global user.name and user.email.", "terminal", "Terminal: Global Git Configuration", "bash", "$ git --version\ngit version 2.43.0\n\n$ git config --global user.name \"Alex\"\n$ git config --global user.email \"alex@dev.com\"", ["Step 1: Check version", "Step 2: Set user name", "Step 3: Set user email"], "cyberpunk computer screen green code typing"),
        LessonSection(5, "Senior Developer Traps & Best Practices", "Never use an unverified email in your config, and always standardize your default branch name to 'main'.", "warning_card", "Senior Dev Warning: Default Branch", "bash", "$ git config --global init.defaultBranch main", ["Use verified GitHub email", "Set default branch to main", "Learn CLI before GUI tools"], "futuristic data security holographic interface"),
        LessonSection(6, "Summary & Mini Challenge", "To recap: Git is your ultimate code safety net. For your mini challenge today, run git config --list on your machine.", "concept_card", "Lesson Summary & Action", "", "", ["Key takeaway: Milestone checkpoints", "Action: Run git config --list", "Next Lesson: Working Dir vs Staging Area"], "glowing digital earth with network nodes")
    ]
    full_narration = " ".join(s.narration for s in sections)
    markers = [{"title": s.section_name, "section_id": s.section_id} for s in sections]
    
    return TechLessonScript(
        course_id=course_info.get("id", "tech"),
        lesson_number=lesson_num,
        title=lesson_title,
        concept=concept,
        analogy=analogy,
        difficulty="Beginner",
        sections=sections,
        full_narration=full_narration,
        youtube_title=f"{lesson_title} | {course_title} (Lesson {lesson_num})",
        youtube_description=f"Master {lesson_title} in this masterclass lesson.",
        youtube_tags=["git", "tutorial", "programming"],
        chapter_markers=markers
    )
