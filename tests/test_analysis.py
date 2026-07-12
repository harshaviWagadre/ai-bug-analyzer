from app.services.gemini import format_analysis_response


def test_format_analysis_response_handles_text_output():
    raw_text = """Root Cause: Missing import\nSeverity: High\nSuggested Fix: Add the import\nConfidence Score: 92%\n"""

    result = format_analysis_response(raw_text)

    assert result["root_cause"] == "Missing import"
    assert result["severity"] == "High"
    assert result["suggested_fix"] == "Add the import"
    assert result["confidence_score"] == "92%"
