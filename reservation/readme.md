🪑 Temporary Seat Reservation System

(Backend Design Assignment — Junior SWE Level)

🧠 Context

You are building the backend for an event ticketing platform.
When a user selects a seat, the system should temporarily reserve that seat so no one else can take it while the user is completing payment.
If the user does not complete payment within a fixed time window, the seat should automatically become available again.
This is a core real-world backend problem used in interviews.

🎯 Goal
Design and implement a backend service that manages:
seat availability
temporary reservations
expiration of reservations
final confirmation of seats

🔑 Core Concepts You Must Handle

Time-based state transitions

Ownership (who reserved what)

Preventing double-reservations

Clear separation of validation vs mutation

Clean error handling

📦 Data Model (you design this)

You will likely need entities similar to:

Seat

Reservation

You must decide:

What fields exist

What states are possible

What timestamps are required

🧩 Functional Requirements
1️⃣ View Seat Status

Endpoint

GET /seats


Returns

List of seats with status:

available

reserved

booked

2️⃣ Reserve a Seat (Temporary)

Endpoint

POST /reserve


Input

{
  "user_id": "u123",
  "seat_id": "A10"
}


Rules

If seat is available → reserve it

If seat is already reserved or booked → reject

Reservation expires after 5 minutes

Each seat can have only one active reservation

3️⃣ Confirm Seat (Payment Success)

Endpoint

POST /confirm


Input

{
  "user_id": "u123",
  "seat_id": "A10"
}


Rules

Only the same user who reserved the seat can confirm it

Reservation must not be expired

On success:

Seat becomes booked

Reservation is invalidated

4️⃣ Auto-Expire Reservations

If reservation time exceeds 5 minutes:
Seat becomes available again
Reservation is removed or marked expired
Expiry should be checked at request time
No background cron required (for now)

⚠️ Edge Cases You MUST Handle

User tries to reserve an already reserved seat

User tries to confirm someone else’s reservation
User tries to confirm after reservation expired

Same user tries to reserve multiple seats

Reservation expires exactly at boundary time

Concurrent reserve requests (assume two requests arrive close together)

🧱 Architectural Constraints

Use Python

No real database (in-memory structures only)

Must separate:

validation logic

state mutation

API/service layer

No giant functions

No hardcoded hacks

🚫 What NOT to do

No “just delete and recreate”

No silent state changes

No mixing validation and mutation

No tutorial-style shortcuts

✅ Evaluation Criteria (how I’ll review it)

I will judge:

correctness of state transitions

clarity of data models

separation of responsibilities

quality of edge-case handling

whether this feels production-minded

🧠 Hint (only one)

If you find yourself writing:

if ...:
    if ...:
        if ...:


You are doing it wrong.

Your Instructions (important)

Design first (on paper or comments)

Define:

data models

valid states

transitions

Write code without asking for help

When done, paste:

models

core service functions

no FastAPI routes yet

Then say:

“Review my seat reservation system.”

I will review it strictly, like a real PR.

Take your time.
This one will make you noticeably better.