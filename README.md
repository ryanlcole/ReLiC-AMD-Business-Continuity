# ReLiC Share — AMD Hackathon

**Hackathon project — AMD Developer Hackathon: ACT III**

## Name

**ReLiC = Remember · Exist · Live · Imagine · Create**

**ReLiC Share = Remember · Exist · Live · Imagine · Create · Share**

ReLiC is ReLiC and is never only a portion of the whole.

`REMEMBER -> EXIST -> LIVE -> IMAGINE -> CREATE -> SHARE -> REMEMBER`

**EI = Environmental Intelligence.**

This public repository is scoped to the hackathon. It contains the hackathon implementation, continuity records, governing canon, tests, synthetic business demonstration, AMD/vLLM connection boundary, and ReLiC Share proof surface. Private/non-hackathon ReLiC work is not part of this repository or proof surface.

## ReLiC lifecycle

- **REMEMBER** — preserve errors, corrections, canon, authority/law records, success, known-working references, backups, provenance, decisions, and why changes occurred.
- **EXIST** — remain a continual reference boundary: applicable ReLiC authority, provenance, time, errors, and context are resolved before dependent downstream action proceeds.
- **LIVE** — observe the current hackathon environment through authorized interfaces. Historical state remains historical rather than silently becoming current state.
- **IMAGINE** — permit hypotheses while keeping fiction/hypothesis distinguishable from known facts, evidence, tests, and results.
- **CREATE** — create a traceable report/context package retaining authority, provenance, uncertainty, errors, tests, and results.
- **SHARE** — expose the hackathon implementation and proof to AMD. Share is the public proof surface into ReLiC; it is not a replacement for ReLiC.

“Remember. Explain. Prove.” describes the Share proof experience, not the whole ReLiC lifecycle.

## Implemented repository content

### Deterministic business proof

`app/relic/engine.py` contains the deterministic refund-policy resolver. The synthetic policy corpus is under `data/demo-company/`. The resolver retains evidence identifiers in its result.

### Temporal continuity

`app/relic/temporal.py` contains valid-time/recorded-time structures, supersession handling, applicable-rate resolution, and reconciliation logic. Original work/payment records are not rewritten by the reconciliation function.

### RuneCore / continuity inventory

`app/relic/runecore.py` loads machine-readable authority, change history, working references, and neurons and returns a continuity inventory. Constructing an authority rune does not prove legal/canonical validity or applicability.

### API

`app/main.py` exposes the static demo plus `/status`, `/continuity`, `/evidence`, and `/decision`. The decision endpoint currently identifies its inference mode as `deterministic-local-reference`.

### AMD/vLLM boundary

`app/inference.py` contains configuration and an OpenAI-compatible `/chat/completions` call for an event AMD-hosted vLLM endpoint. The file explicitly states that endpoint configuration does not prove AMD backing; infrastructure verification is separate.

AMD-backed inference is not claimed as verified until an AMD endpoint is configured and independently verified.

### ReLiC continuity records

- `RELIC_CANON.md` — governing project canon.
- `ERRORS.md` — durable failure/correction ledger.
- `data/relic/authority.json` — machine-readable authority records.
- `data/relic/change_history.json` — material project change records.
- `data/relic/working_references.json` — known-working recovery/comparison reference.
- `data/relic/neurons.json` — plan/dependency organization; neurons do not legislate.
- `docs/index.html` — ReLiC Share public inspection surface.

## Errors retained

`ERRORS.md` currently retains three recorded failures/corrections: pytest import path failure in CI; static demo source existing before it was actually served; and Replit being unsuitable as the continuing no-surprise-cost host. They remain in the ledger after correction because errors are evidence.

## Known-working reference

`data/relic/working_references.json` records commit `43d5fc2fa4bfda0b5770e8fef382d751c0a21679` as a known-working Business Continuity MVP reference before authority-core construction. It explicitly does not claim AMD-backed inference, Evolus integration, general legal reasoning, or production deployment.

## Tests

Repository tests are under `tests/`: `tests/test_engine.py`, `tests/test_runecore.py`, and `tests/test_temporal.py`.

Run:

```bash
pytest -q
```

Test-file presence is not proof that the current commit passed CI. Verification status must be reported separately.

## Current proof boundaries

### Present in this repository

- complete hackathon ReLiC lifecycle canon
- deterministic business resolver
- synthetic policy evidence corpus
- temporal continuity code
- RuneCore continuity inventory
- governing canon
- authority/change/working-reference/neuron records
- durable error ledger
- API and static surfaces
- AMD/vLLM connection code
- tests
- ReLiC Share proof page

### Not claimed as currently verified

- AMD-backed inference execution
- AMD environmental/telemetry integration beyond the connection boundary present in code
- Evolus integration
- general legal reasoning
- production deployment
- current-commit CI success unless independently verified and recorded

## Hosting

The static ReLiC Share surface is in `docs/` for GitHub Pages. Runtime/API deployment remains separate from the static proof surface. No API keys belong in the static site or repository.

## Local run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## License

MIT. See `LICENSE`.