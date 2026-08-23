import json
import os

DATA_FILE = "data/historical_bugs.json"


def add_resolved_bug(bug):
    """
    Add a confirmed resolved bug to the historical knowledge base.
    """

    # If file does not exist, create an empty list
    if not os.path.exists(DATA_FILE):
        bugs = []
    else:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            bugs = json.load(file)

    # Generate new bug ID
    if bugs:
        new_id = max(bug_item.get("bug_id", 0) for bug_item in bugs) + 1
    else:
        new_id = 1

    # Add ID to new bug
    bug["bug_id"] = new_id

    # Add bug to knowledge base
    bugs.append(bug)

    # Save updated knowledge base
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(bugs, file, indent=4, ensure_ascii=False)

    return bug
