"""Run the frozen Rice/Skin developmental existing-baseline matrix.

Candidate only until independent source and exact plan review.  This wrapper
uses the already reviewed scorer/arms in native_baselines and losslessly packs
all raw per-prefix outputs into deterministic per-cohort archives.  Raw staging
is intentionally retained: the first execution demonstrated that deleting a
mutable staging tree could race the surrounding evidence collector.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import resource
import sys
import tarfile
import time
from pathlib import Path
from types import SimpleNamespace

import native_baselines
import baseline_qualify
import numpy
import scipy
import sklearn


C_SENSITIVITY = (1.1, 2.0, 2.5, 5.0, 10.0, 100.0)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fsync_file(path: Path) -> None:
    with path.open("rb") as stream:
        os.fsync(stream.fileno())


def fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


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
    partial = output.with_name(output.name + ".partial")
    with partial.open("xb") as raw:
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
        raw.flush()
        os.fsync(raw.fileno())
    expected = {arcname: sha256(path) for path, arcname in members}
    observed = {}
    with tarfile.open(partial, mode="r:gz") as archive:
        for member in archive.getmembers():
            if not member.isfile() or member.name in observed:
                raise ValueError("archive contains a non-file or duplicate member")
            extracted = archive.extractfile(member)
            if extracted is None:
                raise ValueError(f"archive member unavailable: {member.name}")
            observed[member.name] = hashlib.sha256(extracted.read()).hexdigest()
    if observed != expected:
        raise ValueError(f"archive verification failed for {output.name}")
    os.replace(partial, output)
    fsync_directory(output.parent)
    return sha256(output)


def run(args) -> None:
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    cohorts = [
        ("rice-k1", "rice", args.rice_source, 1, 7),
        ("skin-k1", "skin", args.skin_source, 1, 3),
        ("skin-k2", "skin", args.skin_source, 2, 3),
    ]
    archive_paths = {name: output.parent / f"lowdim-{name}.tar.gz"
                     for name, _, _, _, _ in cohorts}
    staging = output.parent / "lowdim-matrix-raw-v2"
    final_paths = [output, *archive_paths.values()]
    resolved = [path.resolve() for path in final_paths]
    if len(set(resolved)) != len(resolved):
        raise ValueError("manifest and archive output paths must be distinct")
    occupied = [str(path) for path in final_paths if path.exists()]
    occupied += [str(path) for path in archive_paths.values()
                 if path.with_name(path.name + ".partial").exists()]
    if staging.exists():
        occupied.append(str(staging))
    if occupied:
        raise FileExistsError("final output path already exists: " + ", ".join(occupied))
    thread_names = ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
                    "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")
    thread_environment = {name: os.environ.get(name) for name in thread_names}
    if any(value != "1" for value in thread_environment.values()):
        raise ValueError("all numerical thread environment variables must equal 1")
    start = time.perf_counter()
    before = resource.getrusage(resource.RUSAGE_SELF)
    manifest = {
        "format": "consistent-lra-lowdim-existing-baseline-matrix-v2",
        "scope": "developmental project-repair baseline qualification only",
        "cohorts": [],
        "scientific_gate_advanced": False,
        "performance_claim_eligible": False,
        "confirmation": False,
        "rss_semantics": "per-arm ru_maxrss is cumulative process high-water mark, not an independent arm peak",
        "argv": sys.argv,
        "thread_environment": thread_environment,
        "environment": {
            "python": sys.version,
            "numpy": numpy.__version__,
            "scipy": scipy.__version__,
            "sklearn": sklearn.__version__,
        },
    }
    staging.mkdir(parents=False, exist_ok=False)
    fsync_directory(output.parent)
    for cohort, dataset, source, k, d in cohorts:
        records = []
        members = []
        cohort_identity = None
        for config in cohort_configs(cohort, dataset, source, k, d):
            name = slug(config)
            raw = staging / f"{cohort}__{name}.jsonl"
            native_args = SimpleNamespace(
                dataset=dataset, source=source, arm=config["arm"], k=k,
                c=config["c"], interval=config["interval"], ell=config["ell"],
                seed=20261009, random_variant="released_code_unscaled",
                output=str(raw),
            )
            native_baselines.run(native_args)
            summary_path = raw.with_suffix(".summary.json")
            fsync_file(raw)
            fsync_file(summary_path)
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            if summary["prefix_denominator"] != 3000:
                raise ValueError(f"{cohort}/{name} incomplete prefixes")
            identity_keys = ("dataset", "source_blob", "source_sha256", "source_bytes",
                             "released_shape", "denominator", "preprocessing",
                             "transformed_sha256", "labels_sha256",
                             "first3000_label_counts", "mean", "scale")
            identity = {key: summary["native"][key] for key in identity_keys}
            if cohort_identity is None:
                cohort_identity = identity
            elif identity != cohort_identity:
                raise ValueError(f"{cohort}/{name} native identity drift")
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
        fsync_directory(staging)
        archive = archive_paths[cohort]
        archive_hash = deterministic_archive(archive, members)
        manifest["cohorts"].append({
            "name": cohort,
            "dataset": dataset,
            "k": k,
            "dimension": d,
            "native_identity": cohort_identity,
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
        "baseline_qualify.py": sha256(Path(baseline_qualify.__file__)),
    }
    if sum(item["arm_count"] for item in manifest["cohorts"]) != 39:
        raise ValueError("matrix must contain exactly 39 arms")
    for cohort in manifest["cohorts"]:
        for record in cohort["records"]:
            raw = staging / record["raw_member"]
            summary = staging / record["summary_member"]
            if sha256(raw) != record["raw_sha256"] or sha256(summary) != record["summary_sha256"]:
                raise ValueError("retained member changed before manifest publication")
    tracked_paths = [*archive_paths.values(), *sorted(staging.iterdir())]
    manifest["publication_observations"] = {
        path.relative_to(output.parent).as_posix(): {
            "sha256": sha256(path),
            "bytes": path.stat().st_size,
            "inode": path.stat().st_ino,
            "mtime_ns": path.stat().st_mtime_ns,
            "ctime_ns": path.stat().st_ctime_ns,
        }
        for path in tracked_paths
    }
    partial_manifest = output.with_name(output.name + ".partial")
    with partial_manifest.open("x", encoding="utf-8") as stream:
        json.dump(manifest, stream, allow_nan=False, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(partial_manifest, output)
    fsync_directory(output.parent)
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
