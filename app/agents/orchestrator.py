from app.agents.triage_agent import triage_agent
from app.agents.log_analysis_agent import log_analysis_agent


def analyze_bug_with_agents(bug_description: str, log_text: str = ""):
    """
    Runs both agents and combines their outputs.
    """

    # If no separate log is provided,
    # analyze the bug description itself.
    if not log_text:
        log_text = bug_description

    # Run Triage Agent
    triage_result = triage_agent(bug_description)

    # Run Log Analysis Agent
    log_analysis_result = log_analysis_agent(log_text)

    # Combine both results
    combined_result = {"triage": triage_result, "log_analysis": log_analysis_result}

    return combined_result
