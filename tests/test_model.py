"""Frozen reports and independent finite ranks; adversarial native admission."""
import copy
import hashlib
import itertools
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from constraint_lab.admission import LIMITS, Rejection, preflight
from constraint_lab.model import evaluate, evaluate_bytes, serialize

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / "tests/cases.json").read_text())


def document():
    return copy.deepcopy(CASES[0]["input"])


def row(value):
    return evaluate(value)["scenarios"][0]


class ModelTests(unittest.TestCase):
    def test_frozen_reports(self):
        for case in CASES:
            with self.subTest(case=case["name"]):
                self.assertEqual(evaluate(case["input"]), case["expected"])
                self.assertEqual(evaluate_bytes(json.dumps(case["input"]).encode()), case["expected"])

    def test_freeze_hashes(self):
        freeze=json.loads((ROOT/"evidence/freeze.json").read_text())
        self.assertGreaterEqual(freeze["complete_reports"],32)
        for item in freeze["files"]:
            data=(ROOT/item["path"]).read_bytes()
            self.assertEqual(len(data),item["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(),item["sha256"])

    def test_finite_rank_membership(self):
        # Hand ordered ranks, no product comparator used to derive decisions.
        domain=["1.0.0-a","1.0.0-a.0","1.0.0","1.0.0+tag","2.0.0"]
        ranks=[0,1,2,2,3]
        count=0
        for lo, hi, closed_lo, closed_hi in itertools.product(range(5),range(5),(False,True),(False,True)):
            value=document();s=value["scenarios"][0]
            s["constraints"]=[dict(id="b",lower=dict(version=domain[lo],inclusive=closed_lo),upper=dict(version=domain[hi],inclusive=closed_hi))]
            s["candidates"]=[dict(id=f"v{i}",version=v) for i,v in enumerate(domain)]
            result=row(value)
            expected=[i for i,r in enumerate(ranks) if (r>ranks[lo] or (r==ranks[lo] and closed_lo)) and (r<ranks[hi] or (r==ranks[hi] and closed_hi))]
            self.assertEqual(result["supplied_match_indices"],expected)
            self.assertEqual(result["bounds_contradiction"],ranks[lo]>ranks[hi] or (ranks[lo]==ranks[hi] and not(closed_lo and closed_hi)))
            count+=len(domain)
        self.assertEqual(count,500)

    def test_effective_equivalence_permutation_idempotence(self):
        # Explicit ranks and both overlapping/disjoint hand intervals.
        domain=["0.0.0","1.0.0","1.0.0+tag","1.5.0","2.0.0","3.0.0"]
        ranks=[0,1,1,2,3,4]
        for a,b in itertools.product(range(6),repeat=2):
            value=document();s=value["scenarios"][0]
            declarations=[dict(id="a",lower=dict(version=domain[a],inclusive=True),upper=None),dict(id="b",lower=None,upper=dict(version=domain[b],inclusive=False))]
            expected=[i for i,r in enumerate(ranks) if r>=ranks[a] and r<ranks[b]]
            s["candidates"]=[dict(id=f"v{i}",version=v) for i,v in enumerate(domain)]
            for ds in (declarations,list(reversed(declarations)),declarations+[dict(declarations[0],id="dup")]):
                s["constraints"]=ds
                result=row(value)
                self.assertEqual(result["supplied_match_indices"],expected)
                effective=dict(id="effective",lower={k:result["effective_lower"][k] for k in ("version","inclusive")},upper={k:result["effective_upper"][k] for k in ("version","inclusive")})
                s["constraints"]=[effective]
                self.assertEqual(row(value)["supplied_match_indices"],expected)

    def test_immutability_and_alias_occurrences(self):
        value=document();s=value["scenarios"][0];bound=s["constraints"][0]["lower"]
        s["constraints"][0]["upper"]=bound
        before=copy.deepcopy(value);result=evaluate(value)
        self.assertEqual(value,before)
        result["scenarios"][0]["constraints"][0]["lower"]["version"]="changed"
        self.assertEqual(value,before)
        with patch.dict(LIMITS,version_occurrences=3):
            self.assertEqual(evaluate(value)["error"]["code"],"version_occurrence_limit")

    def test_native_no_hooks(self):
        for behavior in (False,True,"raise"):
            calls=[]
            class Meta(type):
                def __eq__(cls,other):
                    calls.append("type-eq")
                    if behavior=="raise": raise RuntimeError("hook")
                    return behavior
                def __ne__(cls,other):
                    calls.append("type-ne")
                    if behavior=="raise": raise RuntimeError("hook")
                    return behavior
            class Exotic(metaclass=Meta):
                def __len__(self): calls.append("len"); raise RuntimeError("hook")
                def __eq__(self,other): calls.append("eq"); raise RuntimeError("hook")
                def __hash__(self): calls.append("hash"); return 7
            obj=Exotic()
            key_input={obj:None};calls.clear() # key construction precedes API.
            values=[obj,key_input,dict(profile=obj,synthetic=True,scenarios=[])]
            for level in ("scenario","bound","flag","version"):
                v=document()
                if level=="scenario": v["scenarios"][0]=obj
                elif level=="bound": v["scenarios"][0]["constraints"][0]["lower"]=obj
                else: v["scenarios"][0]["constraints"][0]["lower"]["inclusive" if level=="flag" else "version"]=obj
                values.append(v)
            for v in values:
                self.assertEqual(evaluate(v)["error"]["code"],"ordinary_type_required")
                self.assertEqual(calls,[])

    def test_subclasses_and_cycles(self):
        class Child(dict):
            def items(self): raise RuntimeError("must not iterate")
        self.assertEqual(evaluate(Child())["error"]["code"],"ordinary_type_required")
        x=[];x.append(x)
        self.assertEqual(evaluate(x)["error"],dict(code="cycle",path="/0"))
        self.assertEqual(evaluate(1.0)["error"]["code"],"ordinary_type_required")
        self.assertEqual(evaluate_bytes(bytearray(b"{}"))["error"]["code"],"bytes_required")

    def test_depth_keys_and_nodes(self):
        # Root0: eight child lists, then a leaf at9 exceeds; at8 accepted.
        x=None
        for _ in range(8): x=[x]
        preflight(x)
        with self.assertRaises(Rejection) as caught: preflight([x])
        self.assertEqual(caught.exception.code,"depth_limit")
        preflight({"a":None}) #3 nodes: dict/key/value
        with patch.dict(LIMITS,nodes=2):
            with self.assertRaises(Rejection) as caught: preflight({"a":None})
            self.assertEqual(caught.exception.code,"node_limit")
        self.assertEqual(evaluate({"x"*257:None})["error"],dict(code="text_limit",path="/key-0"))
        with patch.dict(LIMITS,depth=6): self.assertEqual(evaluate(document())["status"],"complete")
        with patch.dict(LIMITS,depth=5): self.assertEqual(evaluate(document())["status"],"limit")

    def test_raw_and_decoder(self):
        controls=[(b"x"*65537,"raw_limit"),(b"\xff","utf8_invalid"),(b'{"a":1,"a":2}',"duplicate_key"),(b"NaN","constant_invalid"),(b"9"*33,"numeric_limit"),(b"[}","json_invalid"),(b"["*10,"depth_limit")]
        for raw,code in controls:
            self.assertEqual(evaluate_bytes(raw)["error"]["code"],code)
        self.assertNotEqual(evaluate_bytes(b" "*65536)["error"]["code"],"raw_limit")

    def test_counts_boundary_and_global(self):
        v=dict(profile="explicit-semver-bounds/1",synthetic=True,scenarios=[dict(id=f"s{i}",constraints=[],candidates=[]) for i in range(16)])
        self.assertEqual(evaluate(v)["status"],"complete")
        v["scenarios"].append(dict(id="extra",constraints=[],candidates=[]))
        self.assertEqual(evaluate(v)["error"]["code"],"scenario_limit")
        for field,count,total,code in (("constraints",8,64,"total_constraint_limit"),("candidates",16,128,"total_candidate_limit")):
            v=dict(profile="explicit-semver-bounds/1",synthetic=True,scenarios=[])
            for i in range(8):
                items=[dict(id=f"x{j}",lower=None,upper=None) if field=="constraints" else dict(id=f"x{j}",version="1.0.0") for j in range(count)]
                v["scenarios"].append(dict(id=f"s{i}",constraints=items if field=="constraints" else [],candidates=items if field=="candidates" else []))
            self.assertEqual(evaluate(v)["status"],"complete")
            extra=copy.deepcopy(v["scenarios"][0]);extra["id"]="extra";extra[field]=extra[field][:1];v["scenarios"].append(extra)
            self.assertEqual(evaluate(v)["error"]["code"],code)

    def test_id_namespaces_and_duplicate_priority(self):
        for namespace in ("scenarios","constraints","candidates"):
            v=document()
            items=v["scenarios"] if namespace=="scenarios" else v["scenarios"][0][namespace]
            items.append(copy.deepcopy(items[0]))
            self.assertEqual(evaluate(v)["error"]["code"],"duplicate_id")
        v=document();v["scenarios"][0]["candidates"][0]["id"]="b0"
        self.assertEqual(evaluate(v)["status"],"complete")
        for label in ("","a"*33,"bad/id",1,None,True):
            v=document();v["scenarios"][0]["id"]=label
            self.assertEqual(evaluate(v)["error"]["code"],"id_grammar")

    def test_full_node_occurrences(self):
        preflight([None]*4095)
        with self.assertRaises(Rejection) as caught: preflight([None]*4096)
        self.assertEqual(caught.exception.code,"node_limit")
        alias=[None]
        with patch.dict(LIMITS,nodes=4):
            with self.assertRaises(Rejection) as caught: preflight([alias,alias])
            self.assertEqual(caught.exception.code,"node_limit")

    def test_version_caps(self):
        for text,code in (("9"*32+".0.0",None),("1.0.0+"+"a"*64,None),("1.0.0+"+"a"*65,"identifier_limit"),("1.0.0+"+".".join(["a"]*17),"identifier_count_limit"),("1.0.0-"+"9"*33,"numeric_prerelease_limit"),("1.0.0+000",None)):
            v=document();v["scenarios"][0]["candidates"][0]["version"]=text
            r=evaluate(v)
            self.assertEqual(None if r["error"] is None else r["error"]["code"],code)

    def test_late_malformed_after_contradiction(self):
        v=document();s=v["scenarios"][0];s["constraints"][0]["lower"]["version"]="9.0.0"
        s["constraints"].append(dict(id="late",lower=None,upper=dict(version="bad",inclusive=True)))
        result=evaluate(v)
        self.assertEqual(result["error"],dict(code="version_grammar",path="/scenarios/0/constraints/1/upper/version"))
        self.assertIsNone(result["scenarios"])

    def test_serialization(self):
        result=evaluate(document());data=serialize(result)
        self.assertTrue(data.endswith(b"\n"));self.assertTrue(data.isascii())
        self.assertEqual(json.loads(data),result)
        with patch.dict(LIMITS,output_bytes=1):
            with self.assertRaises(Rejection): serialize(result)
