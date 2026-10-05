# Dependency constraint lab — proposed plan

Tier3 portfolio teaching model. APPROVED local stages1�4 at05:24 in this existing chat under Jake's direct overnight delegation; approval addendum is frozen in CONTRACT.md. Authority: .private/coordination/2026-10-05/SUCCESSORS.md, October5 04:49 section. Sole writer/separate directory; cutoff October6 08:00 Eastern. No new repository/install/publication/spending or target requests. Accepted SemVer/inventory/binary and prior manual gates preserved.

## Problem and success

Show how inclusive/exclusive version bounds combine and how supplied candidates match their conjunction. Precedence-equivalent endpoint spellings—including differing build metadata—must combine flags correctly without becoming literal identity. Explain every membership decision using original declaration provenance. Distinguish boundary contradiction, no supplied matches, and unknown unsupplied/package satisfiability.

Success: one frozen custom explicit-bound profile, whole admission before results, independent complete reports before code, exact finite candidate conjunction and effective bounds, immutable inputs, meaningful normal/O/actual CLI/mutation/SAST/ECC checks, current receipts and useful docs/license/AI/learning/vault. No package resolver or proof of compatibility/security/availability.

## Chosen scope and alternatives

Enabled `explicit-semver-bounds/1`. Strict bounded SemVer2.0.0 syntax/precedence reused from accepted owned helper. ALL syntactically valid prereleases participate; build ignored for membership/order but retained literally. This is explicit lab policy, not npm default matching, PEP440, or full SemVer package/API validation.

Compare explicit bounds against npm node-semver ecosystem parsing (research in RESEARCH.md). Recommend original explicit bounds plus supplied-candidate intersection. npm/packaging adoption is appropriate only for their ecosystem semantics, would require larger parsing/policy scope and review. No caret/tilde/wildcards/OR/exclusions, PEP440 conversion, union/complement/subset solver, registry querying, candidate generation/enumeration, packages/lockfile modification or dependency graph.

## Exact proposed input and bounds

Root exact fields profile (1..32 ASCII [A-Za-z0-9_./-]), synthetic (exact true), scenarios (list max16). Scenario exact id,constraints,candidates. Unique scenario id; exact lists constraints0..8 and candidates0..16. Global constraints<=64, candidates<=128, supplied version occurrences<=256 including every nonnull bound and candidate; count duplicates/aliases per occurrence.

Constraint exact id,lower,upper. Endpoint exact null OR {version:exact string,inclusive:exact bool}; null means no bound and has no flag/version. Duplicate constraint ids invalid within scenario. Candidate exact id,version; duplicate candidate ids invalid within scenario. Separate ID namespaces; duplicate version spellings or precedence classes allowed and preserved by index. Every id1..32 ASCII alphanumeric/underscore/hyphen.

Raw bytes<=65,536, native/tree depth<=8/nodes<=4,096, generic strings<=256 ASCII, numeric JSON token<=32 chars before decoding; no numeric input fields exist, so common structure rejects numbers. Exact bytes API, strictUTF8; predecode matched quote/container-depth gate, duplicate-key/nonfinite decoder checks. Native exact builtins admitted by identity BEFORE equality/hashing/iteration; dictionary keys count, repeated aliases count each occurrence, ancestor cycles reject, input not mutated. Reject floats/exotic types/metaclass/subclass hooks. Bound path copying only after key limits.

Version grammar/caps inherited: exactly3 canonical numeric components, core/numeric prerelease<=32 digits, prerelease/build<=16 identifiers each<=64 chars, whole version<=256 ASCII. Build numeric zeroes allowed; numeric prerelease leading zeroes invalid. Total generic/common bounds apply on unknown profiles; SemVer syntax/component caps apply only on supported profile.

Priority to freeze: exact bytes/raw/UTF8, predecode lexical/decoder, native preflight DFS, root/common scenario fields and per/global counts in input order, unsupported profile decision, ALL bound/candidate grammar across every scenario, ALL component caps, then derived bounds/membership. Supported version occurrence order: each scenario constraints in order lower then upper, then candidates in order. Late malformed grammar beats earlier component cap; no partial rows. Inverted bounds are complete meaningful contradictory constraints, not input invalid. Unknown profile receives common admission only; unsupported results contain no modeled rows.

