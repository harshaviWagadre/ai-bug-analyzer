from fastapi import APIRouter, Form

from app.agents.triage_agent import triage_agent
from app.agents.log_analysis_agent import log_analysis_agent
from app.agents.root_cause_agent import root_cause_agent
from app.agents.duplicate_agent import duplicate_detection_agent
from app.agents.remediation_agent import remediation_agent

router = APIRouter()


@router.post("/analyze")
def analyze(bug: str = Form(...)):

    triage = triage_agent(bug)

    log = log_analysis_agent(bug)

    root = root_cause_agent(bug)

    duplicate = duplicate_detection_agent(bug)

    remedy = remediation_agent(root, duplicate)

    return {
        "triage": triage,
        "log_analysis": log,
        "root_cause": root,
        "duplicate_bug": duplicate,
        "remediation": remedy,
    }
