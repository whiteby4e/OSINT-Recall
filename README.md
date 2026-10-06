# OSINT-Recall 🔎

A **terminal-first personal OSINT knowledge base** for remembering techniques, learning how they work, and generating safe public-web search queries.

> **Search → Learn → Recall → Generate**

## Why terminal-first?

OSINT-Recall is designed to be useful on Linux, SSH sessions, lightweight machines, and older Windows installations without requiring a GUI framework.

- 🪶 Standard-library only
- 🐧 Linux-friendly
- 🪟 Works on Windows/macOS too
- 🔌 No database
- ⌨️ Keyboard-first workflow
- 📦 Knowledge stored as editable JSON
- 🌐 Public resources open in the default browser

## Features

- 🔎 Search techniques across titles, categories, tags, summaries, examples and notes
- 📚 Browse techniques by category
- 🧠 Detailed learning view
- ⭐ Local favorites
- 🕘 Recently viewed history
- ⚡ Dork/query generator
- 🎲 Random technique
- 🌐 Public OSINT resource launcher
- 📊 Local statistics
- 📤 Export knowledge packs
- 📥 Import knowledge packs without overwriting repository data
- 🖥️ Per-run Windows/macOS/Linux platform selection
- 🎨 Automatic terminal colors with `NO_COLOR` support
- 🧰 Optional command-line search mode

## Run

Python 3.8+ is recommended.

```text
git clone https://github.com/whiteby4e/OSINT-Recall.git
cd OSINT-Recall
python osint_recall.py
```

No `pip install` is required.

On startup, OSINT-Recall asks which terminal environment you want to target:

```text
[1] Windows
[2] macOS
[3] Linux
[4] Auto detect
```

The choice is **session-only**. It is never written to `~/.osint-recall/state.json`, so the same copy can be used on Windows, Linux, and macOS without carrying a platform setting between machines.

Windows mode disables ANSI terminal styling to stay friendly with older CMD environments. Linux/macOS mode enables ANSI styling when the terminal supports it.

### Quick commands

```text
python osint_recall.py --search "certificate"
python osint_recall.py --random
python osint_recall.py --no-color
```

On Linux you can also run:

```bash
chmod +x osint_recall.py
./osint_recall.py
```

## Project layout

```text
OSINT-Recall/
├── osint_recall.py
├── data/
│   ├── techniques.json
│   ├── dorks.json
│   └── tools.json
├── README.md
└── LICENSE
```

User state is stored outside the repository:

```text
~/.osint-recall/state.json
```

This keeps favorites/history personal and prevents the repository's knowledge files from being modified by normal use. The selected platform is **not** part of this state.

## Adding a technique

Add an object to `data/techniques.json` with:

- `id`
- `title`
- `category`
- `tags`
- `summary`
- `learn`
- `examples`
- `notes`

The program loads JSON at startup. No database server is required.

## Knowledge packs

Use **Export knowledge pack** to create a portable JSON snapshot of the current knowledge base.

Import stores the supplied pack under `~/.osint-recall/` and does not overwrite repository data.

## Scope & safety

OSINT-Recall is designed for lawful research using public information. It is a knowledge and learning tool, not an intrusion toolkit.

Do not use it to:

- obtain passwords, authentication tokens, or private data
- bypass access controls
- stalk, harass, or expose private people
- probe systems without authorization

Use examples against domains and data you own, operate, or are explicitly authorized to research.

## Roadmap

- [x] Terminal-first interface
- [x] Favorites / bookmarks
- [x] Recently viewed techniques
- [x] Keyboard-first navigation
- [x] Query generator
- [x] Import/export knowledge packs
- [x] Per-run platform selection
- [ ] More knowledge packs
- [ ] Technique difficulty and confidence
- [ ] Optional GUI frontend
- [ ] Optional packaged binaries

## License

MIT
