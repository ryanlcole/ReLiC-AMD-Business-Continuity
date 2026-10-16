# ReLiC AMD Hackathon — Proof of Work

Status labels in this ledger are evidence labels, not canonization.

## Proof ladder

| Gate | Claim | Status | Evidence | Boundary |
|---|---|---|---|---|
| P0 | Repository/application continuity scaffold exists | PASS | Existing application, ReLiC continuity records, tests, and Share surface | Does not prove AMD execution |
| P1 | Deterministic RuneCore CPU reference executes reproducibly in CI | PASS | `tests/test_cpu.py`; successful GitHub Actions test job after CPU prerequisite correction | CPU only; normalized experimental model |
| P2 | AMD TokenFactory endpoint can be called through the repository adapter | PASS | `app/inference.py`; `evidence/amd_tokenfactory_sentinel.json` | TokenFactory inference only |
| P3 | Requested sentinel survives AMD inference round trip | PASS | Request/response sentinel `RELIC_AMD_TOKENFACTORY_PASS`; sanitized response metadata | Execution evidence; not ReLiC-ingested canon |
| P4 | AMD inference performs a useful judge-visible ReLiC task | PENDING | Future demo artifact/run | Must preserve deterministic evidence separately from model interpretation |
| P5 | Direct MI300X/ROCm execution | UNTESTED | None yet | Developer Cloud credit/access issue pending; not required for TokenFactory proof |
| P6 | CPU↔HIP numerical parity | UNTESTED | None yet | Do not infer from TokenFactory execution |

## P1 — CPU deterministic reference

The CPU reference is a deterministic C++ experimental state model. The repository test builds `bin/runecore_cpu`, executes the same seeded case repeatedly, checks finite state fields and observation status, and requires byte-identical state CSV output for the repeated run.

The CI failure introduced during package import was traced to the executable prerequisite not being built before `tests/test_cpu.py` executed. The test now builds that prerequisite. The associated CI test job completed successfully, including `pytest` and application import.

This proves the tested CPU behavior at that commit. It does not prove physical-world fidelity, GPU parity, or historical WaveCore identity.

## P2/P3 — AMD TokenFactory execution

Repository adapter: `app/inference.py` → `${AMD_VLLM_BASE_URL}/chat/completions` using bearer authentication supplied only through the execution environment.

Controlled sentinel request:

```text
RELIC_AMD_TOKENFACTORY_PASS
```

Observed response content:

```text
RELIC_AMD_TOKENFACTORY_PASS
```

Observed model identifier:

```text
self-dploy/DeepSeek-V4-Flash
```

Observed usage preserved from the non-secret response metadata:

- prompt tokens: 17
- completion tokens: 11
- total tokens: 28
- reasoning tokens: 0
- reported cost: 0.00000546

The API key is intentionally absent from repository evidence. The captured metadata tail available during the run was truncated; missing fields are not reconstructed.

Sanitized machine-readable evidence is stored at `evidence/amd_tokenfactory_sentinel.json`.

### Claim permitted by this evidence

> The repository's AMD adapter successfully executed a controlled inference request against the configured AMD TokenFactory endpoint and returned the requested sentinel.

### Claims not permitted by this evidence

- direct MI300X execution
- HIP or ROCm execution
- CPU↔GPU numerical parity
- physical ternary processor behavior
- ReLiC canonization/ingestion of the observation
- environmental or carbon reduction

## P4 — next proof

The next proof must demonstrate useful work rather than another connectivity sentinel.

The intended structure is:

1. deterministic ReLiC evidence establishes the bounded case and provenance;
2. AMD TokenFactory receives only the bounded representation needed for the task;
3. AMD output is captured as model output, not silently promoted to fact/canon;
4. deterministic validation compares the output against the known evidence boundary;
5. the judge-facing demo shows input → AMD execution → validation → provenance.

No additional AMD call should be made merely to repeat P2/P3. The next call should create P4 evidence.

## Evidence discipline

- Identity ≠ Representation.
- Representation ≠ Truth.
- UNKNOWN ≠ FACT.
- MEMORY ≠ CANON.
- Observation ≠ Canon.
- Temporal association ≠ causation.
- Preserve contradictions and failures rather than silently rewriting them.
- Never commit API keys, bearer tokens, SSH private keys, or other secrets.
