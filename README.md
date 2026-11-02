<div align="center">

# OSINT-Recall 🔎

**A terminal-first knowledge base for learning public-information research.**

Search techniques, understand workflows, build structured queries, and keep useful knowledge organized — without a database server or third-party Python packages.

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/Dependencies-Standard%20Library-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

**Search → Learn → Verify → Recall → Generate**

</div>

---

## 🧠 Why OSINT-Recall?

OSINT-Recall is a structured learning and reference system, not a random collection of search tricks. Each technique can include its definition, mechanism, use cases, examples, limitations, common mistakes, and related methods.

## ✨ Features

- 🔎 Full-text technique search.
- 📚 Browse organized categories.
- 🧠 Read structured learning pages.
- 🧪 Explore passive research workflows.
- 🧩 Generate search queries with purpose and notes.
- 🛠 Browse a directory of public resources.
- ⭐ Save favorites and revisit recent items.
- 🎲 Discover a random learning topic.
- 📊 View usage statistics.
- 📤 Export and 📥 import portable knowledge packs.
- ⌨️ Use the interactive terminal interface or CLI search mode.
- 🎨 ANSI colors with `NO_COLOR` support.
- 🪶 Run with Python's standard library only.

## ⚡ Quick start

```bash
git clone https://github.com/whiteby4e/OSINT-Recall.git
cd OSINT-Recall
python osint_recall.py
```

**Requirements:** Python 3.8 or newer. No `pip install` step is needed.

For CLI search mode, inspect the program's command-line help:

```bash
python osint_recall.py --help
```

## 🗂️ Knowledge files

The knowledge base is stored as editable JSON:

```text
data/
├── techniques.json
├── dorks.json
├── tools.json
└── workflows.json
```

You can inspect and contribute to the data without running a database service. Favorites and history are stored locally in:

```text
~/.osint-recall/state.json
```

The platform selection is session-only and is not saved.

## 🔍 A useful research mindset

OSINT-Recall encourages separating:

1. **Observation** — what was directly seen.
2. **Inference** — what an observation might suggest.
3. **Verification** — independent evidence that supports a conclusion.
4. **Limitations** — what the method cannot establish.
5. **Confidence** — how strongly the evidence supports the conclusion.

This helps prevent assumptions from being mistaken for facts.

## 🛡️ Scope and responsible use

OSINT-Recall is intended for lawful learning and research using public information. It is not an intrusion, credential collection, surveillance, or access-control-bypass toolkit.

Do not use it to obtain passwords or tokens, access private systems, bypass authentication, stalk or harass people, or expose private information. Respect privacy, applicable laws, and website terms.

Examples use reserved domains such as `example.org` and non-sensitive scenarios.

## 🧪 Roadmap

- [x] Structured techniques with limitations and examples
- [x] Passive research workflows
- [x] Query generator
- [x] Public resource directory
- [x] Favorites and history
- [x] Import / export
- [x] Per-run platform selection
- [ ] More verified knowledge packs
- [ ] Confidence-scoring interface
- [ ] Optional GUI frontend
- [ ] Optional packaged binaries

## 📄 License

MIT — see [LICENSE](LICENSE).
