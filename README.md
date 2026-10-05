# Dependency Constraint Lab

Offline teaching model combines explicit SemVer endpoints and explains which supplied invented candidates satisfy EVERY constraint. Tied inclusive flags combine by AND; build metadata remains visible without changing precedence. Custom profile `explicit-semver-bounds/1`, no registry/package solving or compatibility/security inference.

## Run without installation

Python3.11+ intended; verified Windows CPython3.13.7 only. No runtime dependencies, accounts, registry or network. From this directory:

```powershell
python -I lab.py examples/touch-open.input.json
python -I lab.py examples/build-equal.input.json --output fresh-report.json
python -I scripts/run_tests.py
python -I -O scripts/run_tests.py
python -I scripts/verify_project.py
```

The verifier requires Bandit already installed on this interpreter. It installs nothing and retains raw logs in fresh `.verification-work` directories. It executes owned tests, never candidate data. Existing, empty and missing-parent output destinations fail.

## Input and interpretation

```json
{"profile":"explicit-semver-bounds/1","synthetic":true,"scenarios":[{"id":"demo","constraints":[{"id":"range","lower":{"version":"1.0.0","inclusive":true},"upper":{"version":"2.0.0","inclusive":false}}],"candidates":[{"id":"v","version":"1.5.0"}]}]}
```

Endpoints may be null for no bound. IDs unique within respective namespaces; duplicate candidate versions preserve indices. All admitted prereleases participate; npm default matching and PEP440 differ. No caret/tilde/wildcard/OR/exclusions. Unknown profiles receive whole common admission; all supported grammar precedes all caps and modeling. A late malformed endpoint invalidates the whole report.

For `[1.0.0,2.0.0]` and `(2.0.0,3.0.0]`, candidate2.0.0 fails the second lower bound. Effective endpoints meet at an excluded value: equal_open, sufficient contradiction. Changing that lower flag to true permits it. Examples also include build ties, vacuous membership and a prerelease gap.

`bounds_contradiction` true only for inverted/equal-open bounds. False does not prove global nonemptiness: `(1.0.0-a,1.0.0-a.0)` is ordered but has no intervening precedence value. `supplied_set_empty` describes only supplied candidates. Package existence, availability, compatibility, security and existence of an unsupplied matching version stay unknown.

## Contract, architecture and security

[CONTRACT.md](CONTRACT.md) defines exact versioned JSON and validation order. Report retains original declarations, all strongest tied contributors, effective endpoints, per-constraint relations/pass bits and supplied matching indices. Compact sorted ASCII JSON+LF. Exit0 complete/help even when no candidates match;2 invalid/usage;3 unsupported;4 limit;5 I/O/delivery. Fresh exclusive output can leave partial bytes on failure; no atomicity or durability claim.

Pure `admission.py` bounds bytes/native trees; `version.py` strict SemVer; `bounds.py` endpoint reduction; `model.py` whole admission and conjunction. `cli.py` owned-file transport/checked delivery. API `evaluate`, `evaluate_bytes`, `serialize`. Core modules perform no I/O; presentation remains separate.

64KiB raw, depth8/nodes4096 (root0, supported deepest leaf6),16 scenarios,8 constraints/16 candidates each; globally64 constraints/128 candidates/256 version occurrences. Version256 ASCII chars, numeric32 digits,16 identifiers/group and64 chars/identifier. Aliases and keys count per occurrence. Exact builtin admission before hooks, immutable inputs.1MiB output cap is unreachable under current admitted shapes by a conservative436,992-byte bound; reduced-cap tests are seams. Trusted runtime/source/ordinary filesystem; no hard RSS/time, concurrent-mutation or hostile-path guarantee. See [SECURITY.md](SECURITY.md).

## Evidence and learning

- [Plan](PLAN.md), [Research](RESEARCH.md), [State](STATE.md).
- [Verification](VERIFICATION.md), [Review](REVIEW.md), [Decisions](DECISIONS.md), [Learning](LEARNING.md).
- [Draft review](research/worker-review.md): rejected local draft; unavailable verified-free remote readiness, zero remote inference.
- [Attribution](ATTRIBUTION.md): MIT original code and reviewed owned SemVer/helper reuse; licensed inert upstream research captures.

Codex assisted research, implementation, tests and implementing-agent self-review. Finite synthetic learning model, no independent audit/production certification. No publication, hosted checks, real packages or upstream execution claimed.

## Publication status

See [publication review](PUBLICATION.md) for the October 5 source snapshot, fresh local checks, evidence boundaries and current hosted-check distinction.
