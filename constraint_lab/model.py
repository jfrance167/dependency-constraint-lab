"""Whole-input evaluation; model observations never imply package assurances."""
import json
from .admission import common, decode, LIMITS, PROFILE, Rejection, reject
from .version import caps, compare, grammar
from .bounds import classify, reduce_bound


def _report(profile, rows=None, error=None):
    status = error.status if error is not None else "complete"
    return dict(schema="constraint-membership-report/1", input_profile=profile, status=status,
        evaluation="complete" if status == "complete" else "incomplete", limits=dict(LIMITS),
        assurances=dict(policy="strict-bounded-semver", prereleases="all-admitted",
            build_metadata="ignored-for-precedence", candidate_domain="supplied-only",
            **{key: "unknown" for key in ("package_existence", "availability", "compatibility",
                "security", "unsupplied_candidate_existence")}),
        scenarios=rows if status == "complete" else None,
        error=None if error is None else dict(code=error.code, path=error.path))


def _occurrences(value):
    for i, scenario in enumerate(value["scenarios"]):
        for j, constraint in enumerate(scenario["constraints"]):
            for side in ("lower", "upper"):
                if constraint[side] is not None:
                    yield (i, "bound", j, side), constraint[side]["version"], f"/scenarios/{i}/constraints/{j}/{side}/version"
        for j, candidate in enumerate(scenario["candidates"]):
            yield (i, "candidate", j), candidate["version"], f"/scenarios/{i}/candidates/{j}/version"


def _scenario(index, scenario, parsed):
    constraints, candidates = scenario["constraints"], scenario["candidates"]
    parts = [{side: parsed[(index, "bound", i, side)] if c[side] is not None else None
              for side in ("lower", "upper")} for i, c in enumerate(constraints)]
    lower, left = reduce_bound(constraints, parts, "lower")
    upper, right = reduce_bound(constraints, parts, "upper")
    relation = classify(lower, upper, left, right)
    rows, matches = [], []
    for i, candidate in enumerate(candidates):
        version, checks = parsed[(index, "candidate", i)], []
        for j, constraint in enumerate(constraints):
            lr = compare(version, parts[j]["lower"])[0] if parts[j]["lower"] is not None else None
            ur = compare(version, parts[j]["upper"])[0] if parts[j]["upper"] is not None else None
            lp = lr is None or lr == "greater" or (lr == "equal" and constraint["lower"]["inclusive"])
            up = ur is None or ur == "less" or (ur == "equal" and constraint["upper"]["inclusive"])
            checks.append(dict(constraint_index=j, lower_relation=lr, upper_relation=ur,
                               lower_pass=lp, upper_pass=up, matches=lp and up))
        accepted = all(check["matches"] for check in checks)
        if accepted:
            matches.append(i)
        rows.append(dict(index=i, id=candidate["id"], version=candidate["version"],
                         checks=checks, intersection_matches=accepted))
    # Copy admitted scalar declarations; report edits cannot mutate native inputs.
    declarations = [dict(index=i, id=c["id"], **{side: None if c[side] is None else dict(c[side])
                    for side in ("lower", "upper")}) for i, c in enumerate(constraints)]
    return dict(index=index, id=scenario["id"], constraints=declarations, candidates=rows,
        effective_lower=lower, effective_upper=upper, bounds_relation=relation,
        bounds_contradiction=relation in ("equal_open", "inverted"),
        supplied_match_indices=matches, supplied_set_empty=not matches)


def evaluate(value):
    """Admit all common fields, then all grammar, then caps, before any modeling."""
    profile = None
    try:
        profile = common(value)
        if profile != PROFILE:
            reject("profile_unsupported", "/profile", "unsupported")
        parsed, paths = {}, {}
        for key, text, path in _occurrences(value):
            parsed[key], paths[key] = grammar(text, path), path
        for key, version in parsed.items():
            caps(version, paths[key])
        return _report(profile, [_scenario(i, s, parsed) for i, s in enumerate(value["scenarios"])])
    except Rejection as error:
        return _report(profile, error=error)


def evaluate_bytes(raw):
    """Strict bytes entry point; raw failures expose no modeled rows."""
    try:
        value = decode(raw)
    except Rejection as error:
        return _report(None, error=error)
    return evaluate(value)


def serialize(report):
    """Fully encode a bounded report before opening output."""
    data = (json.dumps(report, ensure_ascii=True, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")
    if len(data) > LIMITS["output_bytes"]:
        reject("output_limit", status="limit")
    return data
