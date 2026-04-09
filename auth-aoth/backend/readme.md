---

# Auth & OAuth — The 5-Phase Deep Dive

You already started. You have signup, login, JWT generation, and some TODOs.
Now turn it into something you'd actually trust in production.

The goal isn't to finish fast. It's to understand *why* every decision exists.

---

## PHASE 1 — Passwords & Tokens Done Right

You are here. Mostly.

What to learn: how bcrypt works, why you never store plaintext, what "work factor" means
What to implement:
- Hash passwords with bcrypt on signup, compare on login
- Access token (short-lived, ~15min) + Refresh token (long-lived, ~7 days)
- Store refresh tokens in the DB, tied to a user
- Logout = delete the refresh token from DB

What to think about:
- Why is the access token short? What happens if it leaks?
- What is the difference between stateless (JWT) and stateful (session) auth?
- What does "Bearer token" actually mean?

You're done when: a stolen access token expires quickly and logout actually works.

---

## PHASE 2 — Hardening Auth

What to learn: refresh token rotation, token families, timing attacks
What to implement:
- Refresh token rotation — every time you use a refresh token, issue a new one and invalidate the old one
- Detect refresh token reuse — if an already-used token is used again, invalidate the entire family (someone is stealing tokens)
- Rate limit login and signup endpoints specifically
- Constant-time password comparison (look up why naive string compare leaks timing info)

What to think about:
- What does "token family" mean and why does reuse detection matter?
- Where do you store refresh tokens — DB row, Redis, hashed?
- Should you hash refresh tokens in the DB the same way you hash passwords?

You're done when: a stolen refresh token can't be silently reused.

---

## PHASE 3 — Password Reset & Email Flows

What to learn: time-limited signed tokens, one-time-use flows
What to implement:
- Forgot password → generate a short-lived reset token (not a JWT, a random signed token)
- Token is single-use and expires in 15 minutes
- Email the link (you can fake the email for now, just log it)
- On use, invalidate token immediately, force re-login everywhere

What to think about:
- Why shouldn't a password reset token be a JWT?
- What happens if the user clicks the reset link twice?
- What does "invalidate all sessions" mean in practice?

You're done when: the reset flow can't be replayed and tokens expire.

---

## PHASE 4 — Understanding OAuth 2.0

Stop coding for a moment. Just understand the protocol first — then build.

What to learn:
- What problem OAuth solves (delegated access, "Login with Google")
- The four OAuth 2.0 grant types — Authorization Code, Client Credentials, Device Flow, Implicit (and why Implicit is dead)
- What an Authorization Server, Resource Server, and Client actually are
- What scopes mean and how they limit access
- PKCE — why it exists, what it prevents (code interception attacks)

What to implement:
- Authorization Code flow with PKCE — your own tiny OAuth server
  - GET /authorize → redirects with a code
  - POST /token → exchanges code for access token
  - POST /token (refresh) → exchanges refresh token for new access token
- A simple protected resource server that validates the token

What to think about:
- Why does the authorization code exist? Why not just return the token directly?
- What is the redirect_uri and why must it match exactly?
- What does a client_id and client_secret represent?
- What is the difference between OAuth (authorization) and authentication?

You're done when: you can explain every step of the Authorization Code + PKCE flow without looking it up.

---

## PHASE 5 — OpenID Connect & Production Patterns

What to learn: OIDC is OAuth + identity, what an ID token is vs access token, JWKS
What to implement:
- Add an ID token (JWT with user claims — sub, email, name) on top of your OAuth server
- Expose a /.well-known/openid-configuration discovery endpoint
- Expose a /jwks.json endpoint so clients can verify your tokens without calling you
- Implement token introspection endpoint (POST /introspect — "is this token still valid?")
- Implement token revocation endpoint (POST /revoke)

What to think about:
- Why do access tokens and ID tokens have different audiences?
- What is the difference between RS256 (asymmetric) and HS256 (symmetric) JWT signing? Which should a real auth server use and why?
- What does a downstream service do when it needs to verify your token without calling you on every request?

You're done when: your auth server looks structurally similar to how Auth0, Okta, or Cognito work under the hood.

---

## The Questions That Should Follow You Through All 5 Phases

- What happens if the DB is down at the moment of login?
- What happens if two login requests arrive at the same time for the same account?
- What does a token look like to an attacker who intercepts network traffic?
- If someone gets read access to your DB, what can they do?
- Which of your tokens can be revoked instantly, and which can't?