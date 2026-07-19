from fastapi import FastAPI

from app.database import Base, engine

from app.models import BugReport

from app.routers.bug import router

Base.metadata.create_all(bind=engine)


app = FastAPI(title="AI Smart Bug Analyzer")


app.include_router(router)
