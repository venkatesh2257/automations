#!/usr/bin/env python3
"""
One-Time YouTube Channel Authorization Script
Run this script to link your YouTube channel and generate token.json.
"""
from config import YOUTUBE_CLIENT_SECRETS_FILE, YOUTUBE_TOKEN_FILE
from youtube_uploader import get_authenticated_service

def main():
    print("=" * 60)
    print("      YOUTUBE CHANNEL OAUTH2 AUTHORIZATION       ")
    print("=" * 60)
    print(f"[*] Reading credentials from: {YOUTUBE_CLIENT_SECRETS_FILE.name}")
    print("[*] Opening Google login in your browser...")
    print("    (If running over SSH/remote, copy and paste the URL into your browser)\n")

    try:
        service = get_authenticated_service()
        # Verify the authenticated channel
        response = service.channels().list(part="snippet,statistics", mine=True).execute()
        items = response.get("items", [])
        if items:
            ch_title = items[0]["snippet"]["title"]
            ch_subs = items[0]["statistics"].get("subscriberCount", "0")
            print("\n" + "=" * 60)
            print(f" [✓] SUCCESS! Connected to YouTube Channel: '{ch_title}'")
            print(f" [✓] Subscribers: {ch_subs}")
            print(f" [✓] Permanent token saved to: {YOUTUBE_TOKEN_FILE.name}")
            print(" [✓] Auto-uploading is now fully enabled!")
            print("=" * 60)
        else:
            print("[✓] Authorized successfully! Token created.")
    except Exception as e:
        print(f"\n[!] Authorization error: {e}")

if __name__ == "__main__":
    main()
