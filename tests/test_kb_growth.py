from app.rag.kb_growth import add_resolved_bug

new_bug = {
    "title": "Payment Crash",
    "description": "Payment fails when database connection is lost.",
    "exception": "DatabaseConnectionError",
    "root_cause": "Database connection was unexpectedly closed.",
    "resolution": "Add database connection retry logic.",
}


result = add_resolved_bug(new_bug)


print("\n==============================")
print("KNOWLEDGE BASE GROWTH")
print("==============================")

print("\nNew bug added successfully!")

print("\nBug ID:", result["bug_id"])
print("Title:", result["title"])
print("Exception:", result["exception"])
print("Root Cause:", result["root_cause"])
print("Resolution:", result["resolution"])
