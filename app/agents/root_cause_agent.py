from app.rag.retriever import retrieve_similar_bugs


def root_cause_agent(current_bug):

    similar_bugs = retrieve_similar_bugs(current_bug)

    best_match = similar_bugs[0]

    bug = best_match["bug"]

    score = round(best_match["score"] * 100)

    result = {
        "root_cause_hypothesis": bug["root_cause"],
        "confidence": f"{score}%",
        "supporting_evidence": {
            "bug_id": bug["bug_id"],
            "title": bug["title"],
            "exception": bug["exception"],
            "resolution": bug["resolution"],
        },
    }

    return result