## Bound and membership semantics

Constraint c accepts candidate v iff (no lower OR v>lower OR v=lower AND lower.inclusive) AND (no upper OR v<upper OR v=upper AND upper.inclusive), using precedence equality. Evaluate both sides for evidence; no skip of late declarations after an early false/contradiction. Scenario intersection membership is AND across ALL supplied constraints. Zero constraints: every supplied admitted candidate matches (vacuous conjunction); zero candidates: no supplied matches, no global existence inference.

Effective lower is greatest supplied lower precedence; effective upper is least supplied upper precedence; null if no respective bound. At equal precedence, combine inclusion flags by AND across ALL tied strongest bounds. Keep all contributor indices/ids/original versions/flags. Select earliest contributor as representative spelling for deterministic presentation only; never let that spelling/build metadata break the tie. Original declarations remain in report.

Bounds relation: unconstrained (bothnull), one_sided (onenull), ordered (lower<upper), equal_closed (equal and both effective flags true), equal_open (equal and either false), inverted (lower>upper). `bounds_contradiction` true only equal_open/inverted; sufficient proof no admitted version can match the supplied conjunction. False does NOT establish full-domain nonemptiness, especially for discrete open intervals. No global interval solver or witness synthesis.

Candidate row: original scenario/candidate indices/id/version, per-constraint lower/upper relation (less/equal/greater or null for absent bound), lower_pass/upper_pass, matches; intersection_matches AND of constraint matches. No literal-identity collapse. Scenario `supplied_match_indices` follows candidate order; `supplied_set_empty` equals list empty. Label this result explicitly as intersection over the supplied candidate list, never registry search or full package satisfiability. Package existence/availability/compatibility/security and unsupplied candidate existence remain unknown in assurances. Contradiction is a mathematical model observation, not a real package failure.

## Architecture, report and delivery

Thin modules: bounded common admission; reviewed task-local adaptation of own SemVer grammar/caps/comparator; effective-bound reduction; independent per-candidate conjunction model; deterministic serialization; owned-file CLI. No external runtime import path/dependencies/dynamic plugins/eval/subprocess/network in production. Freeze helper baseline hash/provenance; accepted lab stays read-only.

Report exact schema constraint-membership-report/1,input_profile,status complete/invalid/unsupported/limit,evaluation complete/incomplete,assurances,limits,scenarios ornull,error ornull. Complete scenario contains original declarations/indices, effective bounds/contributors, bounds_relation/bounds_contradiction, candidate rows and supplied match observations. Incomplete root has no scenario projections. Empty root scenarios is complete with no package/truth inference. Fixed codes/paths, no raw exception/filename echo; freeze all exact fields/priorities before code.

ASCII-safe sorted compactJSON+LF, serialized<=1MiB before output. Measure admitted maximum shapes/output amplification after approval; if cap unreachable label reduced tests as seams. CLI `python -I lab.py INPUT [--output FRESH_FILE]`, exclusive owned ordinary local file. Exit0 complete/help regardless of membership/contradiction,2 invalid/usage,3 unsupported,4 limit,5 I/O/delivery. Empty/existing/missing-parent output fails; no stdout success fallback. Exact write counts reject bool/None/short, checked flush/close/diagnostics, failed real descriptors neutralized before shutdown. Partial output/files possible; no atomic/durable/race promise.

## Threat model

Untrusted trees/strings may trigger hooks, exhaustion, diagnostics/report amplification or plausible partial answers. Identity-only exact admission and byte/tree/count/text/component bounds address these within a trusted interpreter/source/filesystem. Never execute candidate data or upstream source. Native concurrent mutation unsupported. No hard RSS/time/malware/hostile-filesystem/durability containment.

Semantic threats: treating build spelling as tie-break; OR rather than AND flags/conjunction; first/last-wins among tied contributors; implicit npm prerelease exclusion; assuming ordered bounds are dense; equating no supplied matches with no packages. Explicit fields/unknowns, hand controls and targeted mutants guard these. No dependency/supply-chain/security certification or actual system/package changes.

## Independent oracle design and hand controls

Freeze at least32 complete independent input/expected-report cases plus fixed admission/delivery expectations BEFORE product code. Do not derive oracles from the new reducer/model or upstream parser. Include exact original endpoints/provenance/contributor sets/per-candidate booleans/status/error order and nulls. Source-checked hand expectations below are planning examples, not executed results.

