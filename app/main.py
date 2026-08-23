from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


from app.routers.analyze import router as analyze_router

app = FastAPI(title="AI Smart Bug Analyzer", description="Milestone 3", version="3.0")

# Templates Folder
templates = Jinja2Templates(directory="templates")

# Include Router
app.include_router(analyze_router)


# Home Page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request, name="dashboard.html", context={}
    )
