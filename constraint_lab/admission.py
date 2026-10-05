"""Whole-input, exact-type admission before grammar or comparison."""

import json
import re

PROFILE = "explicit-semver-bounds/1"
LIMITS = dict(raw_bytes=65536, depth=8, nodes=4096, scenarios=16,
              constraints_per_scenario=8, candidates_per_scenario=16,
              constraints=64, candidates=128, version_occurrences=256,
              version_chars=256, numeric_digits=32, identifiers=16,
              identifier_chars=64, output_bytes=1048576)


class Rejection(ValueError):
    """A fixed code/path; untrusted values never enter diagnostics."""

    def __init__(self, code, path="", status="invalid"):
        super().__init__(code)
        self.code, self.path, self.status = code, path, status


def reject(code, path="", status="invalid"):
    raise Rejection(code, path, status)


def _lexical_gate(text):
    containers, quoted, escaped, numeric = [], False, False, 0
    for char in text:
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if numeric and char in "0123456789.eE+-":
            numeric += 1
            if numeric > 32:
                reject("numeric_limit", status="limit")
            continue
        numeric = 0
        if char == '"':
            quoted = True
        elif char in "[{":
            containers.append(char)
            if len(containers) > LIMITS["depth"] + 1:
                reject("depth_limit", status="limit")
        elif char in "]}":
            if not containers or containers.pop() != ({"]": "[", "}": "{"}[char]):
                reject("json_invalid")
        elif char in "-0123456789":
            numeric = 1


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            reject("duplicate_key")
        result[key] = value
    return result


def _constant(_value):
    reject("constant_invalid")


def decode(raw):
    """Gate bytes, lexical depth and numeric length before JSON decoding."""
    if type(raw) is not bytes:
        reject("bytes_required")
    if len(raw) > LIMITS["raw_bytes"]:
        reject("raw_limit", status="limit")
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeError:
        reject("utf8_invalid")
    _lexical_gate(text)
    try:
        return json.loads(text, object_pairs_hook=_pairs, parse_constant=_constant)
    except (json.JSONDecodeError, RecursionError):
        reject("json_invalid")


def preflight(value):
    """Count every occurrence including aliases/keys; reject only ancestor cycles."""
    active, nodes = set(), 0
    stack = [(value, "", 0, False, False)]
    while stack:
        obj, path, depth, leaving, key_node = stack.pop()
        if leaving:
            active.remove(id(obj))
            continue
        nodes += 1
        if nodes > LIMITS["nodes"]:
            reject("node_limit", path, "limit")
        if depth > LIMITS["depth"]:
            reject("depth_limit", path, "limit")
        kind = type(obj)
        if key_node and kind is not str:
            reject("ordinary_type_required", path)
        if kind is str:
            if len(obj) > LIMITS["version_chars"]:
                reject("text_limit", path, "limit")
            if not obj.isascii():
                reject("ascii_required", path)
        elif kind is int:
            # Compare against a fixed bound before converting any huge native int.
            if abs(obj) >= 10 ** LIMITS["numeric_digits"]:
                reject("numeric_limit", path, "limit")
        elif kind is dict or kind is list:
            if id(obj) in active:
                reject("cycle", path)
            if len(obj) > LIMITS["nodes"] - nodes:
                reject("node_limit", path, "limit")
            active.add(id(obj))
            stack.append((obj, path, depth, True, False))
            if kind is list:
                for index in range(len(obj) - 1, -1, -1):
                    stack.append((obj[index], f"{path}/{index}", depth + 1, False, False))
            else:
                for index, (key, child) in reversed(list(enumerate(obj.items()))):
                    # Bound native keys before copying them into diagnostic paths.
                    safe_key = type(key) is str and len(key) <= LIMITS["version_chars"] and key.isascii()
                    segment = key.replace("~", "~0").replace("/", "~1") if safe_key else "invalid-key"
                    stack.append((child, f"{path}/{segment}", depth + 1, False, False))
                    stack.append((key, f"{path}/key-{index}", depth + 1, False, True))
        elif kind is not bool and kind is not type(None):
            reject("ordinary_type_required", path)


def _fields(value, keys, path=""):
    if type(value) is not dict or set(value) != set(keys):
        reject("object_fields", path)


def common(value):
    """Unknown profiles receive this entire common contract, not SemVer parsing."""
    preflight(value)
    _fields(value, ("profile", "synthetic", "scenarios"))
    profile = value["profile"]
    if type(profile) is not str or re.fullmatch(r"[A-Za-z0-9_./-]{1,32}", profile) is None:
        reject("profile_grammar", "/profile")
    if value["synthetic"] is not True:
        reject("synthetic_true_required", "/synthetic")
    scenarios = value["scenarios"]
    _array(scenarios, "/scenarios", "scenarios", "scenario_limit")
    seen = set()
    totals = [0, 0, 0]
    for index, scenario in enumerate(scenarios):
        path = f"/scenarios/{index}"
        _fields(scenario, ("id", "constraints", "candidates"), path)
        _label(scenario["id"], seen, path + "/id")
        constraints, candidates = scenario["constraints"], scenario["candidates"]
        _array(constraints, path + "/constraints", "constraints_per_scenario", "constraint_limit")
        _array(candidates, path + "/candidates", "candidates_per_scenario", "candidate_limit")
        seen_constraints, seen_candidates = set(), set()
        for i, constraint in enumerate(constraints):
            cp = f"{path}/constraints/{i}"
            _fields(constraint, ("id", "lower", "upper"), cp)
            _label(constraint["id"], seen_constraints, cp + "/id")
            for side in ("lower", "upper"):
                bound = constraint[side]
                if bound is None:
                    continue
                bp = cp + "/" + side
                _fields(bound, ("version", "inclusive"), bp)
                if type(bound["version"]) is not str:
                    reject("string_required", bp + "/version")
                if type(bound["inclusive"]) is not bool:
                    reject("boolean_required", bp + "/inclusive")
                totals[2] += 1
        for i, candidate in enumerate(candidates):
            cp = f"{path}/candidates/{i}"
            _fields(candidate, ("id", "version"), cp)
            _label(candidate["id"], seen_candidates, cp + "/id")
            if type(candidate["version"]) is not str:
                reject("string_required", cp + "/version")
        totals[0] += len(constraints)
        totals[1] += len(candidates)
        totals[2] += len(candidates)
        for total, key, code in zip(totals, ("constraints", "candidates", "version_occurrences"),
                ("total_constraint_limit", "total_candidate_limit", "version_occurrence_limit")):
            if total > LIMITS[key]:
                reject(code, path, "limit")
    return profile


def _label(label, seen, path):
    if type(label) is not str or re.fullmatch(r"[A-Za-z0-9_-]{1,32}", label) is None:
        reject("id_grammar", path)
    if label in seen:
        reject("duplicate_id", path)
    seen.add(label)


def _array(value, path, limit, code):
    if type(value) is not list:
        reject("array_required", path)
    if len(value) > LIMITS[limit]:
        reject(code, path, "limit")
