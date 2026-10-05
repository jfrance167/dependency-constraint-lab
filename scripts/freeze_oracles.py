"""Independent handwritten ranks/answers; never imports the implementation.

Run before product code. Complete reports are data fixtures, not snapshots of
product output. Endpoint selections and lower/upper pass bits are explicit.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIMITS = dict(raw_bytes=65536, depth=8, nodes=4096, scenarios=16,
              constraints_per_scenario=8, candidates_per_scenario=16,
              constraints=64, candidates=128, version_occurrences=256,
              version_chars=256, numeric_digits=32, identifiers=16,
              identifier_chars=64, output_bytes=1048576)
ASSURANCES = dict(policy="strict-bounded-semver", prereleases="all-admitted",
                  build_metadata="ignored-for-precedence", candidate_domain="supplied-only",
                  **{k: "unknown" for k in ("package_existence", "availability", "compatibility",
                      "security", "unsupplied_candidate_existence")})
# Independent rank declarations; equal build spellings share ranks.
RANKS = {"0.0.0-0": 0, "0.0.0": 1, "1.0.0-a": 2, "1.0.0-a.0": 3,
         "1.0.0-alpha.2": 4, "1.0.0-alpha.9": 5, "1.0.0-alpha.10": 6,
         "1.0.0": 7, "1.0.0+one": 7, "1.0.0+two": 7,
         "1.0.0+three": 7, "1.0.0+tag": 7, "1.0.0+other": 7,
         "1.1.0-alpha": 8, "1.5.0": 9, "2.0.0": 10, "2.0.0+tag": 10,
         "3.0.0": 11, "9.0.0": 12}


def endpoint(v, flag=True):
    return None if v is None else {"version": v, "inclusive": flag}


def report(profile="explicit-semver-bounds/1", status="complete", rows=None, error=None):
    return dict(schema="constraint-membership-report/1", input_profile=profile,
                status=status, evaluation="complete" if status == "complete" else "incomplete",
                assurances=ASSURANCES, limits=LIMITS, scenarios=rows if status == "complete" else None,
                error=error)


CASES = []


def control(name, declarations, versions, bits, selected, relation):
    """Selections and pass bits are hand answers, not reducer-derived."""
    constraints = [{"id": f"b{i}", "lower": endpoint(*lo), "upper": endpoint(*hi)}
                   for i, (lo, hi) in enumerate(declarations)]
    candidates = [{"id": f"v{i}", "version": v} for i, v in enumerate(versions)]
    inp = {"profile": "explicit-semver-bounds/1", "synthetic": True,
           "scenarios": [{"id": name, "constraints": constraints, "candidates": candidates}]}
    def effective(side, indices):
        if not indices:
            return None
        contributors = [{"index": i, "id": constraints[i]["id"], **constraints[i][side]}
                        for i in indices]
        return dict(version=contributors[0]["version"],
                    inclusive=all(x["inclusive"] for x in contributors), contributors=contributors)
    def relative(v, bound):
        if bound is None:
            return None
        a, b = RANKS[v], RANKS[bound["version"]]
        return "less" if a < b else "greater" if a > b else "equal"
    rows, matches = [], []
    for j, candidate in enumerate(candidates):
        checks = []
        for i, constraint in enumerate(constraints):
            lower, upper = bits[j][i]
            checks.append(dict(constraint_index=i,
                lower_relation=relative(candidate["version"], constraint["lower"]),
                upper_relation=relative(candidate["version"], constraint["upper"]),
                lower_pass=bool(lower), upper_pass=bool(upper), matches=bool(lower and upper)))
        accepted = all(x["matches"] for x in checks)
        if accepted:
            matches.append(j)
        rows.append(dict(index=j, **candidate, checks=checks, intersection_matches=accepted))
    scenario = dict(id=name, index=0,
        constraints=[dict(index=i, **c) for i, c in enumerate(constraints)], candidates=rows,
        effective_lower=effective("lower", selected[0]), effective_upper=effective("upper", selected[1]),
        bounds_relation=relation, bounds_contradiction=relation in ("inverted", "equal_open"),
        supplied_match_indices=matches, supplied_set_empty=not matches)
    CASES.append(dict(name=name, input=inp, expected=report(rows=[scenario])))


N = (None, True)
A = ("1.0.0", True)
B = ("2.0.0", True)
C = ("3.0.0", True)
control("closed-open", [(A,("2.0.0",False))], ["1.0.0","2.0.0"], [[[1,1]],[[1,0]]], ([0],[0]), "ordered")
control("open-closed", [(("1.0.0",False),B)], ["1.0.0","2.0.0"], [[[0,1]],[[1,1]]], ([0],[0]), "ordered")
control("build-equal", [(("1.0.0+one",True),("1.0.0+two",True))], ["1.0.0+three"], [[[1,1]]], ([0],[0]), "equal_closed")
control("build-open", [(("1.0.0+one",True),("1.0.0+two",False))], ["1.0.0"], [[[1,0]]], ([0],[0]), "equal_open")
control("tied-lower", [(A,N),(("1.0.0+tag",False),N)], ["1.0.0+other"], [[[1,1],[0,1]]], ([0,1],[]), "one_sided")
control("touch-open", [(A,B),(("2.0.0",False),C)], ["2.0.0"], [[[1,1],[0,1]]], ([1],[0]), "equal_open")
control("touch-closed", [(A,B),(B,C)], ["2.0.0+tag"], [[[1,1],[1,1]]], ([1],[0]), "equal_closed")
control("numeric-pre", [(("1.0.0-alpha.2",True),("1.0.0-alpha.10",True))], ["1.0.0-alpha.9"], [[[1,1]]], ([0],[0]), "ordered")
control("all-prereleases", [(A,("2.0.0",False))], ["1.1.0-alpha"], [[[1,1]]], ([0],[0]), "ordered")
control("inverted", [(B,A)], ["1.5.0"], [[[0,0]]], ([0],[0]), "inverted")
control("lower-only", [(A,N)], ["9.0.0"], [[[1,1]]], ([0],[]), "one_sided")
control("unbounded", [(N,N)], ["0.0.0-0"], [[[1,1]]], ([],[]), "unconstrained")
control("vacuous", [], ["1.0.0"], [[]], ([],[]), "unconstrained")
control("no-candidates", [(A,B)], [], [], ([0],[0]), "ordered")
control("non-dense", [(("1.0.0-a",False),("1.0.0-a.0",False))], ["1.0.0-a","1.0.0-a.0"], [[[0,1]],[[1,0]]], ([0],[0]), "ordered")
control("supplied-empty", [(A,B)], ["0.0.0"], [[[0,1]]], ([0],[0]), "ordered")
control("upper-only", [(N,A)], ["0.0.0","1.5.0"], [[[1,1]],[[1,0]]], ([],[0]), "one_sided")
control("strongest-lower", [(A,N),(B,N)], ["1.5.0","2.0.0"], [[[1,1],[0,1]],[[1,1],[1,1]]], ([1],[]), "one_sided")
control("strongest-upper", [(N,C),(N,B)], ["2.0.0","3.0.0"], [[[1,1],[1,1]],[[1,1],[1,0]]], ([],[1]), "one_sided")
control("tied-upper", [(N,A),(N,("1.0.0+two",False))], ["1.0.0+one"], [[[1,1],[1,0]]], ([],[0,1]), "one_sided")
control("duplicate-versions", [(A,B)], ["1.0.0","1.0.0","1.0.0+tag"], [[[1,1]],[[1,1]],[[1,1]]], ([0],[0]), "ordered")
control("duplicate-conjunction", [(A,B),(A,B)], ["1.5.0"], [[[1,1],[1,1]]], ([0,1],[0,1]), "ordered")
control("permutation", [(B,N),(A,N)], ["1.5.0"], [[[0,1],[1,1]]], ([0],[]), "one_sided")
control("two-incompatible", [(N,A),(B,N)], ["1.0.0","2.0.0"], [[[1,1],[0,1]],[[1,0],[1,1]]], ([1],[0]), "inverted")
control("pre-versus-release", [(("1.0.0-a",True),A)], ["1.0.0-a.0","1.0.0"], [[[1,1]],[[1,1]]], ([0],[0]), "ordered")
control("open-lower-above", [(("1.0.0",False),B)], ["1.5.0"], [[[1,1]]], ([0],[0]), "ordered")
control("open-upper-below", [(A,("2.0.0",False))], ["1.5.0"], [[[1,1]]], ([0],[0]), "ordered")
control("both-open-equal", [(("1.0.0",False),("1.0.0",False))], ["1.0.0"], [[[0,0]]], ([0],[0]), "equal_open")
control("all-tied-three", [(A,N),(("1.0.0+one",True),N),(("1.0.0+two",False),N)], ["1.5.0"], [[[1,1],[1,1],[1,1]]], ([0,1,2],[]), "one_sided")
control("empty-everything", [], [], [], ([],[]), "unconstrained")
control("max-constraints", [(A,B)]*8, ["1.5.0"], [[[1,1]]*8], (list(range(8)),list(range(8))), "ordered")
control("max-candidates", [(A,B)], ["1.5.0"]*16, [[[1,1]]]*16, ([0],[0]), "ordered")
CASES.append(dict(name="zero-scenarios", input=dict(profile="explicit-semver-bounds/1", synthetic=True, scenarios=[]), expected=report(rows=[])))


def failure(name, inp, code, path="", status="invalid", profile=None):
    CASES.append(dict(name=name,input=inp,expected=report(profile,status,error=dict(code=code,path=path))))


def base():
    return json.loads(json.dumps(CASES[0]["input"]))


x=base();x["profile"]="unknown/1";x["scenarios"][0]["constraints"][0]["lower"]["version"]="bad"
failure("unknown-no-version-parse",x,"profile_unsupported","/profile","unsupported","unknown/1")
x=base();x["profile"]="unknown/1";x["scenarios"][0]["candidates"][1]["id"]="v0"
failure("unknown-common-first",x,"duplicate_id","/scenarios/0/candidates/1/id")
x=base();x["scenarios"][0]["constraints"][0]["lower"]["inclusive"]=1
failure("bool-not-int",x,"boolean_required","/scenarios/0/constraints/0/lower/inclusive")
x=base();x["scenarios"][0]["constraints"][0]["upper"]["version"]="01.0.0"
failure("upper-leading-zero",x,"version_grammar","/scenarios/0/constraints/0/upper/version",profile="explicit-semver-bounds/1")
x=base();x["scenarios"][0]["constraints"][0]["lower"]["version"]="9"*33+".0.0";x["scenarios"][0]["candidates"][1]["version"]="bad"
failure("all-grammar-before-caps",x,"version_grammar","/scenarios/0/candidates/1/version",profile="explicit-semver-bounds/1")
x=base();x["scenarios"][0]["constraints"][0]["lower"]["version"]="9"*33+".0.0"
failure("core-cap",x,"core_limit","/scenarios/0/constraints/0/lower/version","limit","explicit-semver-bounds/1")
x=base();x["scenarios"][0]["candidates"][0]["version"]="1.0.0-a.01"
failure("numeric-pre-zero",x,"version_grammar","/scenarios/0/candidates/0/version",profile="explicit-semver-bounds/1")
x=base();x["synthetic"]=False
failure("synthetic-required",x,"synthetic_true_required","/synthetic")
x=base();x["scenarios"][0]["candidates"][0]["version"]="é"
failure("ascii-first",x,"ascii_required","/scenarios/0/candidates/0/version")
x=base();x["scenarios"][0]["constraints"]*=9
failure("constraint-count",x,"constraint_limit","/scenarios/0/constraints","limit")
x=base();x["scenarios"][0]["candidates"]*=9
failure("candidate-count",x,"candidate_limit","/scenarios/0/candidates","limit")
x=base();x["scenarios"][0]["constraints"][0]["lower"]=dict(version="1.0.0")
failure("bound-fields",x,"object_fields","/scenarios/0/constraints/0/lower")


def main():
    (ROOT/"tests").mkdir(exist_ok=True)
    (ROOT/"evidence").mkdir(exist_ok=True)
    path=ROOT/"tests/cases.json"
    with path.open("x",encoding="utf-8") as stream:
        stream.write(json.dumps(CASES,indent=2,ensure_ascii=True)+"\n")
    rows=[]
    for name in ("CONTRACT.md","tests/cases.json","scripts/freeze_oracles.py"):
        data=(ROOT/name).read_bytes()
        rows.append(dict(path=name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
    with (ROOT/"evidence/freeze.json").open("x",encoding="utf-8") as stream:
        json.dump(dict(method="handwritten ranks, pass bits, explicit contributors; no product imports",
            full_reports=len(CASES),complete_reports=sum(c["expected"]["status"]=="complete" for c in CASES),files=rows),stream,indent=2)
        stream.write("\n")
    print(json.dumps(dict(full_reports=len(CASES),complete_reports=33,product_created=False)))


if __name__=="__main__":
    main()
