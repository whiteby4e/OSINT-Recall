#!/usr/bin/env python3
"""
OSINT-Recall - terminal-first personal OSINT knowledge base.
Standard-library only. Designed for Linux, macOS, Windows and SSH terminals.
"""

import argparse
import json
import os
import random
import re
import shutil
import sys
import textwrap
import webbrowser
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
STATE_DIR = Path.home() / ".osint-recall"
STATE_FILE = STATE_DIR / "state.json"
PACK_VERSION = 1

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[36m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"

# Platform is intentionally session-only. It must never be stored in state.json.
PLATFORM = None
ANSI_ENABLED = True


def color(code, value):
    if os.environ.get("NO_COLOR") or not ANSI_ENABLED or not sys.stdout.isatty():
        return value
    return code + value + RESET


def detect_platform():
    if sys.platform.startswith("win"):
        return "windows"
    if sys.platform == "darwin":
        return "macos"
    return "linux"


def choose_platform():
    global PLATFORM, ANSI_ENABLED

    detected = detect_platform()
    labels = {
        "windows": "Windows",
        "macos": "macOS",
        "linux": "Linux",
    }

    print(r"""
╔══════════════════════════════════════════════════════════╗
║                    OSINT-RECALL                         ║
╚══════════════════════════════════════════════════════════╝

  Choose your platform:

  [1] Windows
  [2] macOS
  [3] Linux
  [4] Auto detect
""")
    print(f"  Detected: {labels[detected]}")
    print("  This choice applies to this run only.")
    print("  It is never saved.")
    print()

    while True:
        try:
            choice = input("  Select > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            raise SystemExit(0)

        options = {
            "1": "windows",
            "2": "macos",
            "3": "linux",
            "4": detected,
        }
        if choice in options:
            PLATFORM = options[choice]
            # Windows is treated as ANSI-incompatible so old CMD terminals
            # do not display raw escape sequences.
            ANSI_ENABLED = PLATFORM != "windows"
            return

        print("  Enter 1, 2, 3, or 4.")


def load_json(name):
    with open(DATA / name, "r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    with open(temp, "w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
    temp.replace(path)


def load_state():
    default = {"favorites": [], "history": [], "last_query": ""}
    try:
        if STATE_FILE.exists():
            with open(STATE_FILE, "r", encoding="utf-8") as handle:
                value = json.load(handle)
            default.update(value)
    except (OSError, ValueError):
        pass
    return default


def save_state(state):
    save_json(STATE_FILE, state)


def clear_screen():
    if not sys.stdout.isatty():
        return
    if PLATFORM == "windows":
        os.system("cls")
    elif PLATFORM in ("linux", "macos"):
        os.system("clear")
    else:
        print("\033[2J\033[H", end="")


def pause():
    try:
        input(color(DIM, "\nPress Enter to continue..."))
    except (EOFError, KeyboardInterrupt):
        print()


def banner():
    print(color(CYAN, r"""
╔══════════════════════════════════════════════════════════╗
║                    OSINT-RECALL                         ║
║          Search • Learn • Recall • Generate             ║
╚══════════════════════════════════════════════════════════╝
"""))
    print(color(DIM, "  Personal OSINT knowledge base • terminal-first • stdlib only"))
    print()


def wrap(value, width=78, indent="  "):
    return textwrap.fill(str(value), width=width, initial_indent=indent,
                         subsequent_indent=indent)


def index_by_id(items):
    return {item["id"]: item for item in items}


def record_history(state, technique_id):
    history = [x for x in state["history"] if x != technique_id]
    history.insert(0, technique_id)
    state["history"] = history[:20]
    save_state(state)


def is_favorite(state, technique_id):
    return technique_id in state["favorites"]


def toggle_favorite(state, technique_id):
    if technique_id in state["favorites"]:
        state["favorites"].remove(technique_id)
        result = "Removed from favorites."
    else:
        state["favorites"].append(technique_id)
        result = "Added to favorites."
    save_state(state)
    return result


def print_item(item, number=None, state=None):
    prefix = f"{number:>2}. " if number is not None else ""
    marker = "★ " if state and is_favorite(state, item["id"]) else ""
    print(color(BOLD + BLUE, prefix + marker + item["title"]))
    print(color(DIM, f"    {item['category']}  •  {', '.join(item.get('tags', []))}"))


def search_techniques(techniques, query, category=None):
    query = query.lower().strip()
    return [
        item for item in techniques
        if (not category or item["category"].lower() == category.lower())
        and (not query or query in json.dumps(item, ensure_ascii=False).lower())
    ]


def choose_from(items, state, prompt="Select"):
    if not items:
        print(color(YELLOW, "No results."))
        return None
    while True:
        print()
        for i, item in enumerate(items, 1):
            print_item(item, i, state)
        raw = input(f"\n{prompt} [1-{len(items)}, b=back] > ").strip().lower()
        if raw in ("b", "back", "q", "quit"):
            return None
        if raw.isdigit() and 1 <= int(raw) <= len(items):
            return items[int(raw) - 1]
        print(color(YELLOW, "Enter a valid number or b."))


def show_technique(item, state, lookup=None):
    while True:
        clear_screen()
        print(color(CYAN, "━" * 72))
        print(color(BOLD, item["title"]))
        print(color(DIM, f"{item['category']}  •  {item.get('difficulty', 'Core')}  •  {', '.join(item.get('tags', []))}"))
        print(color(CYAN, "━" * 72))
        print(color(BOLD + CYAN, "CONCEPT"))
        print(wrap(item["summary"]))
        print()
        print(color(BOLD + GREEN, "HOW IT WORKS"))
        print(wrap(item["learn"]))
        if item.get("when_to_use"):
            print()
            print(color(BOLD + BLUE, "WHEN TO USE"))
            for value in item["when_to_use"]:
                print(wrap("• " + value))
        print()
        print(color(BOLD + MAGENTA, "EXAMPLES"))
        for example in item.get("examples", []):
            print(color(BOLD, "  " + example.get("title", "Example")))
            for key in ("query", "action", "record", "url"):
                if example.get(key):
                    print(wrap(f"{key.upper()}: {example[key]}", indent="    "))
            if example.get("why"):
                print(wrap("WHY: " + example["why"], indent="    "))
            print()
        if item.get("limitations"):
            print(color(BOLD + YELLOW, "LIMITATIONS"))
            for value in item["limitations"]:
                print(wrap("• " + value))
            print()
        if item.get("common_mistakes"):
            print(color(BOLD + RED, "COMMON MISTAKES"))
            for value in item["common_mistakes"]:
                print(wrap("• " + value))
            print()
        if item.get("related"):
            print(color(BOLD + CYAN, "RELATED"))
            names = [lookup[x]["title"] for x in item["related"] if lookup and x in lookup]
            print(wrap(" → ".join(names) if names else " → ".join(item["related"])))
            print()
        fav = "Remove favorite" if is_favorite(state, item["id"]) else "Add favorite"
        print(color(DIM, f"[f] {fav}   [b] Back   [q] Quit"))
        try:
            action = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return "quit"
        if action == "f":
            print(toggle_favorite(state, item["id"]))
            continue
        if action in ("b", "back", ""):
            return "back"
        if action in ("q", "quit"):
            return "quit"
def browse(techniques, state, category=None, lookup=None):
    items = [x for x in techniques if not category or x["category"] == category]
    item = choose_from(items, state)
    if item:
        record_history(state, item["id"])
        return show_technique(item, state, lookup)
    return "back"


def search_menu(techniques, state, lookup=None):
    try:
        query = input("Search > ").strip()
    except (EOFError, KeyboardInterrupt):
        return "quit"
    results = search_techniques(techniques, query)
    state["last_query"] = query
    save_state(state)
    item = choose_from(results, state, "Open")
    if item:
        record_history(state, item["id"])
        return show_technique(item, state, lookup)
    return "back"


def categories_menu(techniques, state, lookup=None):
    categories = sorted({x["category"] for x in techniques})
    while True:
        clear_screen()
        print(color(BOLD + CYAN, "CATEGORIES"))
        print()
        for i, category in enumerate(categories, 1):
            count = sum(x["category"] == category for x in techniques)
            print(f"  {i:>2}. {category:<20} {count} techniques")
        raw = input("\nCategory [number, b=back] > ").strip().lower()
        if raw in ("b", "back", ""):
            return "back"
        if raw.isdigit() and 1 <= int(raw) <= len(categories):
            result = browse(techniques, state, categories[int(raw) - 1], lookup)
            if result == "quit":
                return "quit"
        else:
            print(color(YELLOW, "Invalid selection."))


def dork_generator(dorks, state):
    clear_screen()
    print(color(BOLD + MAGENTA, "DORK GENERATOR"))
    print(color(DIM, "Generate passive/public-web search queries from templates."))
    print()
    for i, item in enumerate(dorks, 1):
        print(f"  {i:>2}. {item['name']}")
    raw = input("\nTemplate [number, b=back] > ").strip().lower()
    if raw in ("b", "back", ""):
        return "back"
    if not raw.isdigit() or not 1 <= int(raw) <= len(dorks):
        print(color(YELLOW, "Invalid template."))
        pause()
        return "back"
    item = dorks[int(raw) - 1]
    values = {}
    print()
    for field in item["fields"]:
        value = input(f"{field['label']} [{field.get('placeholder', '')}] > ").strip()
        if not value:
            print(color(YELLOW, "All fields are required."))
            pause()
            return "back"
        values[field["name"]] = value
    query = item["template"]
    for key, value in values.items():
        query = query.replace("{" + key + "}", value)
    state["last_query"] = query
    save_state(state)
    print()
    print(color(GREEN, "Generated query:"))
    print(color(BOLD, "  " + query))
    print()
    print(color(DIM, "Copy manually, or paste it into your preferred search engine."))
    pause()
    return "back"


def resources_menu(tools):
    clear_screen()
    print(color(BOLD + CYAN, "PUBLIC RESOURCES"))
    print()
    for i, tool in enumerate(tools, 1):
        print(f"  {i:>2}. {tool['name']:<20} {tool['type']}")
    raw = input("\nOpen [number, b=back] > ").strip().lower()
    if raw in ("b", "back", ""):
        return "back"
    if raw.isdigit() and 1 <= int(raw) <= len(tools):
        tool = tools[int(raw) - 1]
        print(f"\n{tool['name']}: {tool['url']}")
        try:
            webbrowser.open(tool["url"])
            print(color(GREEN, "Opened in the default browser."))
        except Exception:
            print(color(YELLOW, "Could not open a browser; use the URL above."))
        pause()
    else:
        print(color(YELLOW, "Invalid selection."))
        pause()
    return "back"


def random_technique(techniques, state, lookup=None):
    item = random.choice(techniques)
    record_history(state, item["id"])
    return show_technique(item, state, lookup)


def favorites_menu(techniques, state, lookup=None):
    lookup = index_by_id(techniques)
    items = [lookup[x] for x in state["favorites"] if x in lookup]
    item = choose_from(items, state)
    if item:
        return show_technique(item, state, lookup)
    return "back"


def history_menu(techniques, state, lookup=None):
    lookup = index_by_id(techniques)
    items = [lookup[x] for x in state["history"] if x in lookup]
    if not items:
        print(color(DIM, "History is empty."))
        pause()
        return "back"
    item = choose_from(items, state)
    if item:
        return show_technique(item, state)
    return "back"


def workflow_menu(workflows):
    while True:
        clear_screen()
        print(color(BOLD + MAGENTA, "RESEARCH WORKFLOWS"))
        print(color(DIM, "Passive public-information workflows with explicit verification steps."))
        print()
        for i, item in enumerate(workflows, 1):
            print(f"  {i:>2}. {item['title']}")
        raw = input("\nWorkflow [number, b=back] > ").strip().lower()
        if raw in ("b", "back", ""):
            return "back"
        if raw.isdigit() and 1 <= int(raw) <= len(workflows):
            item = workflows[int(raw) - 1]
            clear_screen()
            print(color(CYAN, "━" * 72))
            print(color(BOLD, item["title"]))
            print(color(CYAN, "━" * 72))
            print(wrap(item["goal"]))
            print()
            print(color(BOLD + GREEN, "STEPS"))
            for i, step in enumerate(item["steps"], 1):
                print(wrap(f"{i}. {step}"))
            print()
            print(color(BOLD + BLUE, "EXPECTED OUTPUTS"))
            for value in item.get("outputs", []):
                print(wrap("• " + value))
            print()
            print(color(BOLD + YELLOW, "SAFETY"))
            print(wrap(item.get("safety", "Use only public information and authorized research.")))
            pause()
        else:
            print(color(YELLOW, "Invalid selection."))


def stats(techniques, dorks, tools, workflows, state):
    categories = len({x["category"] for x in techniques})
    print(color(BOLD, "OSINT-RECALL STATUS"))
    print()
    print(f"  Techniques : {len(techniques)}")
    print(f"  Categories : {categories}")
    print(f"  Templates  : {len(dorks)}")
    print(f"  Resources  : {len(tools)}")
    print(f"  Workflows  : {len(workflows)}")
    print(f"  Favorites  : {len(state['favorites'])}")
    print(f"  History    : {len(state['history'])}")
    pause()


def export_pack(techniques, dorks, tools, workflows):
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    default = Path.cwd() / f"osint-recall-pack-{stamp}.json"
    raw = input(f"Export path [{default}] > ").strip()
    path = Path(raw) if raw else default
    pack = {
        "format": "OSINT-Recall Knowledge Pack",
        "version": PACK_VERSION,
        "exported_at": datetime.now().isoformat(timespec="seconds"),
        "techniques": techniques,
        "dorks": dorks,
        "tools": tools,
        "workflows": workflows,
    }
    save_json(path, pack)
    print(color(GREEN, f"Exported: {path}"))
    pause()
    return "back"


def import_pack():
    raw = input("Import JSON pack path > ").strip()
    if not raw:
        return "back"
    path = Path(raw)
    try:
        with open(path, "r", encoding="utf-8") as handle:
            pack = json.load(handle)
        if pack.get("format") != "OSINT-Recall Knowledge Pack":
            raise ValueError("Not an OSINT-Recall pack.")
        # Import to a separate local file; never overwrite the repository's data.
        target = STATE_DIR / ("imported-" + path.name)
        save_json(target, pack)
        print(color(GREEN, f"Imported pack saved locally: {target}"))
        print(color(DIM, "Repository knowledge files were not modified."))
    except (OSError, ValueError, TypeError) as exc:
        print(color(RED, f"Import failed: {exc}"))
    pause()
    return "back"


def main_loop():
    techniques = load_json("techniques.json")
    dorks = load_json("dorks.json")
    tools = load_json("tools.json")
    workflows = load_json("workflows.json")
    state = load_state()
    lookup = index_by_id(techniques)

    choose_platform()

    while True:
        clear_screen()
        banner()
        print(f"  {color(BOLD, str(len(techniques)))} techniques  •  "
              f"{len({x['category'] for x in techniques})} categories  •  "
              f"{len(dorks)} query templates  •  {len(workflows)} workflows")
        print()
        menu = [
            ("1", "Search techniques"),
            ("2", "Browse categories"),
            ("3", "Dork generator"),
            ("4", "Research workflows"),
            ("5", "Public resources"),
            ("6", "Random technique"),
            ("7", "Favorites"),
            ("8", "Recent history"),
            ("9", "Stats"),
            ("a", "Export knowledge pack"),
            ("i", "Import knowledge pack"),
            ("0", "Exit"),
        ]
        for key, label in menu:
            print(f"  [{key}] {label}")
        print()
        try:
            choice = input(color(CYAN, "Select > ")).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            return 0

        if choice == "1":
            result = search_menu(techniques, state, lookup)
        elif choice == "2":
            result = categories_menu(techniques, state, lookup)
        elif choice == "3":
            result = dork_generator(dorks, state)
        elif choice == "4":
            result = workflow_menu(workflows)
        elif choice == "5":
            result = resources_menu(tools)
        elif choice == "6":
            result = random_technique(techniques, state, lookup)
        elif choice == "7":
            result = favorites_menu(techniques, state, lookup)
        elif choice == "8":
            result = history_menu(techniques, state, lookup)
        elif choice == "9":
            stats(techniques, dorks, tools, workflows, state)
            result = "back"
        elif choice == "a":
            result = export_pack(techniques, dorks, tools, workflows)
        elif choice == "i":
            result = import_pack()
        elif choice == "0":
            print(color(GREEN, "Goodbye."))
            return 0
        else:
            print(color(YELLOW, "Unknown command."))
            pause()
            result = "back"

        if result == "quit":
            print(color(GREEN, "Goodbye."))
            return 0


def command_line_search(techniques, query):
    results = search_techniques(techniques, query)
    if not results:
        print("No techniques found.")
        return 1
    for item in results:
        print_item(item)
    return 0


def parse_args():
    parser = argparse.ArgumentParser(
        description="OSINT-Recall: terminal-first personal OSINT knowledge base."
    )
    parser.add_argument("--search", "-s", help="Search techniques and exit.")
    parser.add_argument("--random", action="store_true", help="Show a random technique and exit.")
    parser.add_argument("--no-color", action="store_true", help="Disable ANSI colors.")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.no_color:
        os.environ["NO_COLOR"] = "1"
    techniques = load_json("techniques.json")
    if args.search:
        return command_line_search(techniques, args.search)
    if args.random:
        state = load_state()
        show_technique(random.choice(techniques), state)
        return 0
    return main_loop()


if __name__ == "__main__":
    sys.exit(main())
