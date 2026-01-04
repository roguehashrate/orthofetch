#!/usr/bin/env python3
import datetime
import textwrap
import os
import argparse
import re

# Locate calendar file
if os.path.exists("data/orthodox_calendar_2026.txt"):
    CALENDAR_FILE = "data/orthodox_calendar_2026.txt"
    BIBLE_DIR = "data/bible"
else:
    CALENDAR_FILE = os.path.expanduser(
        "~/.local/share/orthofetch/orthodox_calendar_2026.txt"
    )
    BIBLE_DIR = os.path.expanduser("~/.local/share/orthofetch/bible")

# Book name to 3-letter code mapping
BOOK_CODES = {
    "Genesis": "GEN", "Exodus": "EXO", "Leviticus": "LEV", "Numbers": "NUM", "Deuteronomy": "DEU",
    "Joshua": "JOS", "Judges": "JDG", "Ruth": "RUT", "1 Samuel": "1SA", "2 Samuel": "2SA",
    "1 Kings": "1KI", "2 Kings": "2KI", "1 Chronicles": "1CH", "2 Chronicles": "2CH", "Ezra": "EZR",
    "Nehemiah": "NEH", "Esther": "EST", "Job": "JOB", "Psalms": "PSA", "Proverbs": "PRO",
    "Ecclesiastes": "ECC", "Song of Solomon": "SNG", "Isaiah": "ISA", "Jeremiah": "JER",
    "Lamentations": "LAM", "Ezekiel": "EZK", "Daniel": "DAN", "Hosea": "HOS", "Joel": "JOL",
    "Amos": "AMO", "Obadiah": "OBA", "Jonah": "JON", "Micah": "MIC", "Nahum": "NAM",
    "Habakkuk": "HAB", "Zephaniah": "ZEP", "Haggai": "HAG", "Zechariah": "ZEC", "Malachi": "MAL",
    "Matthew": "MAT", "Mark": "MRK", "Luke": "LUK", "John": "JHN", "Acts": "ACT",
    "Romans": "ROM", "1 Corinthians": "1CO", "2 Corinthians": "2CO", "Galatians": "GAL",
    "Ephesians": "EPH", "Philippians": "PHP", "Colossians": "COL", "1 Thessalonians": "1TH",
    "2 Thessalonians": "2TH", "1 Timothy": "1TI", "2 Timothy": "2TI", "Titus": "TIT",
    "Philemon": "PHM", "Hebrews": "HEB", "James": "JAS", "1 Peter": "1PE", "2 Peter": "2PE",
    "1 John": "1JN", "2 John": "2JN", "3 John": "3JN", "Jude": "JUD", "Revelation": "REV",
    "Wisdom of Solomon": "WIS", "Sirach": "SIR", "Baruch": "BAR", "1 Maccabees": "1MA",
    "2 Maccabees": "2MA", "Tobit": "TOB", "Judith": "JDT", "Esther (Greek)": "ESG",
    "Psalm 151": "P151", "Prayer of Manasseh": "MAN", "1 Esdras": "1ES", "2 Esdras": "2ES"
}

# Compact Orthodox Cross
ORTHODOX_CROSS = [
    "      ██",
    "    ██████",
    "      ██",
    "  ██████████",
    "      ██",
    "      ██",
    "    ████",
    "      ████",
    "      ██"
]

TEXT_GAP = 8
WRAP_WIDTH = 60

FIELDS = ["[Saints]:", "[Feasts]:", "[Fasting]:", "[Readings]:"]
MAX_FIELD_WIDTH = max(len(f) for f in FIELDS)
CROSS_WIDTH = max(len(line) for line in ORTHODOX_CROSS)


def parse_reading_reference(reference):
    """Parse a reading reference like 'Genesis 3:1-8' or 'John 10:9'"""
    # Handle special case for Wisdom of Solomon
    reference = reference.replace("Wisdom", "Wisdom of Solomon")
    
    # Pattern to match: Book Chapter:Verse-Verse or Book Chapter:Verse
    pattern = r"([0-9A-Za-z\s]+)\s+(\d+)[.:](\d+)(?:[-:]?(\d+))?"
    match = re.match(pattern, reference.strip())
    
    if match:
        book = match.group(1).strip()
        chapter = int(match.group(2))
        start_verse = int(match.group(3))
        end_verse = int(match.group(4)) if match.group(4) else start_verse
        
        return book, chapter, start_verse, end_verse
    return None


