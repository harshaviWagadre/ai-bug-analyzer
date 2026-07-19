from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal

from app.models import BugReport

from app.agents.orchestrator import analyze_bug_with_agents

router = APIRouter()


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/submit-bug")
def submit_bug(bug_description: str, log_text: str = "", db: Session = Depends(get_db)):

    # Run both agents
    analysis = analyze_bug_with_agents(
        bug_description=bug_description, log_text=log_text
    )

    # Get Triage result
    triage = analysis["triage"]

    # Get Log Analysis result
    log_analysis = analysis["log_analysis"]

    # Create database record
    bug_report = BugReport(
        bug_description=bug_description,
        log_text=log_text,
        severity=triage.get("severity"),
        priority=triage.get("priority"),
        component=triage.get("component"),
        confidence=str(triage.get("confidence")),
        reasoning=triage.get("reasoning"),
        exception_type=log_analysis.get("exception_type"),
        failure_point=log_analysis.get("failure_point"),
        affected_code_path=log_analysis.get("affected_code_path"),
        summary=log_analysis.get("summary"),
    )

    # Save to database
    db.add(bug_report)

    db.commit()

    db.refresh(bug_report)

    return {
        "message": "Bug analyzed successfully",
        "bug_id": bug_report.id,
        "analysis": analysis,
    }
