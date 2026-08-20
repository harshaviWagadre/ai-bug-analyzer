import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
KB_PATH = BASE_DIR / "data" / "historical_bugs.json"


def load_knowledge_base():
    with open(KB_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def get_all_bugs():
    return load_knowledge_base()


def get_bug_by_id(bug_id):
    bugs = load_knowledge_base()

    for bug in bugs:
        if bug["bug_id"] == bug_id:
            return bug

    return None
