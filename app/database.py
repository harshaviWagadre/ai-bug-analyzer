from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./bugs.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def init_db() -> None:
    """Create the database tables and refresh the schema when needed."""
    inspector = inspect(engine)
    if "bugs" in inspector.get_table_names():
        existing_columns = {column["name"] for column in inspector.get_columns("bugs")}
        required_columns = {"title", "ai_analysis", "created_at"}
        if not required_columns.issubset(existing_columns):
            with engine.begin() as connection:
                connection.execute(text("DROP TABLE bugs"))

    Base.metadata.create_all(bind=engine)
