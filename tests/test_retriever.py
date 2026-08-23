from app.rag.retriever import retrieve_similar_bugs

query = "Application crashes during login"

results = retrieve_similar_bugs(query)

for result in results:

    print("Similarity:", round(result["score"], 2))

    print("Bug ID:", result["bug"]["bug_id"])

    print("Title:", result["bug"]["title"])

    print("Description:", result["bug"]["description"])

    print("Root Cause:", result["bug"]["root_cause"])

    print("Resolution:", result["bug"]["resolution"])

    print("-" * 50)
