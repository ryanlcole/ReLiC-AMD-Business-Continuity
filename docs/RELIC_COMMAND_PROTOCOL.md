# ReLiC Command Protocol

Status: FINALIZED for current ChatGPT/ReLiC continuity behavior.

This protocol defines user-facing `@ReLiC` commands. Commands are case-insensitive. The token immediately following `@ReLiC` is the command; remaining text is its argument.

ReLiC remains observer-first. A command never grants a capability that is not exposed in the current chat, never converts read-only access into write access, and never permits false claims of persistence, deployment, AWS/GitHub/Drive mutation, or canon authority.

## Fresh-chat bootstrap

### `@ReLiC relic`
Primary fresh-chat bootstrap alias. Treat exactly as `@ReLiC Continue`.

### `@ReLiC Continue`
Signals that a new ChatGPT session has begun and requests continuation of the active project from the last verified implementation state.

Required continuation procedure:
1. Retrieve focused MCP ReLiC continuity for the active/recent project and governing execution contract.
2. If needed, run exact-term ReLiC search.
3. Reconcile available MCP ReLiC, legacy/old ReLiC continuity, authoritative project records, newest neuron/current-state pointers, and current repository state.
4. Identify active project, active milestone/contract, last verified implementation/deployment, blockers, and next allowed action.
5. Re-inspect current repository state before implementation-sensitive work.
6. Enforce the governing execution contract before AWS/GitHub mutation.
7. Continue only through already-authorized plan work or repairs; do not duplicate existing implementations.

For Sourcerors through Christmas 2026 beta completion, the finalized beta milestone contract governs AWS/GitHub work. New product-direction ideas are discussion/post-beta only unless explicitly amended by the user; unrelated side projects are exempt. Update the existing final product in place.

## Recording controls

- `@ReLiC Save` — audit the current conversation for continuity-significant decisions, amendments, implementation evidence, tests, commits/PRs/deployments, superseded ideas, blockers, unresolved work, provenance, and drift; persist only through an actually exposed dedicated ReLiC writer. Report any persistence gap.
- `@ReLiC Load` — audit ChatGPT's present understanding against ReLiC evidence, current project records, newest current-state pointers, and current repository implementation truth; correct stale/conflicting context before continuing.
- `@ReLiC Quit` — stop automatic ReLiC continuity observation/recording semantics for the rest of the chat unless ReLiC is explicitly invoked again.
- `@ReLiC Pause` — pause continuity recording/ingestion semantics from this point; paused material is not retroactively ingested unless explicitly requested.
- `@ReLiC Resume` — resume continuity observation/recording semantics from this point forward.

## Inspection and operations

- `@ReLiC Help` — list recognized commands and one-line meanings.
- `@ReLiC Checkup` — health audit for MCP ReLiC, legacy ReLiC where exposed, project identity, execution-contract drift, repository/branches/PR/deploy state, AWS/server status, Drive continuity artifacts, storage/resources, stale/duplicate modules, alerts, and blockers. Report PASS/FAIL/UNKNOWN.
- `@ReLiC Smile` — ecosystem-wide inventory of known currently running programs/projects with links, repositories, deployments/servers, storage/resources, alerts, continuity state, and blockers. Save to Google Drive as `YYYY-MM-DD_smile.bat` only when Drive write capability is actually exposed. The `.bat` is report data, not executable automation unless separately requested.
- `@ReLiC Wink` — same inventory as Smile but scoped only to the active project and returned to ChatGPT; no Smile `.bat` is created.
- `@ReLiC Status` — compact active project, milestone/contract, implementation/deploy state, ReLiC connectivity/persistence state, blocker, and next step.
- `@ReLiC Milestone` — report active milestone, target, satisfied exit criteria, remaining build work, blockers, and exact next user-required action without changing scope.
- `@ReLiC Drift` — compare current implementation/deployments/continuity/current ChatGPT understanding against the governing execution contract and report divergences, duplicates, stale paths, and unauthorized scope changes.
- `@ReLiC Guard <proposal>` — classify a proposed action as exactly one of: `IN PLAN`, `REPAIR`, `POST-BETA IDEA`, `UNRELATED SIDE PROJECT`, `REQUIRES AMENDMENT`.
- `@ReLiC Trace <thing>` — reconstruct provenance from intent/decision through ReLiC/authoritative record, commit/PR, test, deploy, and verified behavior; missing links remain UNKNOWN.
- `@ReLiC Verify <claim>` — return VERIFIED, CONTRADICTED, or UNKNOWN against the highest-authority evidence available.
- `@ReLiC Test` — run every applicable available automated/health/contract check for the current milestone and summarize PASS/FAIL/UNKNOWN without expanding scope.
- `@ReLiC Handoff` — produce the minimum complete continuation packet for another ChatGPT session/agent: project, governing contract, current implementation/deploy, authoritative pointers, active milestone, blockers, next allowed action, and provenance. Never include secrets.

## Planning and scope

- `@ReLiC Next` — determine and execute the next allowed step under the governing execution contract until a user-required milestone action, genuine blocker, or capability boundary is reached.
- `@ReLiC Idea <idea>` — treat the supplied idea as discussion/post-beta under the locked beta contract unless already in-plan or clearly an unrelated side project. Do not mutate AWS/GitHub from `Idea` alone.
- `@ReLiC Amend <change>` — explicit user request to amend a locked execution contract. Preserve old and new states as lineage; record the amendment in an authoritative project record before using the new scope for AWS/GitHub work when possible.

## Core continuity laws

- Identity != Representation.
- Representation != Truth.
- UNKNOWN != FACT.
- MEMORY != CANON.
- Observation != Canon.
- Temporal association != causation.
- Storage/retrieval/compression/translation/summarization does not promote evidence to canon.
- Current inspected repository state governs current software implementation truth.
- Never claim a ReLiC write unless the dedicated writer returns a persistence receipt/event ID or other explicit confirmation.

## Capability failure behavior

If a command requests an unavailable capability, ReLiC performs all available read/audit work, identifies the exact missing capability, and does not pretend the requested write/check succeeded. In particular, if both legacy ReLiC and MCP ReLiC are not exposed, `Checkup` must identify which side could not be checked instead of claiming both are connected.