| Constraints (lower,upper) | Supplied candidate(s) | Expected model observation |
|---|---|---|
| [1.0.0,2.0.0) | 1.0.0,2.0.0 | first matches; second fails upper |
| (1.0.0,2.0.0] | 1.0.0,2.0.0 | first fails lower; second matches |
| [1.0.0+one,1.0.0+two] | 1.0.0+three | equal_closed, matches; literals retained |
| [1.0.0+one,1.0.0+two) | 1.0.0 | equal_open contradiction, no match |
| lower1.0.0 closed AND lower1.0.0+tag open | 1.0.0+other | tied flag AND makes effective lower open; fails |
| [1.0.0,2.0.0] AND (2.0.0,3.0.0] | 2.0.0 | equal_open contradiction |
| [1.0.0,2.0.0] AND [2.0.0,3.0.0] | 2.0.0+tag | equal_closed, matches |
| [1.0.0-alpha.2,1.0.0-alpha.10] | alpha.9 on same core | matches numeric prerelease |
| [1.0.0,2.0.0) | 1.1.0-alpha | matches explicit lab prerelease policy |
| [2.0.0,1.0.0] | 1.5.0 | inverted contradiction, complete/false |
| lower1.0.0 closed, uppernull | 9.0.0 | one_sided, matches |
| bothnull | 0.0.0-0 | unconstrained, matches |
| zero constraints | 1.0.0 | vacuous membershiptrue |
| zero candidates | none | supplied_set_empty true; no existence claim |
| (1.0.0-a,1.0.0-a.0) | a,a.0 on same core | ordered, both fail, no density inference |
| [1.0.0,2.0.0) | 0.0.0 only | supplied_set_empty true while1.5.0 would match if supplied |

Also cover duplicate ids versus duplicate versions, max/one-past bounds/counts/aliases, booleans versus0, noncanonical/nonASCII/deep/large-key/metaclass controls, malformed later unused bounds/candidate behind earlier contradiction, unknown profile with malformed common fields, all-grammar-before-caps and exact source restoration.

Meaningful mutations: tied inclusion AND->OR, weaker instead of stronger lower, intersection AND->OR, build tie-break, drop a tied contributor, inject npm prerelease exclusion or infer global emptiness from no supplied match. Select at least4 distinct intended assertion targets; crashes/import errors never count. Finite independently supplied rank-domain membership truth tables, constraint permutation/duplicate-conjunction/idempotence and effective-bound versus per-constraint conjunction equivalence supplement literal reports. Do not use the product comparator as the sole order oracle.

## Stages and definitions of done

1. After approval freeze CONTRACT, helper reuse receipts and >=32 full independent oracle cases/status/error/bounds/delivery outputs/hashes. Done before product code when all semantics/nulls/provenance/unknown distinctions are fixed and independently reviewable.
2. Adapt owned helper and implement admission/reduction/membership. Done when frozen API reports, native identity/no-hook/alias/cycle/immutability controls and finite hand-rank checks pass; unknown/invalid/limit contain no rows.
3. Implement checked CLI. Done when all full cases run via actual process normal/O and fresh/existing/empty/help/usage/both-failed pipes pass; narrow dirty/short/flush/close seams labelled, output reachability measured, no overwrites/fallback.
4. Verification/documentation: normal/O/restored suites, >=4 intended assertion mutants/source restoration, compile, available installed production/harness SAST separate with reviewed findings, actual ECC self-review/fixes/rechecks, current source/fixture receipts, reusable no-install verifier, README/demo/MIT/attribution/AI/SECURITY/DECISIONS/LEARNING/STATE and vault milestone. No hosted/repository checks claimed unless separately authorized; Python3.11+ intended, only actual runtime tested reported.

## Historical preimplementation review gate (superseded by approval)

Research/recommendation/concrete stages ready for coordinator review. No project source/tests/executable implementation yet. Only research captures/docs/worker evidence exist. Approval must identify this plan/addenda before stage1 begins. No successor or external work inferred from this file.

Approval recorded October5 05:24; root-depth0 includes keys/leaves, exact write counts also reject float. Stage1 freeze completed before source adaptation. No further external scope granted.
