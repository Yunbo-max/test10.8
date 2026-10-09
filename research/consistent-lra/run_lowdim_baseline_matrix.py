"""Run the frozen Rice/Skin developmental existing-baseline matrix.

Candidate only until independent source and exact plan review.  This wrapper
uses the already reviewed scorer/arms in native_baselines and losslessly packs
all raw per-prefix outputs into deterministic per-cohort archives.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import resource
import tarfile
import tempfile
import time
from pathlib import Path
from types import SimpleNamespace

import native_baselines


C_SENSITIVITY = (1.1, 2.0, 2.5, 5.0, 10.0, 100.0)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def cohort_configs(name: str, dataset: str, source: str, k: int, d: int):
    c_values = list(C_SENSITIVITY)
    if name == "skin-k2":
        c_values.insert(1, 1.5)
    configs = [dict(arm="algorithm4", c=c, interval=100, ell=2)
               for c in c_values]
    configs += [
        dict(arm="fresh", c=1.1, interval=100, ell=2),
        dict(arm="fixed", c=1.1, interval=100, ell=2),
        dict(arm="periodic", c=1.1, interval=10, ell=2),
        dict(arm="periodic", c=1.1, interval=100, ell=2),
    ]
    strong_ells = sorted({min(d, 2 * k), min(d, 4 * k)})
    configs += [dict(arm="fd", c=1.1, interval=100, ell=ell)
                for ell in strong_ells if k < ell <= d]
    configs += [dict(arm="author_fd", c=1.1, interval=100, ell=2)]
    if len(configs) != 13:
        raise ValueError(f"{name} expected 13 configurations, got {len(configs)}")
    return [dict(cohort=name, dataset=dataset, source=source, k=k, **cfg)
            for cfg in configs]


def slug(config: dict) -> str:
    arm = config["arm"]
    if arm == "algorithm4":
        parameter = "c" + str(config["c"]).replace(".", "p")
    elif arm == "periodic":
        parameter = f"interval{config['interval']}"
    elif arm in ("fd", "author_fd"):
        parameter = f"ell{config['ell']}"
    else:
        parameter = "default"
    return f"{arm}-{parameter}"


def deterministic_archive(output: Path, members: list[tuple[Path, str]]) -> str:
    with output.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as zipped:
            with tarfile.open(fileobj=zipped, mode="w", format=tarfile.PAX_FORMAT) as archive:
                for path, arcname in sorted(members, key=lambda item: item[1]):
                    data = path.read_bytes()
                    info = tarfile.TarInfo(arcname)
                    info.size = len(data)
                    info.mode = 0o644
                    info.mtime = 0
                    info.uid = info.gid = 0
                    info.uname = info.gname = ""
                    archive.addfile(info, io.BytesIO(data))
    return sha256(output)


def run(args) -> None:
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise FileExistsError(output)
    cohorts = [
        ("rice-k1", "rice", args.rice_source, 1, 7),
        ("skin-k1", "skin", args.skin_source, 1, 3),
        ("skin-k2", "skin", args.skin_source, 2, 3),
    ]
    start = time.perf_counter()
    before = resource.getrusage(resource.RUSAGE_SELF)
    manifest = {
        "format": "consistent-lra-lowdim-existing-baseline-matrix-v1",
        "scope": "developmental project-repair baseline qualification only",
        "cohorts": [],
        "scientific_gate_advanced": False,
        "performance_claim_eligible": False,
        "confirmation": False,
    }
    with tempfile.TemporaryDirectory(prefix="lowdim-matrix-", dir=output.parent) as temporary:
        temporary = Path(temporary)
        for cohort, dataset, source, k, d in cohorts:
            records = []
            members = []
            for config in cohort_configs(cohort, dataset, source, k, d):
                name = slug(config)
                raw = temporary / f"{cohort}__{name}.jsonl"
                native_args = SimpleNamespace(
                    dataset=dataset, source=source, arm=config["arm"], k=k,
                    c=config["c"], interval=config["interval"], ell=config["ell"],
                    seed=20261009, random_variant="released_code_unscaled",
                    output=str(raw),
                )
                native_baselines.run(native_args)
                summary_path = raw.with_suffix(".summary.json")
                summary = json.loads(summary_path.read_text(encoding="utf-8"))
                if summary["prefix_denominator"] != 3000:
                    raise ValueError(f"{cohort}/{name} incomplete prefixes")
                raw_hash = sha256(raw)
                if raw_hash != summary["raw_sha256"]:
                    raise ValueError(f"{cohort}/{name} raw hash mismatch")
                records.append({
                    "name": name,
                    "configuration": config,
                    "prefix_denominator": summary["prefix_denominator"],
                    "defined_ratio_denominator": summary["defined_ratio_denominator"],
                    "near_zero_opt_exclusions": summary["near_zero_opt_exclusions"],
                    "positive_loss_near_zero_opt_count": summary["positive_loss_near_zero_opt_count"],
                    "ratio_mean": summary["ratio_mean"],
                    "ratio_median": summary["ratio_median"],
                    "ratio_max": summary["ratio_max"],
                    "final_recourse": summary["final_recourse"],
                    "final_steady_recourse": summary["final_steady_recourse"],
                    "usage": summary["usage"],
                    "raw_member": raw.name,
                    "raw_sha256": raw_hash,
                    "summary_member": summary_path.name,
                    "summary_sha256": sha256(summary_path),
                })
                members.extend([(raw, raw.name), (summary_path, summary_path.name)])
            archive = output.parent / f"lowdim-{cohort}.tar.gz"
            if archive.exists():
                raise FileExistsError(archive)
            archive_hash = deterministic_archive(archive, members)
            manifest["cohorts"].append({
                "name": cohort,
                "dataset": dataset,
                "k": k,
                "dimension": d,
                "arm_count": len(records),
                "archive": archive.name,
                "archive_sha256": archive_hash,
                "records": records,
            })
    after = resource.getrusage(resource.RUSAGE_SELF)
    manifest["usage"] = {
        "wall_seconds": time.perf_counter() - start,
        "cpu_seconds": after.ru_utime + after.ru_stime - before.ru_utime - before.ru_stime,
        "max_rss_kib": after.ru_maxrss,
    }
    manifest["source_hashes"] = {
        "runner": sha256(Path(__file__)),
        "native_baselines.py": sha256(Path(native_baselines.__file__)),
    }
    if sum(item["arm_count"] for item in manifest["cohorts"]) != 39:
        raise ValueError("matrix must contain exactly 39 arms")
    output.write_text(json.dumps(manifest, allow_nan=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "usage": manifest["usage"],
                      "arms": 39, "scientific_gate_advanced": False}))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rice-source", required=True)
    parser.add_argument("--skin-source", required=True)
    parser.add_argument("--output", required=True)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
