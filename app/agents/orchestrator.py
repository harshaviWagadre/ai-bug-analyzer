from app.agents.triage_agent import triage_agent
from app.agents.log_analysis_agent import log_analysis_agent
from app.agents.root_cause_agent import root_cause_agent
from app.agents.duplicate_agent import duplicate_detection_agent
from app.agents.remediation_agent import remediation_agent


def orchestrate(bug):

    triage = triage_agent(bug)

    log_analysis = log_analysis_agent(bug)

    root_cause = root_cause_agent(bug)

    duplicate_bug = duplicate_detection_agent(bug)

    remediation = remediation_agent(bug, duplicate_bug)

    return {
        "triage": triage,
        "log_analysis": log_analysis,
        "root_cause": root_cause,
        "duplicate_bug": duplicate_bug,
        "remediation": remediation,
    }
