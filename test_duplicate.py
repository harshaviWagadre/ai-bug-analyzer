from app.agents.duplicate_agent import duplicate_detection_agent

bug = "Application crashes during login."

duplicates = duplicate_detection_agent(bug)

for duplicate in duplicates:

    print(duplicate)
