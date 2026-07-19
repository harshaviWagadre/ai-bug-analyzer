import re


def log_analysis_agent(log_text: str):

    # Find common exception types
    exception_match = re.search(
        r"([A-Za-z_][A-Za-z0-9_]*(?:Exception|Error))", log_text
    )

    exception_type = exception_match.group(1) if exception_match else "Unknown"

    # Find file and line number
    failure_match = re.search(
        r"([A-Za-z0-9_./\\-]+\.(?:py|java|js|ts|cpp|c):\d+)", log_text
    )

    failure_point = failure_match.group(1) if failure_match else "Unknown"

    # Try to identify the affected code path
    code_path_match = re.search(r"(?:at\s+|in\s+)([A-Za-z0-9_.]+)", log_text)

    affected_code_path = code_path_match.group(1) if code_path_match else "Unknown"

    return {
        "exception_type": exception_type,
        "failure_point": failure_point,
        "affected_code_path": affected_code_path,
        "summary": create_summary(exception_type, failure_point, affected_code_path),
    }


def create_summary(exception_type, failure_point, affected_code_path):

    return (
        f"{exception_type} occurred at {failure_point} " f"within {affected_code_path}."
    )
