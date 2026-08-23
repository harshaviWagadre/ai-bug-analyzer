from app.rag.knowledge_base import load_knowledge_base

bugs = load_knowledge_base()

for bug in bugs:

    print(bug)
