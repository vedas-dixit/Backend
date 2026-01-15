Idempotent Request Processing System
This project teaches:
idempotency
request deduplication
safe retries
state transitions
correctness under repeated calls
These are non-negotiable backend fundamentals.

🧠 High-Level Idea
Clients sometimes retry requests:
due to network failure
timeout
frontend bugs
user double-clicks

Your backend must:
Process the request exactly once — even if it is sent multiple times.

🟢 Phase 1 — Easy: Basic Idempotency
Problem Statement

You are building an API that processes actions (e.g., “create order”, “send email”, “apply discount”).

Each request includes a client-generated idempotency key.

API
POST /process-request

Input

{
"idempotency_key": "abc-123",
"payload": {
"action": "apply_discount",
"amount": 50
}
}

Rules
If idempotency_key is new:
Process the request
Store the result
Return success
If idempotency_key is already processed:
Do NOT process again
Return the same response as before

Concepts Introduced
Idempotency
Request identity
Safe retries
State-based logic

🟡 Phase 2 — Moderate: In-Progress State
Now reality hits.
New Requirement
Requests can take time.
Add a third state:
in_progress
completed
failed
New Rules
When a request starts → mark as in_progress

If same idempotency key arrives while in_progress:

Reject or return “processing”

If completed → return cached response

If failed → allow retry OR return error (your choice, but be consistent)
Concepts Introduced
State machines
Transitional states
Partial failure handling

🟠 Phase 3 — Moderate+: Time-Based Cleanup
Nothing should live forever.
New Requirement
Idempotency records expire after 24 hours
After expiry, same idempotency key can be reused

Constraints
No cron jobs
No background workers

Cleanup must happen naturally during request processing

Concepts Introduced

TTL logic

Lazy cleanup

Time-based invalidation

🔴 Phase 4 — Edge Cases 
Handle these scenarios explicitly:
Same idempotency key, different payload
Partial failure mid-processing
Client retries after timeout but server succeeded
Concurrent requests with same idempotency key
You don’t need infra-level locking — just correct logic.
