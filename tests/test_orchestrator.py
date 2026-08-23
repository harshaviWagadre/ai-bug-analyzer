from app.agents.orchestrator import analyze_bug_with_agents

bug_description = """
The application crashes when the user clicks the Login button.
"""


log_text = """
java.lang.NullPointerException

at com.example.LoginService.login(LoginService.java:54)

Database connection failed
"""


result = analyze_bug_with_agents(bug_description=bug_description, log_text=log_text)


print(result)
