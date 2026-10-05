# Frozen contract — explicit-semver-bounds/1

Approved local stages1–4: coordinator SUCCESSORS.md October5 05:24, existing
chat 01a10a3e-df45-71a2-baae-bf109c3d8d22 under Jake's direct delegation.
PLAN.md semantics and limits apply. Depth counts root at0, each key/value/list
element at parent+1, containers and leaves alike. Deepest supported leaf is6.
Aliases count per occurrence; ancestor cycles reject. Exact builtin identity
admission precedes any user hooks. No concurrent native mutation guarantee.

Validation order: bytes/raw/UTF8; lexical depth/numeric token; decoder duplicate
key/nonfinite/syntax; native DFS nodes/depth/type/text/numeric; root fields,
profile grammar, synthetic true, scenarios type/count; each scenario fields/id,
constraints type/count, candidates type/count, constraint fields/id then lower
then upper type/fields/version-string/inclusive-bool, candidate fields/id/string;
global constraint/candidate/version occurrence limits after each scenario;
unsupported decision; ALL version grammar in scenario constraint lower/upper
then candidates order; ALL version component caps in that same order; model.
Earlier structure failures dominate later grammar. Generic text/ASCII admission
precedes profile reporting: input_profile stays null until common succeeds.

Root report exact keys: schema,input_profile,status,evaluation,assurances,limits,
scenarios,error. schema constraint-membership-report/1. Complete: evaluation
complete, error null, scenarios list. Other statuses invalid/limit/unsupported:
evaluation incomplete, scenarios null, error {code,path}. Unsupported error
profile_unsupported at /profile. Fixed assurances: policy strict-bounded-semver;
prereleases all-admitted; build_metadata ignored-for-precedence;
candidate_domain supplied-only; package_existence,availability,compatibility,
security,unsupplied_candidate_existence all unknown. No whole-domain solver.

Scenario exact keys id,index,constraints,candidates,effective_lower,
effective_upper,bounds_relation,bounds_contradiction,supplied_match_indices,
supplied_set_empty. Original constraint fields plus index. Candidate fields plus
index,checks,intersection_matches. Check exact constraint_index,lower_relation,
upper_relation,lower_pass,upper_pass,matches. Relations less/equal/greater or
null for absent endpoints; absent passes true. Effective endpoint null or
{version,inclusive,contributors}; contributor {index,id,version,inclusive}.
Earliest strongest tie supplies spelling; ALL strongest tied contributors stay
in declaration order, inclusion AND. Candidate checks evaluate both endpoints
and all constraints. Intersection AND, vacuous true. Original declarations and
candidate occurrences preserved; no literal/build equality collapse.

Relations unconstrained/one_sided/ordered/equal_closed/equal_open/inverted.
Contradiction true only equal_open/inverted, sufficient impossibility within
model. Ordered/false does not imply nonempty domain (a to a.0 open gap).
supplied_set_empty means supplied_match_indices is empty, including no candidates.

Limits exact report dictionary: raw_bytes65536,depth8,nodes4096,scenarios16,
constraints_per_scenario8,candidates_per_scenario16,constraints64,candidates128,
version_occurrences256,version_chars256,numeric_digits32,identifiers16,
identifier_chars64,output_bytes1048576.
Admission codes bytes_required,raw_limit,utf8_invalid,numeric_limit,depth_limit,
json_invalid,duplicate_key,constant_invalid,node_limit,ordinary_type_required,
text_limit,ascii_required,cycle,object_fields,profile_grammar,
synthetic_true_required,array_required,scenario_limit,id_grammar,duplicate_id,
constraint_limit,candidate_limit,string_required,boolean_required,
total_constraint_limit,total_candidate_limit,version_occurrence_limit.
Component codes version_grammar/core_limit/identifier_count_limit/
identifier_limit/numeric_prerelease_limit. All *_limit status limit; others invalid.
Native paths RFC6901 segments, invalid key path key-N, cycle occurrence path.
Decoder/raw errors empty path. Common counters evaluated constraints then
candidates then occurrences. Version grammar/caps use endpoint /version paths.

serialize sorted compact ASCII JSON plus LF; fully prepare before checked delivery.
Output cap1048576; output_limit rejection, CLI fixed diagnostic. CLI local
ordinary files, exclusive fresh output. Exit0 complete/help,2 invalid/usage,
3 unsupported,4 limit,5 I/O or delivery. Diagnostic {error:usage|input_failure|
output_failure|output_limit} compact JSON+LF. Exact builtin int write count equals
payload length, checked flush/close. Bool/float/None/short reject. Failed output
may leave partial file/bytes. No atomicity/durability/hostile-path guarantee.
No network, registry, packages, install, execution or security certification.

Independent oracle construction uses handwritten precedence ranks, literal
per-constraint pass bits and explicitly selected contributor indices; it imports
no product code and contains no strongest-bound reducer. freeze.json hashes the
complete reports and this contract before product source is created.
