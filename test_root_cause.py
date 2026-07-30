from app.agents.root_cause_agent import root_cause_agent

bug = "Application crashes during login."

result = root_cause_agent(bug)

print(result)
