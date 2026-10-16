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

### AMD/TokenFactory boundary

`app/inference.py` contains configuration and an OpenAI-compatible `/chat/completions` call for the event AMD TokenFactory endpoint.

A single controlled sentinel call through `amd_chat` returned the requested sentinel `RELIC_AMD_TOKENFACTORY_PASS` from model `self-dploy/DeepSeek-V4-Flash`. Sanitized non-secret response metadata is preserved in `evidence/amd_tokenfactory_sentinel.json`.

This verifies AMD TokenFactory inference execution for the hackathon integration boundary. It does **not** establish direct MI300X execution, HIP/ROCm parity, or ReLiC ingestion of that observation. Those remain separate evidence gates.

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

Repository tests are under `tests/`, including the deterministic application tests and the RuneCore CPU reference test. The CPU test builds its prerequisite executable before executing the deterministic repeatability checks.

Run:

```bash
pytest -q
```

The CI run associated with the CPU prerequisite correction completed successfully: tests passed and the application imported successfully. CI status is commit-specific; later commits must be verified independently.

## Current proof boundaries

### Present and verified where stated

- complete hackathon ReLiC lifecycle canon
- deterministic business resolver
- synthetic policy evidence corpus
- temporal continuity code
- RuneCore continuity inventory
- governing canon
- authority/change/working-reference/neuron records
- durable error ledger
- API and static surfaces
- AMD TokenFactory connection code
- successful controlled TokenFactory sentinel execution with sanitized evidence
- deterministic RuneCore CPU reference test integrated into CI
- ReLiC Share proof page

### Not claimed as currently verified

- direct MI300X execution
- HIP/ROCm CPU↔GPU numerical parity
- AMD environmental/telemetry integration beyond the TokenFactory inference boundary
- ReLiC ingestion/canonization of the TokenFactory observation
- Evolus integration
- general legal reasoning
- production deployment

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