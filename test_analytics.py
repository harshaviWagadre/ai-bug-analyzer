from app.analytics.defect_analytics import generate_analytics

result = generate_analytics()


print("\n==============================")
print("DEFECT PATTERN ANALYTICS")
print("==============================")


print("\nTotal Bugs:")
print(result["total_bugs"])


print("\nSeverity Distribution:")

for severity, count in result["severity"].items():
    print(severity, ":", count)


print("\nAffected Components:")

for component, count in result["components"].items():
    print(component, ":", count)


print("\nException Frequency:")

for exception, count in result["exceptions"].items():
    print(exception, ":", count)


print("\nRoot Cause Frequency:")

for cause, count in result["root_causes"].items():
    print(cause, ":", count)
