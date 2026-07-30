from difflib import SequenceMatcher

from app.rag.knowledge_base import load_knowledge_base


def similarity(text1, text2):
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()


def retrieve_similar_bugs(query, top_k=3):

    bugs = load_knowledge_base()

    results = []

    for bug in bugs:

        score = similarity(query, bug["description"])

        results.append({"bug": bug, "score": score})

    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:top_k]
