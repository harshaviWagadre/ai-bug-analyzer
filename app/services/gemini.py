import json
import os
import re
from typing import Any

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    model = None


def _fallback_analysis(reason: str) -> dict[str, Any]:
    return {
        "bug_summary": "Unable to determine confidently",
        "root_cause": "Unable to determine confidently",
        "severity": "Medium",
        "suggested_fix": "Please share more context or logs so the issue can be analyzed more accurately.",
        "explanation": reason,
        "confidence_score": "Low",
    }


def format_analysis_response(raw_text: str) -> dict[str, Any]:
    """Convert a raw Gemini response into a simple dictionary for the app."""
    if not raw_text:
        return _fallback_analysis("No analysis returned by the AI service.")

    stripped_text = raw_text.strip()

    try:
        parsed_json = json.loads(stripped_text)
        if isinstance(parsed_json, dict):
            return {
                "bug_summary": parsed_json.get("bug_summary")
                or parsed_json.get("summary")
                or "Unable to determine confidently",
                "root_cause": parsed_json.get("root_cause")
                or "Unable to determine confidently",
                "severity": parsed_json.get("severity") or "Medium",
                "suggested_fix": parsed_json.get("suggested_fix")
                or parsed_json.get("suggested_solution")
                or "Please review the code and logs carefully.",
                "explanation": parsed_json.get("explanation")
                or "No additional explanation was provided.",
                "confidence_score": parsed_json.get("confidence_score") or "Low",
            }
    except json.JSONDecodeError:
        pass

    bug_summary = re.search(r"Bug Summary:\s*(.+)", stripped_text, re.IGNORECASE)
    root_cause = re.search(r"Root Cause:\s*(.+)", stripped_text, re.IGNORECASE)
    severity = re.search(r"Severity:\s*(.+)", stripped_text, re.IGNORECASE)
    suggested_fix = re.search(r"Suggested Fix:\s*(.+)", stripped_text, re.IGNORECASE)
    explanation = re.search(r"Explanation:\s*(.+)", stripped_text, re.IGNORECASE)
    confidence = re.search(r"Confidence Score:\s*(.+)", stripped_text, re.IGNORECASE)

    return {
        "bug_summary": (
            bug_summary.group(1).strip()
            if bug_summary
            else "Unable to determine confidently"
        ),
        "root_cause": (
            root_cause.group(1).strip()
            if root_cause
            else "Unable to determine confidently"
        ),
        "severity": severity.group(1).strip() if severity else "Medium",
        "suggested_fix": (
            suggested_fix.group(1).strip()
            if suggested_fix
            else "Please review the logs and confirm the issue with more context."
        ),
        "explanation": (
            explanation.group(1).strip()
            if explanation
            else "No additional explanation was provided."
        ),
        "confidence_score": confidence.group(1).strip() if confidence else "Low",
    }


def analyze_bug(log_text: str) -> dict[str, Any]:
    """Send the uploaded bug text to Gemini and return a structured analysis."""
    if not log_text or not log_text.strip():
        return _fallback_analysis("No bug content was provided.")

    prompt = f"""
You are a careful debugging assistant.
Analyze the bug report below and return valid JSON only.

Required keys:
- bug_summary
- root_cause
- severity
- suggested_fix
- explanation
- confidence_score

Rules:
- If the report is too vague, say "Unable to determine confidently" instead of inventing facts.
- Keep the response short and practical.
- Return only valid JSON and no extra text.

Bug report:
{log_text}
"""

    if not model:
        return _fallback_analysis(
            "The Google Gemini API key is not configured, so a safe fallback response was returned."
        )

    try:
        response = model.generate_content(prompt)
        return format_analysis_response(response.text)
    except Exception as exc:  # pragma: no cover - defensive path
        return _fallback_analysis(
            f"The AI service could not complete the analysis: {exc}"
        )
