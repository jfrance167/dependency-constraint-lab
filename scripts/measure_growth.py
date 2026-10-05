"""Reachable native/byte shapes and conservative output upper bound."""
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from constraint_lab.model import evaluate,evaluate_bytes,serialize


def shape(length):
    # Restricted ASCII build spelling, bounded identifiers, exactly length.
    pieces=[];remaining=length-6
    while remaining:
        n=min(64,remaining);pieces.append("a"*n);remaining-=n
        if remaining: remaining-=1
    version="1.0.0+"+".".join(pieces)
    return dict(profile="explicit-semver-bounds/1",synthetic=True,scenarios=[
        dict(id="s"*30+str(i),constraints=[dict(id="b"*30+str(j),lower=dict(version=version,inclusive=True),
            upper=dict(version=version,inclusive=True)) for j in range(8)],
            candidates=[dict(id="v"*29+str(j),version=version) for j in range(16)]) for i in range(8)])


def main():
    measurements=[]
    for length in (7,128,185,256):
        value=shape(length);raw=json.dumps(value,separators=(",",":")).encode()
        report=evaluate(value)
        if report["status"]!="complete": raise RuntimeError("Measurement shape invalid")
        measurements.append(dict(version_chars=length,native_status=report["status"],raw_bytes=len(raw),
            byte_status=evaluate_bytes(raw)["status"],report_bytes=len(serialize(report)),checks=1024,
            constraints=64,candidates=128,version_occurrences=256))
    # Loose safe per-element ceilings: allowed IDs/versions have no JSON escapes.
    # Up to64 declarations;128 contributor records;128 candidates;1024 checks;
    #32 effective envelopes;16 scenario envelopes; fixed root<2048 bytes.
    bound=64*800+128*400+128*400+1024*256+32*400+16*400+2048
    if bound>=1048576: raise RuntimeError("Bound does not establish reachability")
    incomplete_bound=8*(256*6+16)+2048 # escaped bounded path plus fixed report.
    result=dict(measurements=measurements,conservative_upper_bytes=bound,
        incomplete_upper_bytes=incomplete_bound,
        output_cap=1048576,cap_reachable_by_admitted_reports=False,
        note="Loose structural proof, not measured exact maximum. Reduced-cap tests are delivery seams.")
    print(json.dumps(result,indent=2))


if __name__=="__main__": main()
