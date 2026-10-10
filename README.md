# ReLiC — AMD Hackathon

**Hackathon project — AMD Developer Hackathon: ACT III**

ReLiC is ReLiC and is never only a portion of the whole.

`REMEMBER -> EXIST -> LIVE -> IMAGINE -> CREATE -> SHARE -> REMEMBER`

**EI = Environmental Intelligence.**

This repository contains the hackathon implementation, continuity records, governing canon, tests, business demonstration, AMD/vLLM connection boundary, and ReLiC Share proof surface.

## ReLiC lifecycle

- **REMEMBER** — errors, corrections, canon, authority/law records, success, known-working references, backups, provenance, decisions, and why changes occurred.
- **EXIST** — continual reference boundary: applicable ReLiC authority, provenance, time, errors, and context are resolved before dependent downstream action proceeds.
- **LIVE** — current environmental observation. Hardware/performance monitoring requires authorized telemetry; AMD hardware-health monitoring is not claimed as currently connected.
- **IMAGINE** — hypotheses/fiction remain distinguishable from known facts, evidence, tests, and results.
- **CREATE** — traceable report/context package retaining authority, provenance, uncertainty, errors, tests, and results.
- **SHARE** — inspection surface for AMD. Share exposes ReLiC; Share is not ReLiC itself.

“Remember. Explain. Prove.” describes the Share proof experience, not the whole ReLiC lifecycle.

## Implemented repository content

### Deterministic business proof

`app/relic/engine.py` contains the deterministic refund-policy resolver. The synthetic policy corpus is under `data/demo-company/`. The resolver retains evidence identifiers in its result.

### Temporal continuity

`app/relic/temporal.py` contains valid-time/recorded-time structures and reconciliation logic. Original work/payment records are not rewritten by the reconciliation function.

### RuneCore / continuity inventory

`app/relic/runecore.py` loads machine-readable authority, change history, working references, and neurons and returns a continuity inventory. Constructing an authority rune does not prove legal/canonical validity or applicability.

### API

`app/main.py` exposes the static demo plus `/status`, `/continuity`, `/evidence`, and `/decision`. The decision endpoint currently identifies its inference mode as `deterministic-local-reference`.

### AMD/vLLM boundary

`app/inference.py` contains configuration and an OpenAI-compatible `/chat/completions` call for an event AMD-hosted vLLM endpoint. The file explicitly states that endpoint configuration does not prove AMD backing; infrastructure verification is separate.

AMD-backed inference is not claimed as verified in this repository until an AMD endpoint is configured and independently verified.

### ReLiC continuity records

- `RELIC_CANON.md` — governing project canon.
- `ERRORS.md` — durable failure/correction ledger.
- `data/relic/authority.json` — machine-readable authority records.
- `data/relic/change_history.json` — material project change records.
- `data/relic/working_references.json` — known-working recovery/comparison reference.
- `data/relic/neurons.json` — plan/dependency organization; neurons do not legislate.
- `docs/RELIC_OS_EI_CANON.md` — historical OS/EFI Environmental Intelligence continuity record with explicit proof-status boundaries.
- `docs/index.html` — ReLiC Share public inspection surface.

## Historical OS / EFI record

`docs/RELIC_OS_EI_CANON.md` preserves the historical ReLiC OS/EFI architecture and named EFI components as a **historical proof record**. Their names in that record do not claim their binaries/source have been copied into this repository or that EFI deployment is current.

## Errors retained

`ERRORS.md` currently retains three recorded failures/corrections:

1. pytest import path failure in CI.
2. static demo source existed before it was actually served.
3. Replit was unsuitable as the continuing no-surprise-cost host.

They remain in the ledger after correction because errors are evidence.

## Known-working reference

`data/relic/working_references.json` records commit `43d5fc2fa4bfda0b5770e8fef382d751c0a21679` as a known-working Business Continuity MVP reference before authority-core construction. It explicitly does not claim AMD-backed inference, Evolus integration, general legal reasoning, or production deployment.

## Tests

Repository tests are under `tests/`:

- `tests/test_engine.py`
- `tests/test_runecore.py`
- `tests/test_temporal.py`

Run:

```bash
pytest -q
```

## Current proof boundaries

### Present in this repository

- deterministic business resolver
- temporal continuity code
- RuneCore continuity inventory
- governing canon
- authority/change/working-reference/neuron records
- durable error ledger
- API and static surfaces
- AMD/vLLM connection code
- tests
- historical OS/EI continuity record

### Not claimed as currently verified

- AMD-backed inference execution
- AMD hardware-health telemetry
- silicon-level error prevention
- processor tuning results
- current EFI deployment
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