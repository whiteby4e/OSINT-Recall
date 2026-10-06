# OSINT-Recall 🔎

A lightweight personal OSINT knowledge base for remembering techniques, learning how they work, and generating safe public-web search queries.

> Search → Find → Learn → Generate

## Features

- 🔎 Fast local search across techniques, categories, tags, and descriptions
- 🧠 Learn view for each technique
- ⚡ Dork Generator with reusable templates
- 🌐 Public OSINT resource shortcuts
- 📦 JSON-based knowledge base — easy to edit and extend
- 🪶 Lightweight PySide6 desktop UI

## Run

Python 3.10+ is recommended.

~~~text
git clone https://github.com/whiteby4e/OSINT-Recall.git
cd OSINT-Recall
python -m pip install -r requirements.txt
python app.py
~~~

## Project layout

~~~text
OSINT-Recall/
├── app.py
├── data/
│   ├── techniques.json
│   ├── dorks.json
│   └── tools.json
├── requirements.txt
└── README.md
~~~

## Adding a technique

Add an object to data/techniques.json with the fields:
- id
- title
- category
- tags
- summary
- learn
- examples
- notes

The app loads the JSON at startup, so no database server is required.

## Scope & safety

OSINT-Recall is designed for lawful research using public information. It is a knowledge and learning tool, not an intrusion toolkit.

Do not use it to:
- obtain passwords, authentication tokens, or private data
- bypass access controls
- stalk, harass, or expose private people
- probe systems without authorization

Use examples against domains and data you own, operate, or are explicitly authorized to research.

## Roadmap

- [ ] Favorites / bookmarks
- [ ] Technique difficulty and confidence
- [ ] Recently viewed techniques
- [ ] More query generators
- [ ] Import/export knowledge packs
- [ ] Keyboard-first navigation
- [ ] Optional themes
- [ ] Windows EXE packaging

## License

MIT
