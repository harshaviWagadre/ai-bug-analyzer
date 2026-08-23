import json


def load_knowledge_base():

    with open("data/historical_bugs.json", "r", encoding="utf-8") as file:

        bugs = json.load(file)

    return bugs
