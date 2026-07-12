from pydantic import BaseModel, Field
from typing import Any


class AnalyzeResponse(BaseModel):
    message: str
    bug_id: int
    title: str
    filename: str | None = None
    ai_analysis: dict[str, Any]


class BugRecord(BaseModel):
    id: int
    title: str
    description: str
    filename: str | None = None
    ai_analysis: dict[str, Any]
    created_at: str | None = None


class BugListResponse(BaseModel):
    bugs: list[BugRecord]
