def remediation_agent(root_cause, duplicate_bug):

    if duplicate_bug:
        best_match = duplicate_bug[0]
        fix = best_match.get("resolution_summary", "No recommendation available.")
    else:
        fix = "No recommendation available."

    return {
        "recommended_fix": fix,
        "reason": root_cause.get("root_cause_hypothesis", "Unknown root cause"),
    }
