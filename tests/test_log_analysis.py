from app.agents.log_analysis_agent import log_analysis_agent

log = """
java.lang.NullPointerException

at com.example.LoginService.login(LoginService.java:54)

Database connection failed
"""


result = log_analysis_agent(log)

print(result)
