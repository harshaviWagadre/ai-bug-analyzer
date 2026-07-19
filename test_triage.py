from app.agents.triage_agent import triage_agent

bug = """
Application crashes after clicking Login button.
"""

print(triage_agent(bug))
