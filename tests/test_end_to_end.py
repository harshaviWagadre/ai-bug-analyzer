from app.agents.orchestrator import orchestrate

test_bugs = [
    {
        "title": "Login Crash",
        "description": "Application crashes during login. NullPointerException at LoginService.java:54",
    },
    {
        "title": "Payment Crash",
        "description": "Payment fails because database connection times out. DatabaseTimeoutException at PaymentService.java:120",
    },
    {
        "title": "Invalid Password",
        "description": "User cannot login with valid credentials. AuthenticationException at AuthService.java:45",
    },
    {
        "title": "Email Notification Failure",
        "description": "Verification email is not sent. SMTPException at EmailService.java:72",
    },
    {
        "title": "File Upload Failure",
        "description": "Image upload fails for files larger than 5MB. FileSizeLimitExceeded at UploadService.java:80",
    },
]


print("\n======================================")
print("MILESTONE 4.3 - END TO END TESTING")
print("======================================")


for i, bug in enumerate(test_bugs, start=1):

    print("\n--------------------------------------")
    print(f"TEST CASE {i}: {bug['title']}")
    print("--------------------------------------")

    try:
        result = orchestrate(bug["description"])

        print("RESULT:")
        print(result)

        print("STATUS: PASS")

    except Exception as e:
        print("STATUS: FAIL")
        print("ERROR TYPE:", type(e).__name__)
        print("ERROR:", repr(e))

        import traceback

        traceback.print_exc()
