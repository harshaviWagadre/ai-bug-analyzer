# AI Bug Analyzer

AI Bug Analyzer is a beginner-friendly FastAPI project that lets a user submit a bug report, upload a log or text file, and receive an AI-generated analysis using Gemini.

## Features

- Upload a bug description or a file such as `.txt`, `.log`, or `.md`
- Send the content to Gemini for analysis
- Receive a simple bug analysis with:
  - bug summary
  - root cause
  - severity
  - suggested fix
  - explanation
  - confidence score
- Save bug reports in a SQLite database
- Explore saved bugs through simple API endpoints

## Project Structure

- `app/main.py` – creates the FastAPI app
- `app/database.py` – database connection and table setup
- `app/models.py` – SQLAlchemy model for bugs
- `app/routers/bug.py` – API routes for analysis and bug storage
- `app/services/gemini.py` – Gemini-based AI analysis logic
- `app/schemas.py` – request/response models
- `uploads/` – uploaded files are stored here

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Gemini API
- Pydantic

## Installation

### 1. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your environment variable

Create a `.env` file in the project root with:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

## Run the Project

```bash
python run.py
```

Then open:

- http://127.0.0.1:8000/

## API Endpoints

### POST /analyze

Submit a bug title, description, and optional file.

Example request:

```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
  -F "title=Database error" \
  -F "description=The app crashes when saving a user" \
  -F "bug_file=@/path/to/error.log"
```

Example response:

```json
{
  "message": "Bug Submitted Successfully",
  "bug_id": 1,
  "title": "Database error",
  "filename": "error.log",
  "ai_analysis": {
    "bug_summary": "The app crashes during save operations",
    "root_cause": "A database connection issue",
    "severity": "High",
    "suggested_fix": "Validate the connection object before writing data",
    "explanation": "The uploaded logs suggest a connection failure",
    "confidence_score": "92%"
  }
}
```

### GET /bugs

Returns all stored bugs.

### GET /bugs/{id}

Returns one stored bug by ID.

## Future Improvements

- Add authentication
- Support more file types
- Improve AI prompt quality
- Add a simple frontend
- Add pagination for bug history
