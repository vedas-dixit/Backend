🧠 Problem Statement: OTP-Based Authentication Service (Mini Auth System)

You are asked to design and build a simple backend authentication service using Python.

This service allows users to request a one-time password (OTP) and verify it for login.

Think of this as a very small piece of a real production auth system.

🔧 Functional Requirements
1️⃣ Request OTP

Endpoint

POST /auth/request-otp


Input

{
  "email": "user@example.com"
}


Behavior

If the email is new:

Create a user record

Generate a 6-digit numeric OTP

Store OTP with creation time

If the email already exists:

Generate a new OTP

Each OTP should:

Expire after 5 minutes

Be usable only once

Limit OTP requests:

Max 3 OTP requests per email per hour

Simulate sending OTP (print to console)

2️⃣ Verify OTP

Endpoint

POST /auth/verify-otp


Input

{
  "email": "user@example.com",
  "otp": "123456"
}


Behavior

Validate:

User exists

OTP matches

OTP not expired

OTP not already used

If valid:

Mark OTP as used

Mark user as “authenticated”

Return success response

If invalid:

Return meaningful error

📦 Data Handling Rules

You must not use a real database.

Use:

In-memory storage (dict, dataclass, etc.)

But structure it as if it could later be replaced by a DB.

🏗️ Architecture Constraints

Your project must have:

Separate layers for:

API routes

Business logic

Data storage

Clear folder structure

No global spaghetti logic

Type hints everywhere

Clean function boundaries

Example (you don’t have to copy exactly):

app/
  main.py
  api/
  services/
  models/
  storage/

⚠️ Edge Cases You Must Handle

OTP expired

OTP reused

Too many OTP requests

Wrong OTP

Email never requested OTP

Concurrent requests (assume two requests hit quickly)

🎯 Evaluation Criteria (Big Tech Style)

You’ll be judged on:

Code readability

Logical correctness

Separation of concerns

Defensive programming

Clear error handling

Whether this feels production-ready, not hacky

❌ What NOT To Do

No hard-coded OTPs

No giant single file

No copying tutorials

No skipping edge cases

🧪 Bonus (Optional but Impressive)

Add:

GET /auth/status?email=user@example.com


Returns:

{
  "authenticated": true
}


Add basic unit tests

Add simple rate-limiter logic

🧠 Why This Problem Matters

This problem tests:

Backend thinking

API design

State management

Time-based logic

Real-world edge cases

This is exactly the kind of task a junior SWE would get in a take-home or pairing round.