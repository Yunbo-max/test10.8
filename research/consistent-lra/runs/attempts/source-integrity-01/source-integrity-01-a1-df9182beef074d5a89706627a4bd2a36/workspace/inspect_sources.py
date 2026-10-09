"""Mechanical source/data integrity only; no numerical or scientific scoring."""
import argparse
import ast
import collections
import hashlib
import json
import resource
import time
from pathlib import Path

EXPECTED = {
    "Rice_Cammeo_Osmancik.arff": "745655b79f4ca46a3a65a0a8653bd792fa6f7c31",
    "Skin_NonSkin.txt": "fc58dda2eaf5b1f0d2d8c7924a298cd7d14ba17d",
}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--rice", required=True)
    p.add_argument("--skin", required=True)
    p.add_argument("--code", action="append", default=[])
    p.add_argument("--output", required=True)
    args = p.parse_args()
    start = time.perf_counter()
    sources = []
    for name, location in [("Rice_Cammeo_Osmancik.arff", args.rice), ("Skin_NonSkin.txt", args.skin)]:
        raw = Path(location).read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        if blob != EXPECTED[name]:
            raise ValueError("unmatched source bytes")
        lines = raw.decode("utf-8").splitlines()
        if name.endswith(".arff"):
            begin = next(i for i, s in enumerate(lines) if s.strip().upper() == "@DATA")
            rows = [s.split(",") for s in lines[begin + 1:] if s.strip() and not s.startswith("%")]
            width, count = 8, 3810
        else:
            rows = [s.split() for s in lines if s.strip()]
            width, count = 4, 245057
        if len(rows) != count or any(len(row) != width for row in rows):
            raise ValueError("released dimensions differ")
        sources.append({"name": name, "bytes": len(raw), "git_blob": blob,
                        "sha256": hashlib.sha256(raw).hexdigest(),
                        "rows": count, "feature_columns": width - 1,
                        "labels": dict(collections.Counter(row[-1].strip() for row in rows)),
                        "first3000_labels": dict(collections.Counter(row[-1].strip() for row in rows[:3000])),
                        "source_order": "unchanged released line order"})
    code = []
    for name in args.code:
        raw = Path(name).read_bytes()
        ast.parse(raw, filename=name)
        code.append({"path": name, "sha256": hashlib.sha256(raw).hexdigest(), "ast_parse": "completed_without_import_or_execution"})
    r = resource.getrusage(resource.RUSAGE_SELF)
    result = {"format": "mechanical-source-integrity-v1", "sources": sources, "code": code,
              "numerical_qualification": False, "scientific_gate_advanced": False,
              "usage": {"wall_seconds": time.perf_counter() - start,
                        "process_cpu_seconds": r.ru_utime + r.ru_stime, "max_rss_kib": r.ru_maxrss}}
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"output": str(out), "usage": result["usage"]}))


if __name__ == "__main__":
    main()
