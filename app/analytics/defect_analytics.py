import json
from collections import Counter

DATA_FILE = "data/historical_bugs.json"


def load_bugs():

    with open(DATA_FILE, "r", encoding="utf-8") as file:

        return json.load(file)


def generate_analytics():

    bugs = load_bugs()

    severity_list = []
    component_list = []
    exception_list = []
    root_cause_list = []

    for bug in bugs:

        if bug.get("severity"):
            severity_list.append(bug["severity"])

        if bug.get("component"):
            component_list.append(bug["component"])

        if bug.get("exception"):
            exception_list.append(bug["exception"])

        if bug.get("root_cause"):
            root_cause_list.append(bug["root_cause"])

    return {
        "total_bugs": len(bugs),
        "severity": dict(Counter(severity_list)),
        "components": dict(Counter(component_list)),
        "exceptions": dict(Counter(exception_list)),
        "root_causes": dict(Counter(root_cause_list)),
    }
