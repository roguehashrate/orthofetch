#!/bin/sh
set -e

BIN_DIR="$HOME/.local/bin"
DATA_DIR="$HOME/.local/share/orthofetch"

mkdir -p "$BIN_DIR"
mkdir -p "$DATA_DIR"

# Download main script
curl -fsSL https://raw.githubusercontent.com/roguehashrate/orthofetch/main/orthofetch.py -o "$BIN_DIR/orthofetch"
chmod +x "$BIN_DIR/orthofetch"

# Download calendar data
curl -fsSL https://raw.githubusercontent.com/roguehashrate/orthofetch/main/data/orthodox_calendar_2026.txt -o "$DATA_DIR/orthodox_calendar_2026.txt"

# Create bible directory and download all Bible files
BIBLE_DIR="$DATA_DIR/bible"
mkdir -p "$BIBLE_DIR"

# Function to download Bible books
download_bible_book() {
    local book=$1
    local book_dir="$BIBLE_DIR/$book"
    mkdir -p "$book_dir"
    
    # Download all chapters for this book (1-50 chapters max)
    for chapter in $(seq 1 50); do
        local url="https://raw.githubusercontent.com/roguehashrate/orthofetch/main/data/bible/$book/ch$chapter.txt"
        local file="$book_dir/ch$chapter.txt"
        
        # Try to download the chapter file, break if it doesn't exist
        if curl -fsSL "$url" -o "$file" 2>/dev/null; then
            echo "Downloaded $book chapter $chapter"
        else
            rm -f "$file"  # Remove empty file if download failed
            break
        fi
    done
}

# List of Bible books to download
BIBLE_BOOKS="GEN EXO LEV NUM DEU JOS JDG RUT 1SA 2SA 1KI 2KI 1CH 2CH EZR NEH EST JOB PSA PRO ECC SNG ISA JER LAM EZK DAN HOS JOL AMO OBA JON MIC NAM HAB ZEP HAG ZEC MAL MAT MRK LUK JHN ACT ROM 1CO 2CO GAL EPH PHP COL 1TH 2TH 1TI 2TI TIT PHM HEB JAS 1PE 2PE 1JO 2JO 3JO JUD REV"

# Download each Bible book
for book in $BIBLE_BOOKS; do
    echo "Downloading $book..."
    download_bible_book "$book"
done

echo "[*] Installation complete!"
echo "Run 'orthofetch' from anywhere."
echo "Orthofetch script installed to $BIN_DIR."
echo "Data installed to $DATA_DIR."
