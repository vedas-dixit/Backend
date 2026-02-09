🟢 Phase 1 — Basic Pagination (Foundations)
Goal

Return large datasets in small, predictable chunks.

Requirements

Expose an endpoint:

GET /items

Support query parameters:
page (1-based)
limit (max items per page)

Rules

Default page = 1

Default limit = 10

Enforce limit ≤ 50
Return:

current page data

total number of items
total pages

Response Shape (example)
{
  "page": 2,
  "limit": 10,
  "total_items": 123,
  "total_pages": 13,
  "data": [...]
}

What This Phase Teaches

Offset-based pagination

Defensive input validation

UX expectations for paginated lists

🟡 Phase 2 — Filtering + Sorting (Real Usage Begins)
Goal

Allow clients to narrow down results without downloading everything.
New Requirements (Superset of Phase 1)
Add optional query parameters:
min_amount
max_amount
status (e.g. pending, completed, failed)
sort_by (e.g. created_at, amount)
order (asc or desc)

Rules
Filters must be composable
Invalid filters must return a clear validation error
Sorting must be deterministic
Pagination applies after filtering

Example Request
GET /items?status=completed&min_amount=500&sort_by=created_at&order=desc&page=1&limit=20

What This Phase Teaches

Query composition

Filter ordering vs pagination ordering

API contract discipline

🟠 Phase 3 — Consistency & Edge Cases (Backend Maturity)
Goal

Prevent inconsistent pagination results when data changes.

New Requirements (Superset of Phase 2)
Results must be stable across pagination
If new items are added while the client is paginating:
already-seen items must not reappear
items must not disappear mid-pagination

Rules
Pagination must be based on a stable sort key
Reject pagination without a deterministic sort
Document the consistency guarantee clearly

Example Scenario
Client fetches page 1
New item inserted
Client fetches page 2
→ no duplicates, no skips

What This Phase Teaches

Why naïve offset pagination breaks

Snapshot thinking

Consistency vs freshness tradeoffs

🔴 Phase 4 — Professional-Level API (Production Grade)
Goal

Design pagination that scales, performs, and never lies.

New Requirements (Superset of Phase 3)

Introduce cursor-based pagination

Offset pagination still works (backward compatibility)

Cursor must:
be opaque
encode position safely
expire safely if invalid
New Query Parameters
cursor (optional)
limit

New Response Fields
{
  "data": [...],
  "next_cursor": "eyJjcmVhdGVkX2F0IjoiMjAyNi0wMS0xNSIsImlkIjoxMjM0fQ==",
  "has_more": true
}

Rules
Cursor pagination must:
outperform offset pagination on large datasets
remain consistent under concurrent writes
Filtering + sorting must still work
Clear error when cursor is invalid or expired
What This Phase Teaches
Industry-standard pagination (Stripe, GitHub, Twitter)
API evolution without breaking clients
Performance-aware backend design