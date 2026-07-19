"""from sqlalchemy import Column, Integer, String

from app.database import Base


class Bug(Base):
    __tablename__ = "bugs"

    id = Column(Integer, primary_key=True, index=True)

    description = Column(String, nullable=False)

    filename = Column(String)"""

from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class BugReport(Base):

    __tablename__ = "bug_reports"

    id = Column(Integer, primary_key=True, index=True)

    bug_description = Column(Text, nullable=False)

    log_text = Column(Text, nullable=True)

    severity = Column(String, nullable=True)

    priority = Column(String, nullable=True)

    component = Column(String, nullable=True)

    confidence = Column(String, nullable=True)

    reasoning = Column(Text, nullable=True)

    exception_type = Column(String, nullable=True)

    failure_point = Column(String, nullable=True)

    affected_code_path = Column(String, nullable=True)

    summary = Column(Text, nullable=True)
