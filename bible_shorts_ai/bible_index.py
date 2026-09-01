"""
Comprehensive index of the 66 Books of the Bible with chapter counts
spanning the Old and New Testaments.
"""

BIBLE_BOOKS = [
    # Old Testament (Law / Pentateuch)
    {"name": "Genesis", "chapters": 50, "testament": "OT"},
    {"name": "Exodus", "chapters": 40, "testament": "OT"},
    {"name": "Leviticus", "chapters": 27, "testament": "OT"},
    {"name": "Numbers", "chapters": 36, "testament": "OT"},
    {"name": "Deuteronomy", "chapters": 34, "testament": "OT"},
    
    # Historical Books
    {"name": "Joshua", "chapters": 24, "testament": "OT"},
    {"name": "Judges", "chapters": 21, "testament": "OT"},
    {"name": "Ruth", "chapters": 4, "testament": "OT"},
    {"name": "1 Samuel", "chapters": 31, "testament": "OT"},
    {"name": "2 Samuel", "chapters": 24, "testament": "OT"},
    {"name": "1 Kings", "chapters": 22, "testament": "OT"},
    {"name": "2 Kings", "chapters": 25, "testament": "OT"},
    {"name": "1 Chronicles", "chapters": 29, "testament": "OT"},
    {"name": "2 Chronicles", "chapters": 36, "testament": "OT"},
    {"name": "Ezra", "chapters": 10, "testament": "OT"},
    {"name": "Nehemiah", "chapters": 13, "testament": "OT"},
    {"name": "Esther", "chapters": 10, "testament": "OT"},
    
    # Wisdom & Poetry
    {"name": "Job", "chapters": 42, "testament": "OT"},
    {"name": "Psalms", "chapters": 150, "testament": "OT"},
    {"name": "Proverbs", "chapters": 31, "testament": "OT"},
    {"name": "Ecclesiastes", "chapters": 12, "testament": "OT"},
    {"name": "Song of Solomon", "chapters": 8, "testament": "OT"},
    
    # Major Prophets
    {"name": "Isaiah", "chapters": 66, "testament": "OT"},
    {"name": "Jeremiah", "chapters": 52, "testament": "OT"},
    {"name": "Lamentations", "chapters": 5, "testament": "OT"},
    {"name": "Ezekiel", "chapters": 48, "testament": "OT"},
    {"name": "Daniel", "chapters": 12, "testament": "OT"},
    
    # Minor Prophets
    {"name": "Hosea", "chapters": 14, "testament": "OT"},
    {"name": "Joel", "chapters": 3, "testament": "OT"},
    {"name": "Amos", "chapters": 9, "testament": "OT"},
    {"name": "Obadiah", "chapters": 1, "testament": "OT"},
    {"name": "Jonah", "chapters": 4, "testament": "OT"},
    {"name": "Micah", "chapters": 7, "testament": "OT"},
    {"name": "Nahum", "chapters": 3, "testament": "OT"},
    {"name": "Habakkuk", "chapters": 3, "testament": "OT"},
    {"name": "Zephaniah", "chapters": 3, "testament": "OT"},
    {"name": "Haggai", "chapters": 2, "testament": "OT"},
    {"name": "Zechariah", "chapters": 14, "testament": "OT"},
    {"name": "Malachi", "chapters": 4, "testament": "OT"},
    
    # New Testament (Gospels & History)
    {"name": "Matthew", "chapters": 28, "testament": "NT"},
    {"name": "Mark", "chapters": 16, "testament": "NT"},
    {"name": "Luke", "chapters": 24, "testament": "NT"},
    {"name": "John", "chapters": 21, "testament": "NT"},
    {"name": "Acts", "chapters": 28, "testament": "NT"},
    
    # Pauline Epistles
    {"name": "Romans", "chapters": 16, "testament": "NT"},
    {"name": "1 Corinthians", "chapters": 16, "testament": "NT"},
    {"name": "2 Corinthians", "chapters": 13, "testament": "NT"},
    {"name": "Galatians", "chapters": 6, "testament": "NT"},
    {"name": "Ephesians", "chapters": 6, "testament": "NT"},
    {"name": "Philippians", "chapters": 4, "testament": "NT"},
    {"name": "Colossians", "chapters": 4, "testament": "NT"},
    {"name": "1 Thessalonians", "chapters": 5, "testament": "NT"},
    {"name": "2 Thessalonians", "chapters": 3, "testament": "NT"},
    {"name": "1 Timothy", "chapters": 6, "testament": "NT"},
    {"name": "2 Timothy", "chapters": 4, "testament": "NT"},
    {"name": "Titus", "chapters": 3, "testament": "NT"},
    {"name": "Philemon", "chapters": 1, "testament": "NT"},
    
    # General Epistles & Prophecy
    {"name": "Hebrews", "chapters": 13, "testament": "NT"},
    {"name": "James", "chapters": 5, "testament": "NT"},
    {"name": "1 Peter", "chapters": 5, "testament": "NT"},
    {"name": "2 Peter", "chapters": 3, "testament": "NT"},
    {"name": "1 John", "chapters": 5, "testament": "NT"},
    {"name": "2 John", "chapters": 1, "testament": "NT"},
    {"name": "3 John", "chapters": 1, "testament": "NT"},
    {"name": "Jude", "chapters": 1, "testament": "NT"},
    {"name": "Revelation", "chapters": 22, "testament": "NT"}
]

def get_next_chapter(current_book: str, current_chapter: int):
    """Calculates the next book and chapter in chronological Biblical sequence."""
    for idx, book_info in enumerate(BIBLE_BOOKS):
        if book_info["name"].lower() == current_book.lower():
            if current_chapter < book_info["chapters"]:
                return book_info["name"], current_chapter + 1
            else:
                # Move to the first chapter of next book
                if idx + 1 < len(BIBLE_BOOKS):
                    return BIBLE_BOOKS[idx + 1]["name"], 1
                else:
                    # Loop back to Genesis 1
                    return BIBLE_BOOKS[0]["name"], 1
    # Default fallback
    return "Genesis", 1
