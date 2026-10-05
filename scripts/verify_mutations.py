"""Isolated assertion mutants; original source never edited. No network/install."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

ROOT=Path(__file__).resolve().parents[1]
MUTANTS=[
    ("tied-inclusion","bounds.py",'inclusive=all(item["inclusive"] for item in contributors)',
     'inclusive=any(item["inclusive"] for item in contributors)',"tied-lower"),
    ("weak-lower","bounds.py",'strongest = "greater" if side == "lower" else "less"',
     'strongest = "less"',"strongest-lower"),
    ("intersection-or","model.py",'accepted = all(check["matches"] for check in checks)',
     'accepted = any(check["matches"] for check in checks)',"two-incompatible"),
    ("drop-tied-provenance","bounds.py",'contributors=contributors), chosen',
     'contributors=contributors[:1]), chosen',"all-tied-three"),
    ("build-tiebreak","version.py",'    return result(0, "equal")',
     '    return result(_order(left.build, right.build), "equal")',"build-equal")]


def main():
    sources={p.name:p.read_bytes() for p in (ROOT/"constraint_lab").glob("*.py")}
    work=ROOT/".verification-work"/("mutations-"+uuid.uuid4().hex);work.mkdir(parents=True)
    rows=[]
    for label,name,before,after,target in MUTANTS:
        dest=work/label;dest.mkdir()
        for folder in ("constraint_lab","tests","evidence","scripts"):
            shutil.copytree(ROOT/folder,dest/folder,ignore=shutil.ignore_patterns("__pycache__"))
        for name_to_copy in ("CONTRACT.md","lab.py"):
            shutil.copyfile(ROOT/name_to_copy,dest/name_to_copy)
        text=sources[name].decode()
        if text.count(before)!=1: raise RuntimeError("Mutation anchor changed")
        (dest/"constraint_lab"/name).write_text(text.replace(before,after))
        process=subprocess.run([sys.executable,"-I","scripts/run_tests.py"],cwd=dest,capture_output=True,timeout=45,check=False,shell=False)
        (dest/"stdout.log").write_bytes(process.stdout);(dest/"stderr.log").write_bytes(process.stderr)
        stderr=process.stderr.decode(errors="replace")
        detected=process.returncode==1 and "AssertionError" in stderr and f"case='{target}'" in stderr and "ERROR:" not in stderr
        rows.append(dict(mutation=label,target=target,exit=process.returncode,intended_assertion_detected=detected))
    unchanged=all((ROOT/"constraint_lab"/name).read_bytes()==data for name,data in sources.items())
    result=dict(outcomes=rows,original_unchanged=unchanged,
                original_sha256={k:hashlib.sha256(v).hexdigest() for k,v in sources.items()},work=str(work))
    print(json.dumps(result))
    return 0 if unchanged and all(r["intended_assertion_detected"] for r in rows) else 1


if __name__=="__main__": raise SystemExit(main())
