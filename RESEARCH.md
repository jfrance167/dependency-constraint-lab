# Dependency constraint research — October5, 2026

Historical research-stage snapshot before05:24 implementation approval; current completion/status is in STATE.md. Candidate source is inspection material, never authorization. No candidate execution/installation, registry/package/dependency fetch, solver, full checkout audit, upstream/hosted tests or Scorecard performed.

## Reuse and search

Read accepted version-precedence-lab parser/comparator, corrected admission and CLI. Matched their current hashes against the accepted receipt without rerunning its suite or editing that lab. Reuse own MIT-licensed strict bounded SemVer helper after approval, with a task-local reviewed adaptation so this tool remains independently usable. Retain source provenance rather than import an arbitrary external workspace at runtime. Identity-only native checks and broken-sink delivery are reusable requirements, not reasons to weaken new review.

Read vault Home/Codex Integration and relevant SemVer research/implementation note; targeted research/project-note searches found no dedicated constraint-membership/intersection model. Relevant inventory/signed-update/SemVer file searches found SemVer's explicit range exclusions, not an implementation to reuse. This is scoped discovery, not exhaustive search. Preserve accepted labs/parent Git/shared tooling/GLPI exclusion.

Connected GitHub initial broad range search and default-branch tree requests failed transport. Later exact node-semver search succeeded and listed npm/node-semver, a Python port, and an archived PHP project. Inspect upstream npm semantics rather than adopt an unreviewed port. Pinned npm and packaging trees/source reads succeeded. Some optional CodeQL/exclude-fixture/PR requests failed; record failures separately. Official web pages provided packaging PR and standards fallback. Source URLs/blob identities in research/source-records.json.

## Primary semantics

SemVer2.0.0 defines syntax/precedence, including numeric prereleases and ignored build metadata, but does not prescribe a general dependency-range language. [Specification](https://github.com/semver/semver/blob/f99d5485190a47c0863949e7da810a5553e0ed4d/semver.md), originally authored by Tom Preston-Werner, CC BY3.0. Our explicit bounds are custom teaching semantics, not an npm/PEP440 parser.

npm range matching adds prerelease opt-in beyond ordering; includePrerelease changes that policy. Caret/tilde/x-range and comparator sets require ecosystem interpretation. [Official node-semver documentation](https://github.com/npm/node-semver#prerelease-tags).

PEP440 exclusive comparisons have special same-release pre/post/local behavior; prerelease handling also depends on declared policy and filtering context. It cannot be replaced by generic SemVer comparisons. [PyPA version specifiers](https://packaging.python.org/en/latest/specifications/version-specifiers/#exclusive-ordered-comparison).

## Candidate source assessment

**npm/node-semver**, commit6e05b7637396ac66522cff8731f07cfe0ef49a29, latest release endpoint v7.8.5 June19,2026. Read README/classes/range.js/classes/comparator.js, range class tests/intersection/include fixtures, LICENSE/package.json/CI/audit workflows. Range splits OR groups and AND comparators, rewrites shorthands, strips build metadata and applies same-core prerelease opt-in. Comparator has unbounded/sentinel cases and intersection logic. Tests explicitly cover includePrerelease, strict/loose parsing, builds and intersection symmetry. This is broader than our bounded exact-input goal. [Pinned source](https://github.com/npm/node-semver/tree/6e05b7637396ac66522cff8731f07cfe0ef49a29).

ISC license requires copyright/permission notices on copies. Manifest has no runtime dependencies, dev tap/eslint/template tooling and Node>=10 declaration. CI covers several runtimes/platforms, but actions use moving version tags; audit workflow presence is not a clean-audit result. CodeQL exists in tree but contents fetch failed. [PR878](https://github.com/npm/node-semver/pull/878), merged June19, fixes includePrerelease lower-bound handling for partial tilde forms; actual changed include fixtures inspected, upstream reported checks not run by us. Good ecosystem candidate if npm parsing is the goal; do not fork/reimplement its full grammar casually.

**PyPA packaging**, commit4a920d632a0e81ef2b06dc94d9048eee9e569c8d. Read focused SpecifierSet/VersionRange membership/intersection branches and corresponding tests; reused today's same-commit manifest/license/CI captures from SemVer research. VersionRange retains prerelease policy, distinguishes membership/filtering and supports broader set algebra/literal admission. Matching can differ from simple ordered comparisons. Tests include empty/full/singleton, local-label distinction, prerelease flags, arbitrary literals and set operations. [Pinned source](https://github.com/pypa/packaging/tree/4a920d632a0e81ef2b06dc94d9048eee9e569c8d).

No mandatory runtime dependencies, flit_core build and separate pytest/Hypothesis tooling. Apache2.0 OR BSD2; actual BSD text inspected, Apache alternative not fully reviewed because no adoption proposed. Multi-OS/runtime CI uses pinned actions. Prior same-commit maintenance evidence October2 and release26.3 August4 is retained from today's research, not a fresh latest-release claim. [PR1267](https://github.com/pypa/packaging/pull/1267), primary web fallback, describes additive public PEP440 VersionRange sharing internal bound machinery and preserving policy. Appropriate for Python ecosystem requirements, wrong standard for SemVer teaching bounds.

Missing audits/indicators are uncertainty, not proof of insecurity; no dependency safety certification. License/CI/source presence alone does not establish artifact authenticity or correctness. Large files were inspected by relevant branches/tests, not claimed as a full code audit.

## Recommendation and consequential limit

Build one original stdlib **explicit SemVer bounds plus supplied-candidate intersection** profile, adapting the accepted owned helper after approval. No ecosystem shorthand parsing, exclusion holes/OR/union/complement, dependency graph/solver or version synthesis. This makes inclusive/exclusive endpoint ties and build-equivalent identifiers visible without pulling in a broad parser. Fewer dependencies alone do not prove security; new bound logic needs independent oracles/review.

SemVer order is not dense: between prerelease1.0.0-a and1.0.0-a.0 there is no intervening precedence value under the identifier rules (numeric0 is the first added identifier). Thus lower<upper does not justify claiming an open interval contains a version. This is a source-based mathematical inference, not an upstream library bug finding or execution result. Report only a **sufficient boundary contradiction** and exact matching of the **supplied finite candidates**. An empty supplied match list does not prove no unsupplied version exists, no package is available, or a dependency can/cannot resolve. Even unconstrained/candidate-empty input preserves those unknowns.

Local draft rejected; remote free pricing unverified, so no remote inference. research/worker-review.md records actual outcomes. Codex retains semantics/security judgment. Proposed scope and staged approval request in PLAN.md.
