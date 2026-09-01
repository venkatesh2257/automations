#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from config import BASE_DIR, YOUTUBE_CLIENT_SECRETS_FILE, YOUTUBE_TOKEN_FILE
from youtube_uploader import get_authenticated_service

def setup_env():
    print("=" * 60)
    print("      AI BIBLICAL SHORTS - CREDENTIALS SETUP WIZARD       ")
    print("=" * 60)

    env_file = BASE_DIR / ".env"
    
    # 1. Gemini API Key Setup
    print("\n[1/3] Gemini API Key Setup (For Unlimited AI Scriptwriting):")
    current_key = os.environ.get("GEMINI_API_KEY", "")
    if current_key:
        print(f"  • Current Key Found: {current_key[:6]}...{current_key[-4:]}")
    
    user_key = input("  Enter your Gemini API Key (or press Enter to keep current): ").strip()
    if user_key:
        with open(env_file, "a") as f:
            f.write(f"\nGEMINI_API_KEY={user_key}\n")
        print(f"  [✓] Gemini API Key saved to {env_file.name}")

    # 2. YouTube OAuth client_secrets.json
    print("\n[2/3] YouTube Data API Credentials Setup:")
    print(f"  Expected location: {YOUTUBE_CLIENT_SECRETS_FILE.resolve()}")
    if YOUTUBE_CLIENT_SECRETS_FILE.exists():
        print("  [✓] client_secrets.json is already present!")
    else:
        print("  [!] client_secrets.json is missing.")
        print("  To get it:")
        print("    1. Go to https://console.cloud.google.com")
        print("    2. Create a project and search/enable 'YouTube Data API v3'.")
        print("    3. Go to 'Credentials' -> 'Create Credentials' -> 'OAuth client ID'.")
        print("    4. Application type: 'Desktop App'.")
        print("    5. Download the JSON file and rename/copy it to:")
        print(f"       {YOUTUBE_CLIENT_SECRETS_FILE.resolve()}")

    # 3. Authenticate YouTube
    print("\n[3/4] Authenticate YouTube Channel (One-Time Login):")
    if YOUTUBE_CLIENT_SECRETS_FILE.exists():
        try:
            print("  [+] Starting authentication flow in your browser...")
            get_authenticated_service()
            print(f"  [✓] YouTube channel successfully connected! Token saved to {YOUTUBE_TOKEN_FILE.name}")
        except Exception as e:
            print(f"  [!] Authentication failed: {e}")
    else:
        print("  [i] Place your client_secrets.json file first, then run this script again.")

    # 4. Instagram Credentials Setup
    print("\n[4/4] Instagram Reels Setup:")
    ig_user = input("  Enter your Instagram Username/Handle (or leave empty to skip): ").strip()
    if ig_user:
        ig_pass = input("  Enter your Instagram Password: ").strip()
        with open(env_file, "a") as f:
            f.write(f"\nINSTAGRAM_USERNAME={ig_user}\n")
            f.write(f"INSTAGRAM_PASSWORD={ig_pass}\n")
        print(f"  [✓] Instagram credentials saved to {env_file.name}")

    print("\n" + "=" * 60)
    print(" [✓] SETUP WIZARD COMPLETE!")
    print("=" * 60)

if __name__ == "__main__":
    setup_env()
