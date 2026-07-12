"""from sqlalchemy import Column, Integer, String

from app.database import Base


class Bug(Base):
    __tablename__ = "bugs"

    id = Column(Integer, primary_key=True, index=True)

    description = Column(String, nullable=False)

    filename = Column(String)"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.database import Base


class Bug(Base):
    __tablename__ = "bugs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, default="Untitled Bug")
    description = Column(Text, nullable=False)
    filename = Column(String(255), nullable=True)
    ai_analysis = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