def get_bible_text(book, chapter, start_verse, end_verse):
    """Retrieve bible text for the specified reference"""
    book_code = BOOK_CODES.get(book)
    if not book_code:
        return f"Book '{book}' not found."
    
    chapter_file = os.path.join(BIBLE_DIR, book_code, f"ch{chapter}.txt")
    if not os.path.exists(chapter_file):
        return f"Chapter {chapter} of {book} not found."
    
    try:
        with open(chapter_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        verses = {}
        current_verse = None
        verse_text = []
        
        for line in lines:
            line = line.strip()
            if line.isdigit():
                if current_verse is not None:
                    verses[current_verse] = " ".join(verse_text)
                current_verse = int(line)
                verse_text = []
            elif current_verse is not None:
                verse_text.append(line)
        
        # Add the last verse
        if current_verse is not None:
            verses[current_verse] = " ".join(verse_text)
        
        # Collect requested verses
        result_lines = []
        for verse_num in range(start_verse, end_verse + 1):
            if verse_num in verses:
                result_lines.append(f"{verse_num} {verses[verse_num]}")
            else:
                result_lines.append(f"{verse_num} [Verse not found]")
        
        if result_lines:
            header = f"{book} {chapter}:{start_verse}"
            if end_verse != start_verse:
                header += f"-{end_verse}"
            return f"\n{header}\n" + "\n".join(result_lines)
        else:
            return f"Verses {start_verse}-{end_verse} not found in {book} {chapter}."
            
    except Exception as e:
        return f"Error reading {book} {chapter}:{start_verse}-{end_verse}: {e}"


def display_reading(reading_number):
    """Display the full text of a specific reading for today"""
    today = datetime.date.today()
    calendar = parse_calendar(CALENDAR_FILE)
    today_str = today.strftime("📅 %A, %B %-d, %Y")

    entry = None
    for key in calendar:
        if key.startswith(today_str):
            entry = calendar[key]
            break

    if not entry:
        print("No entry for today in the calendar.")
        return

    readings_text = entry.get("[Readings]:", "")
    if not readings_text:
        print("No readings for today.")
        return

    # Split readings by " • " first
    readings = [r.strip() for r in readings_text.split(" • ") if r.strip()]
    
    # Filter out "Composite X - " prefix and handle complex formats
    clean_readings = []
    for reading in readings:
        if reading.startswith("Composite"):
            # Remove "Composite X - " prefix
            clean_reading = re.sub(r'^Composite \d+ -\s*', '', reading)
            # Handle cases with semicolons and multiple readings
            if ';' in clean_reading:
                # Split by semicolon first
                semicolon_parts = [p.strip() for p in clean_reading.split(';')]
                for part in semicolon_parts:
                    if part:
                        # Then split by • within each semicolon part
                        sub_parts = [r.strip() for r in part.split(" • ") if r.strip()]
                        clean_readings.extend(sub_parts)
            else:
                # Split by • as before
                sub_parts = [r.strip() for r in clean_reading.split(" • ") if r.strip()]
                clean_readings.extend(sub_parts)
        else:
            clean_readings.append(reading)
    
    # Filter out any empty entries
    clean_readings = [r for r in clean_readings if r and not r.isdigit()]

    try:
        reading_idx = int(reading_number) - 1
        if reading_idx < 0 or reading_idx >= len(clean_readings):
            print(f"Reading number {reading_number} not found. There are {len(clean_readings)} readings today.")
            print("Available readings:")
            for i, reading in enumerate(clean_readings, 1):
                print(f"  {i}. {reading}")
            return

        reading_ref = clean_readings[reading_idx]
        parsed = parse_reading_reference(reading_ref)
        
        if parsed:
            book, chapter, start_verse, end_verse = parsed
            text = get_bible_text(book, chapter, start_verse, end_verse)
            print(text)
        else:
            print(f"Could not parse reading reference: {reading_ref}")
            
    except ValueError:
        print("Please provide a valid reading number (e.g., --reading 1)")


def parse_calendar(file_path):
    calendar = {}
    with open(file_path, "r", encoding="utf-8") as f:
        current_date = None
        entry = {}
        for line in f:
            line = line.strip()
            if line.startswith("📅"):
                if current_date:
                    calendar[current_date] = entry
                current_date = line
                entry = {field: "" for field in FIELDS}
            elif any(line.startswith(field) for field in FIELDS):
                for field in FIELDS:
                    if line.startswith(field):
                        entry[field] = line[len(field):].strip()
                        break
        if current_date:
            calendar[current_date] = entry
    return calendar


def wrap_readings(text, width):
    # Parse the readings the same way as display_reading to get clean list
    readings = [r.strip() for r in text.split(" • ") if r.strip()]
    clean_readings = []
    
    for reading in readings:
        if reading.startswith("Composite"):
            # Remove "Composite X - " prefix
            clean_reading = re.sub(r'^Composite \d+ -\s*', '', reading)
            # Handle cases with semicolons and multiple readings
            if ';' in clean_reading:
                # Split by semicolon first
                semicolon_parts = [p.strip() for p in clean_reading.split(';')]
                for part in semicolon_parts:
                    if part:
                        # Then split by • within each semicolon part
                        sub_parts = [r.strip() for r in part.split(" • ") if r.strip()]
                        clean_readings.extend(sub_parts)
            else:
                # Split by • as before
                sub_parts = [r.strip() for r in clean_reading.split(" • ") if r.strip()]
                clean_readings.extend(sub_parts)
        else:
            clean_readings.append(reading)
    
    # Filter out any empty entries
    clean_readings = [r for r in clean_readings if r and not r.isdigit()]
    
    lines = []
    
    for i, reading in enumerate(clean_readings, 1):
        # Add number prefix: [1] reading
        numbered_reading = f"[{i}] {reading}"
        wrapped = textwrap.wrap(
            numbered_reading,
            width=width - 2,
            subsequent_indent="  "  # Indent continuation lines
        )
        for j, line in enumerate(wrapped):
            if j == 0:
                lines.append("  " + line)
            else:
                lines.append(line)

    return lines if lines else [""]


def display_today():
    today = datetime.date.today()
    calendar = parse_calendar(CALENDAR_FILE)
    today_str = today.strftime("📅 %A, %B %-d, %Y")

    entry = None
    for key in calendar:
        if key.startswith(today_str):
            entry = calendar[key]
            break

    if not entry:
        print("No entry for today in the calendar.")
        return

    wrapped_fields = {}

    for field in FIELDS:
        text = entry.get(field, "")
        if field == "[Readings]:":
            wrapped_fields[field] = wrap_readings(text, WRAP_WIDTH)
        else:
            wrapped = textwrap.wrap(text, width=WRAP_WIDTH)
            wrapped_fields[field] = wrapped if wrapped else [""]

    cross_height = len(ORTHODOX_CROSS)
    cross_index = 0

    for field in FIELDS:
        lines = wrapped_fields[field]
        for i, line in enumerate(lines):
            cross_part = (
                ORTHODOX_CROSS[cross_index]
                if cross_index < cross_height
                else " " * CROSS_WIDTH
            )

            label = field.ljust(MAX_FIELD_WIDTH) if i == 0 else " " * MAX_FIELD_WIDTH

            print(
                f"{cross_part.ljust(CROSS_WIDTH)}"
                f"{' ' * TEXT_GAP}"
                f"{label} {line}"
            )

            cross_index += 1

    # Print remaining cross lines if any
    for i in range(cross_index, cross_height):
        print(ORTHODOX_CROSS[i])


def main():
    parser = argparse.ArgumentParser(description="Orthodox Christian calendar fetch tool")
    parser.add_argument("--reading", type=int, help="Display full text of specific reading number for today")
    
    args = parser.parse_args()
    
    if args.reading is not None:
        if args.reading <= 0:
            print("Reading number must be positive.")
            return
        display_reading(args.reading)
    else:
        display_today()


if __name__ == "__main__":
    main()
