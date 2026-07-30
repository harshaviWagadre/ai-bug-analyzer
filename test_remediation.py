from app.agents.remediation_agent import remediation_agent

duplicate = {"resolution": "Add null validation before accessing user properties."}

root = {"root_cause": "User object is null."}

print(remediation_agent(root, duplicate))
