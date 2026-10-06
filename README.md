# OSINT-Recall 🔎

A **terminal-first personal OSINT knowledge base** for learning public-information research methods, recalling concepts, building passive workflows, and generating structured search queries.

> **Search → Learn → Verify → Recall → Generate**

## What makes it different?

OSINT-Recall is a **knowledge system**, not a collection of random search tricks.

Techniques can contain definitions, mechanism, use cases, distinct examples, limitations, common mistakes, and related methods. The project also includes reusable passive workflows, structured query templates, public resources, favorites, history, and portable knowledge packs.

## Features

- 🔎 Full-text technique search
- 📚 Category browsing
- 🧠 Structured learning pages
- 🧪 Passive research workflows
- 🧩 Query generator with purpose and notes
- 🛠 Public resource directory
- ⭐ Favorites
- 🕘 Recently viewed history
- 🎲 Random learning
- 📊 Statistics
- 📤 Export / 📥 import knowledge packs
- 🖥️ Per-run Windows/macOS/Linux terminal profile
- 🎨 ANSI colors with `NO_COLOR`
- ⌨️ CLI search mode
- 🪶 Standard-library Python runtime

## Run

Python 3.8+:

```text
git clone https://github.com/whiteby4e/OSINT-Recall.git
cd OSINT-Recall
python osint_recall.py
```

No pip dependencies are required.

The platform selection is **session-only** and is never saved. Favorites and history remain in `~/.osint-recall/state.json`.

## Data model

```text
data/
├── techniques.json
├── dorks.json
├── tools.json
└── workflows.json
```

The JSON files are intentionally human-editable. No database server is required.

## Knowledge quality

The project separates:
1. **Observation** — what was directly seen.
2. **Inference** — what an observation may suggest.
3. **Verification** — independent evidence supporting a conclusion.
4. **Limitations** — what the method cannot establish.
5. **Confidence** — how strongly the evidence supports the conclusion.

Examples use reserved domains such as `example.org` and non-sensitive scenarios.

## Scope & safety

OSINT-Recall is for lawful research using public information. It is **not** an intrusion, credential, surveillance, or access-control-bypass toolkit.

Do not use it to obtain passwords or tokens, access private systems, bypass authentication, stalk or harass people, or expose private information.

## Project layout

```text
OSINT-Recall/
├── osint_recall.py
├── data/
│   ├── techniques.json
│   ├── dorks.json
│   ├── tools.json
│   └── workflows.json
├── README.md
└── LICENSE
```

## Roadmap

- [x] Structured techniques with limitations and examples
- [x] Passive research workflows
- [x] Query generator
- [x] Public resource directory
- [x] Favorites / history
- [x] Import / export
- [x] Per-run platform selection
- [ ] More verified knowledge packs
- [ ] Confidence scoring UI
- [ ] Optional GUI frontend
- [ ] Optional packaged binaries

## License

MIT
