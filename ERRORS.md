# ERRORS — Durable Failure & Correction Ledger

Errors are retained as evidence. Do not erase an entry merely because the problem is fixed. Add the correction, verification, and relevant commit/reference.

Every error record must preserve temporal continuity. Record both **when the event actually occurred** (`occurred_at`) and **when ReLiC Share learned/recorded it** (`recorded_at`). If either is unknown, write `UNKNOWN`; never substitute the current timestamp for an unknown historical time. Corrections may be backdated in valid time, but their later recorded time must remain visible.

## ERR-2026-10-09-001 — Test import path failed in CI

- **Observed:** GitHub CI could not resolve the Python `app` package during pytest collection.
- **Impact:** The build could not be truthfully described as verified.
- **Cause:** The repository root was not explicitly established for pytest imports in CI.
- **Correction:** Added `pytest.ini` with `pythonpath = .` and `testpaths = tests`.
- **Verification:** Subsequent CI completed successfully before the hackathon MVP was merged to `main`.
- **Lesson:** Local/source presence is not proof of executable repository state. CI verification is a separate evidence object.

## ERR-2026-10-09-002 — Static demo existed before it was actually served

- **Observed:** `app/static/index.html` existed, but the FastAPI application initially did not route a browser request to it.
- **Impact:** The existence of UI source was temporarily mistaken for a usable UI.
- **Correction:** FastAPI was changed to serve the demo and the static GitHub Pages reference demo was added separately.
- **Lesson:** Representation/source presence is not runtime reachability.

## ERR-2026-10-09-003 — Replit was an unsuitable continuity host

- **Observed:** A Replit app could be created through the connected integration, but publication was blocked by the account's Autoscale deployment limit and the user had no Replit credits intended for this work.
- **Impact:** Replit could not be relied upon as the project's continuing no-surprise-cost host.
- **Correction:** Treat Replit as non-authoritative/optional tooling and keep the project source in GitHub. Prefer a static zero-runtime-cost reference surface for the deterministic demo; keep runtime deployment separate from source truth.
- **Lesson:** A tool accepting a build operation does not prove sustainable deployment, cost suitability, or ownership expectations. Hosting choice is part of project continuity evidence.

## Entry template

```text
## ERR-YYYY-MM-DD-NNN — Short title
- occurred_at: ISO-8601 timestamp/date or UNKNOWN
- recorded_at: ISO-8601 timestamp/date
- discovered_at: ISO-8601 timestamp/date or UNKNOWN
- Observed:
- Impact:
- Cause: UNKNOWN until supported by evidence
- Correction:
- correction_effective_from: ISO-8601 timestamp/date or N/A
- Verification:
- Related authority/decision:
- Known-working reference:
- Lesson:
```
