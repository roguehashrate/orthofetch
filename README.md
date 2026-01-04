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

Simply run:

```bash
orthofetch
```

It will display today’s Orthodox calendar entry in a neat, aligned format with the Orthodox cross.

```bash
orthofetch --reading [NUM]
```

This will give you the reading well to read. So if you see [1] John 3.15-18 for example you will get those verses to read.

```bash
orthofetch --no-color
```

This will take the color out of it making it plain text. This will also work with `--reading [num]` if you want to use it that way.

---

## Data

Currently supports the year 2026. Future updates may include additional years or maybe things to make it prettier.

---

## License

Rogue Pact License v2
