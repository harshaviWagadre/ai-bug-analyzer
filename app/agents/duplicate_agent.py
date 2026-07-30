from app.rag.retriever import retrieve_similar_bugs


def duplicate_detection_agent(current_bug):

    similar_bugs = retrieve_similar_bugs(current_bug, top_k=3)

    duplicates = []

    for item in similar_bugs:

        bug = item["bug"]

        duplicates.append(
            {
                "bug_id": bug["bug_id"],
                "title": bug["title"],
                "similarity_score": f"{round(item['score'] * 100)}%",
                "resolution_summary": bug["resolution"],
            }
        )

    return duplicates
