import json
import os
import requests
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import google.genai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL, OPENROUTER_API_KEY, OPENROUTER_MODEL

@dataclass
class DialogueTurn:
    speaker: str  # "Alex" or "Sarah"
    text: str

@dataclass
class DeepDiveAct:
    act_id: int
    act_name: str
    visual_title: str
    visual_subtitle: str
    badge: str
    bullet_points: List[str]
    code_content: str
    dialogue: List[DialogueTurn]

@dataclass
class DeepDiveLesson:
    course_id: str
    lesson_number: int
    title: str
    concept: str
    analogy: str
    acts: List[DeepDiveAct]
    youtube_title: str
    youtube_description: str

def generate_with_openrouter(prompt: str) -> Optional[str]:
    """Generates text via OpenRouter API (DeepSeek V3 / R1)."""
    if not OPENROUTER_API_KEY:
        return None
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": OPENROUTER_MODEL,
            "messages": [
                {"role": "system", "content": "You are a senior computer science educator and scriptwriter. Always output strict JSON."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"}
        }
        resp = requests.post(url, json=payload, headers=headers, timeout=60)
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[!] OpenRouter error: {e}")
    return None

def generate_notebooklm_deepdive_script(course_title: str, lesson_num: int, lesson_title: str, concept: str, analogy: str, key_commands: List[str]) -> DeepDiveLesson:
    """
    Writes an ultra-realistic 2-host technical Deep Dive conversation using Google Pro or OpenRouter (DeepSeek R1/V3).
    """
    print(f"\n[*] Writing 2-Host Deep-Dive Script for Lesson {lesson_num}: {lesson_title}...")

    prompt = f"""You are the scriptwriter behind the famous Google NotebookLM Audio Deep Dives.
Create a hyper-realistic, lively, and intellectually thrilling 2-Host Technical Deep Dive conversation between two senior software engineers:

- **Alex (Lead Systems Architect)**: Grounded, strategic, explains deep architectural internals, analogies, and reasons.
- **Sarah (Senior Staff Engineer)**: Energetic, asks piercing practical questions, points out real-world developer headaches, terminal commands, and edge cases.

TOPIC DETAILS:
Course: {course_title}
Lesson {lesson_num}: {lesson_title}
Core Concept: {concept}
Analogy: {analogy}
Key Commands: {', '.join(key_commands)}

Structure the lesson into 6 Clear Educational Acts:
1. Act 1: The Nightmare Before Git (Chaos of final_v1.zip, overwritten code, 2 AM outages)
2. Act 2: The Mental Model (The Video Game Checkpoint system, alternate save slots)
3. Act 3: Under The Hood Architecture (Centralized SVN vs Distributed Git, why Linus built it)
4. Act 4: Deep Data Mechanics (Snapshots vs Deltas, Blobs, Trees, and SHA hashes)
5. Act 5: Live Terminal Masterclass (Exact commands for first-time setup and config)
6. Act 6: Senior Dev Pitfalls & Action Challenge (Verified emails, .gitignore secrets, practical challenge)

For each act, write 3-4 natural conversational turns between Alex and Sarah where they bounce insights off each other, laugh at classic dev mistakes, and deliver crystal-clear technical clarity.

Return a strict JSON object with this EXACT structure:
{{
  "course_id": "git",
  "lesson_number": {lesson_num},
  "title": "{lesson_title}",
  "concept": "{concept}",
  "analogy": "{analogy}",
  "acts": [
    {{
      "act_id": 1,
      "act_name": "The Chaos: Life Before Version Control",
      "visual_title": "Why Version Control Exists",
      "visual_subtitle": "The final_v1.zip, final_v2_really_final.zip disaster",
      "badge": "ACT 1: THE HOOK",
      "bullet_points": [
        "Multiple developers overwriting shared files",
        "2 AM critical production outage with no audit trail",
        "Zero ability to safely rollback to a working state",
        "Lost engineering hours manually diffing code"
      ],
      "code_content": "$ ls -la /shared_project\\nauth_service_v1.py\\nauth_service_v2_FINAL.py\\nauth_service_v3_DO_NOT_DELETE.py\\n[CRITICAL ERROR] Overwritten session handler!",
      "dialogue": [
        {{"speaker": "Sarah", "text": "Alex, let's be honest—every developer has been there. It is Friday afternoon, and someone saves a file called final_v2_really_final.zip."}},
        {{"speaker": "Alex", "text": "Oh absolutely. And then Monday morning the production server is down, and nobody knows whose code broke the build."}},
        {{"speaker": "Sarah", "text": "That chaos is exactly why Version Control isn't just a nice tool—it is the foundation of all modern engineering."}}
      ]
    }},
    {{
      "act_id": 2,
      "act_name": "The Mental Model: Video Game Checkpoints",
      "visual_title": "The Checkpoint Mental Model",
      "visual_subtitle": "Never save over your single game file again",
      "badge": "ACT 2: ANALOGY",
      "bullet_points": [
        "Checkpoint (Commit): Instant respawn before dangerous boss fights",
        "Branch (Alternate Slot): Explore experiments without risking main save",
        "Merge (Combine): Safely integrate victories into the main story",
        "Immutability: Every checkpoint is cryptographically sealed"
      ],
      "code_content": "# The Mental Model\\nCheckpoint 1: Project Initialized\\nCheckpoint 2: Added User Login\\nCheckpoint 3: Broken API Refactor\\n==> Action: Rewind to Checkpoint 2 in 1 sec!",
      "dialogue": [
        {{"speaker": "Alex", "text": "The best way to visualize Git is like a video game checkpoint system. Before a boss fight, you save your progress."}},
        {{"speaker": "Sarah", "text": "Right! If your character gets eliminated, you don't delete the whole game—you instantly reload at that exact checkpoint."}},
        {{"speaker": "Alex", "text": "Exactly. In Git, a commit is that permanent, unbreakable checkpoint."}}
      ]
    }},
    {{
      "act_id": 3,
      "act_name": "Centralized vs Distributed Architecture",
      "visual_title": "Centralized vs. Distributed Git",
      "visual_subtitle": "Why Linus Torvalds engineered Git for the Linux Kernel in 2005",
      "badge": "ACT 3: ARCHITECTURE",
      "bullet_points": [
        "Centralized (SVN): Single point of failure; offline work is impossible",
        "Distributed (Git): Every developer has the FULL repository history",
        "100% Offline: Commit, branch, diff, and inspect with zero Wi-Fi",
        "Blazing Speed: All operations execute on local SSD in milliseconds"
      ],
      "code_content": "Centralized (SVN): [Laptop] ---> [Single Central Server (SPoF)]\\n\\nDistributed (Git):\\n[Laptop A (Full Clone)] <---> [GitHub Backup]\\n[Laptop B (Full Clone)] <---> [Laptop C (Full Clone)]",
      "dialogue": [
        {{"speaker": "Sarah", "text": "Before Git, older systems like SVN kept all history on a single central server. If that server died, you were stuck."}},
        {{"speaker": "Alex", "text": "Linus Torvalds hated that bottleneck, so in 2005 he created Git as a Distributed system where every developer's machine holds the complete project history."}},
        {{"speaker": "Sarah", "text": "Which means you can commit, branch, and inspect diffs completely offline on an airplane with zero internet."}}
      ]
    }},
    {{
      "act_id": 4,
      "act_name": "Under The Hood: Snapshots vs Deltas",
      "visual_title": "How Git Actually Stores Data",
      "visual_subtitle": "Snapshots, Trees, Blobs, and SHA-1 Hashes",
      "badge": "ACT 4: MECHANICS",
      "bullet_points": [
        "Snapshots: Git takes full-filesystem pictures, not file deltas",
        "Efficiency: Unchanged files are lightweight cryptographic links",
        "Blob: Raw file content stored by hash",
        "Tree: Directory structure and filenames",
        "Commit: Top-level tree + Author + Parent Hash DAG"
      ],
      "code_content": "$ git cat-file -p HEAD\\ntree d8329fc1cc938780ffdd9f94e0d364e0ea74f579\\nauthor Alex Rivera <alex@dev.com>\\ncommitter Alex Rivera <alex@dev.com>\\n\\nInitial repository architecture commit",
      "dialogue": [
        {{"speaker": "Alex", "text": "A huge misconception is that Git stores line-by-line differences. In reality, Git stores complete filesystem snapshots."}},
        {{"speaker": "Sarah", "text": "And if a file hasn't changed between commits, Git doesn't duplicate it—it just points a cryptographic link to the existing blob."}},
        {{"speaker": "Alex", "text": "That makes Git lightning fast and mathematically corruption-proof."}}
      ]
    }},
    {{
      "act_id": 5,
      "act_name": "Live Terminal Masterclass",
      "visual_title": "First-Time Essential Configuration",
      "visual_subtitle": "Setting up your workstation like a senior engineer",
      "badge": "ACT 5: TERMINAL SETUP",
      "bullet_points": [
        "Set global user name for commit signatures",
        "Set verified GitHub email to preserve contribution graph",
        "Standardize default branch to 'main'",
        "Set VS Code as the interactive editor",
        "Inspect all configuration file origins"
      ],
      "code_content": "$ git --version\\ngit version 2.43.0\\n\\n$ git config --global user.name \\\"Alex Rivera\\\"\\n$ git config --global user.email \\\"alex@dev.com\\\"\\n$ git config --global init.defaultBranch main\\n$ git config --list --show-origin",
      "dialogue": [
        {{"speaker": "Sarah", "text": "Let's look at the terminal. The first three commands every engineer must run are setting their user name, email, and default branch."}},
        {{"speaker": "Alex", "text": "Make sure your email matches your GitHub account exactly, otherwise your commit history won't show up on your profile graph."}},
        {{"speaker": "Sarah", "text": "And running `git config --list --show-origin` shows you exactly where those global settings are stored on your disk."}}
      ]
    }},
    {{
      "act_id": 6,
      "act_name": "Senior Dev Pitfalls & Action Challenge",
      "visual_title": "Production Traps & Hands-On Challenge",
      "visual_subtitle": "Golden rules for professional production environments",
      "badge": "ACT 6: ACTION CHALLENGE",
      "bullet_points": [
        "⚠️ Pitfall 1: Unverified email breaks GitHub contribution streak",
        "⚠️ Pitfall 2: Forgetting .gitignore leaks API keys and .env secrets",
        "⚠️ Pitfall 3: Relying on GUI before understanding CLI plumbing",
        "🎯 Your Challenge: Run `git config --list` and verify your setup!"
      ],
      "code_content": "$ cat .gitignore\\n.env\\n*.pem\\nnode_modules/\\n__pycache__/\\n\\n# Verified & Ready for Lesson 02!",
      "dialogue": [
        {{"speaker": "Alex", "text": "The number one senior developer rule: always configure your `.gitignore` before making your first commit to prevent leaking API keys."}},
        {{"speaker": "Sarah", "text": "For your action challenge today, open your terminal, run `git config --list`, and verify your workstation is ready for Lesson 2."}},
        {{"speaker": "Alex", "text": "Hit subscribe, and we'll see you in the next deep dive!"}}
      ]
    }}
  ],
  "youtube_title": "{lesson_title} | {course_title} (Lesson {lesson_num})",
  "youtube_description": "2-Host Deep Dive Masterclass covering {lesson_title} with full architecture, analogies, and terminal setup."
}}

Strict Rules:
- Return ONLY valid JSON, no backticks, no markdown fences.
- Total 6 acts with realistic 2-host conversational dialogue.
"""

    raw_text = None

    # Try Google Pro First
    if GEMINI_API_KEY:
        try:
            client = genai.Client(api_key=GEMINI_API_KEY)
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )
            raw_text = response.text.strip()
        except Exception as e:
            print(f"[!] Google Gemini Pro error ({e}), falling back to OpenRouter...")

    # Fallback to OpenRouter (DeepSeek R1 / V3)
    if not raw_text and OPENROUTER_API_KEY:
        print("[*] Generating with OpenRouter (DeepSeek)...")
        raw_text = generate_with_openrouter(prompt)

    if raw_text:
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.startswith("```"):
            raw_text = raw_text[3:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]

        data = json.loads(raw_text.strip())

        acts = []
        for a in data["acts"]:
            dialogue_turns = [DialogueTurn(**d) for d in a["dialogue"]]
            acts.append(DeepDiveAct(
                act_id=a["act_id"],
                act_name=a["act_name"],
                visual_title=a["visual_title"],
                visual_subtitle=a["visual_subtitle"],
                badge=a["badge"],
                bullet_points=a["bullet_points"],
                code_content=a["code_content"],
                dialogue=dialogue_turns
            ))

        return DeepDiveLesson(
            course_id=data.get("course_id", "git"),
            lesson_number=data.get("lesson_number", lesson_num),
            title=data.get("title", lesson_title),
            concept=data.get("concept", concept),
            analogy=data.get("analogy", analogy),
            acts=acts,
            youtube_title=data.get("youtube_title", f"{lesson_title} (Lesson {lesson_num})"),
            youtube_description=data.get("youtube_description", f"Deep Dive on {lesson_title}")
        )

    raise RuntimeError("Failed to generate script with both Gemini Pro and OpenRouter.")
