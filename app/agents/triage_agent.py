import json

from app.services.gemini import analyze_bug


def triage_agent(bug_description: str):

    prompt = f"""
You are an AI Software Bug Triage Agent.

Analyze this bug report:

{bug_description}

Return ONLY valid JSON:

{{
    "severity": "High",
    "priority": "P1",
    "component": "Authentication",
    "confidence": 95,
    "reasoning": "Explain why you selected these values."
}}
"""

    result = analyze_bug(prompt)

    # Convert JSON string into Python dictionary
    try:
        return json.loads(result)

    except json.JSONDecodeError:

        return {
            "severity": "Unknown",
            "priority": "Unknown",
            "component": "Unknown",
            "confidence": 0,
            "reasoning": result,
        }
