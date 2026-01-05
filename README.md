# orthofetch

A terminal-based Orthodox Christian calendar made in a "fetch" style for Linux, showing today's saints, feasts, fasting, and readings.

---

## Install

Run this one-liner:

```bash
/bin/sh -c "$(curl -fsSL https://raw.githubusercontent.com/roguehashrate/orthofetch/main/install.sh)"
```

This will:

- Copy the `orthofetch` script to `~/.local/bin`
- Copy the calendar data to `~/.local/share/orthofetch`
- Copy the bible data to `~/.local/share/orthofetch/bible`

Make sure `~/.local/bin` is in your `PATH` to run `orthofetch` from anywhere.

---

## Usage

### Daily Calendar

Simply run:

```bash
orthofetch
```

It will display today's Orthodox calendar entry in a neat, aligned format with the Orthodox cross.

```bash
orthofetch --reading [NUM]
```

This will give you the full text of a specific reading for today. So if you see [1] John 3.15-18 for example you will get those verses to read.

### Bible Reading

```bash
orthofetch --bible
```

This will display all available Bible books organized by testament.

```bash
orthofetch --bible [BOOK]
```

This will list all chapters in the specified book (e.g., `--bible John`).

```bash
orthofetch --bible [BOOK] [CHAPTER]
```

This will display the full chapter (e.g., `--bible John 3`).

```bash
orthofetch --bible [BOOK] [CHAPTER]:[VERSE]
```

This will display a specific verse (e.g., `--bible John 3:16`).

```bash
orthofetch --bible [BOOK] [CHAPTER]:[VERSE]-[VERSE]
```

This will display a range of verses (e.g., `--bible John 3:16-17`).

### Random Verses

```bash
orthofetch --random-verse
```

This will display a random verse from anywhere in the Bible.

```bash
orthofetch --random-verse [BOOK]
```

This will display a random verse from the specified book (e.g., `--random-verse Proverbs`).

### Display Options

```bash
orthofetch --no-color
```

This will take the color out of it making it plain text. This will also work with all other commands if you want to use it that way.

---

## Data

Currently supports the year 2026.

---

## License

Rogue Pact License v2
