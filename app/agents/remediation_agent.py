def remediation_agent(bug, duplicate_bug):

    best_match = duplicate_bug[0]

    return {
        "recommended_fix": best_match["resolution_summary"],
        "reason": best_match["resolution_summary"],
    }
