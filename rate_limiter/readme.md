🅰️ Project: API Rate Limiter (Per-User + Per-IP)
📌 High-level Goal

Build a backend service that limits how frequently clients can call APIs, based on:

User identity (if logged in)

IP address (if anonymous or as a fallback)

The system must be:

Correct

Predictable

Hard to bypass

Extendable

🟢 Phase 1 — Easy: Fixed Window Rate Limiting
Problem Statement

You are building an API that should prevent abuse.

Each client is allowed:

5 requests per minute

A client is identified by:

user_id (if present)

otherwise ip_address

Required API
POST /check-rate-limit

Input

{
  "user_id": "user_123",   // optional
  "ip_address": "1.2.3.4"
}


Output

{
  "allowed": true | false,
  "remaining": number,
  "reset_at": "timestamp"
}

Rules
Use fixed time windows (e.g., per minute)
Track request count per client
If limit exceeded → deny
Reset counter when window expires



🟡 Phase 2 — Moderate: Per-User + Per-IP Rules

Now business adds nuance.

New Rules

If user_id exists:

Rate limit applies per user

If no user_id:

Rate limit applies per IP

If both exist:

Apply stricter of the two

Example:

User limit: 10/min

IP limit: 5/min
→ effective limit = 5/min

New Requirements

Track both dimensions

Decide precedence correctly

Do not double-count requests

Concepts Introduced

Multi-key rate limiting

Precedence rules

Composite identity

🟠 Phase 3 — Moderate+: Sliding Window

Fixed windows cause bursts.
Now you must fix that.

New Requirement

Replace fixed window with sliding window logic.

Meaning:

Requests are counted over the last 60 seconds

Window moves with time

Constraints

No background cleanup jobs

No cron

Old requests must naturally expire

Concepts Introduced

Sliding window algorithm

Time-series thinking

Memory management

🔴 Phase 4 — Advanced: Concurrency & Safety

Your API is now popular.

New Problems

Multiple requests can hit the limiter at the same time

Race conditions may allow extra requests

New Requirements

Ensure correctness under concurrent access

Prevent double increments

Avoid over-blocking

(You can assume single-process for now, but concurrent requests exist.)

Concepts Introduced

Atomicity

Critical sections

Locking (conceptual, not infra-heavy)

🟣 Phase 5 — Advanced+: Abuse Protection & Design Thinking

Now think like a production engineer.

New Requirements

Add temporary blocking

If limit exceeded 3 times → block for 5 minutes

Blocking must expire automatically

Rate limiter must explain why request is blocked

Response Example
{
  "allowed": false,
  "reason": "rate_limit_exceeded",
  "blocked_until": "timestamp"
}

Concepts Introduced

Escalation logic

Penalty windows

Clear error semantics

🚫 Explicit Constraints (Very Important)

You must NOT use:

Redis

External rate-limit libraries

Middleware magic

Cron jobs

Background workers

Use:

In-memory structures

Clear logic

Explicit timestamps

🧠 What This Project Trains

By the end, you’ll have practiced:

Time-based state

Idempotent thinking

Concurrency reasoning

Abuse prevention

Clean API contracts

This is core backend engineering.