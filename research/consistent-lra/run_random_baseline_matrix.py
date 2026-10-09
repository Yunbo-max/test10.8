"""Run a prospective seeded instance of the released Appendix-G random family.

This is a source-review candidate, not an admitted queue.  The original figure
stream is unseeded and irrecoverable; this runner therefore labels seed
20261009 as a new development instance and never as a paper reproduction.
It reuses the already reviewed arm/scorer implementation and the terminal
no-replace publication helpers from the Rice/Skin runner.
"""
from __future__ import annotations

import argparse
import json
import os
import resource
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import baseline_qualify
import native_baselines
import numpy
import run_lowdim_baseline_matrix as publication
import scipy
import sklearn


SEED = 20261009
COHORT = "random-seed20261009-k1"


def run(args) -> None:
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    archive = output.parent / f"{COHORT}.tar.gz"
    staging = output.parent / "random-matrix-raw-v1"
    final_paths = [output, archive]
    partial_paths = [path.with_name(path.name + ".partial") for path in final_paths]
    candidates = [*final_paths, *partial_paths, staging]
    if len({path.resolve() for path in candidates}) != len(candidates):
        raise ValueError("manifest, archive, partials and staging must be distinct")
    occupied = [str(path) for path in candidates if path.exists()]
    if occupied:
        raise FileExistsError("output path already exists: " + ", ".join(occupied))

    thread_names = ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
                    "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")
    thread_environment = {name: os.environ.get(name) for name in thread_names}
    if any(value != "1" for value in thread_environment.values()):
        raise ValueError("all numerical thread environment variables must equal 1")

    configs = publication.cohort_configs(COHORT, "random", "", 1, 4)
    if len(configs) != 13:
        raise ValueError("prospective random matrix must contain exactly 13 arms")
    start = time.perf_counter()
    before = resource.getrusage(resource.RUSAGE_SELF)
    staging.mkdir(parents=False, exist_ok=False)
    publication.fsync_directory(output.parent)
    records = []
    members = []
    published_members = []
    cohort_identity = None
    identity_keys = ("dataset", "generator_blob", "generator", "seed",
                     "denominator", "preprocessing", "matrix_sha256",
                     "original_figure_replication")

    for config in configs:
        name = publication.slug(config)
        raw = staging / f"{COHORT}__{name}.jsonl"
        working_raw = staging / f".partial-{COHORT}__{name}.jsonl"
        native_args = SimpleNamespace(
            dataset="random", source="", arm=config["arm"], k=1,
            c=config["c"], interval=config["interval"], ell=config["ell"],
            seed=SEED, random_variant="released_code_unscaled",
            output=str(working_raw),
        )
        native_baselines.run(native_args)
        working_summary = working_raw.with_suffix(".summary.json")
        summary_path = raw.with_suffix(".summary.json")
        publication.fsync_file(working_raw)
        publication.fsync_file(working_summary)
        summary = json.loads(working_summary.read_text(encoding="utf-8"))
        if summary["prefix_denominator"] != 3000:
            raise ValueError(f"{name} incomplete prefixes")
        identity = {key: summary["native"][key] for key in identity_keys}
        if identity["seed"] != SEED or identity["original_figure_replication"] is not False:
            raise ValueError("random identity or non-replication label drift")
        if cohort_identity is None:
            cohort_identity = identity
        elif identity != cohort_identity:
            raise ValueError(f"{name} random identity drift")
        raw_hash = publication.sha256(working_raw)
        if raw_hash != summary["raw_sha256"]:
            raise ValueError(f"{name} raw hash mismatch")
        summary_hash = publication.sha256(working_summary)
        publication.publish_no_replace(working_raw, raw)
        publication.publish_no_replace(working_summary, summary_path)
        if publication.sha256(raw) != raw_hash or publication.sha256(summary_path) != summary_hash:
            raise ValueError(f"{name} final publication mismatch")
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
            "summary_sha256": summary_hash,
        })
        members.extend([(raw, raw.name), (summary_path, summary_path.name)])
        published_members.extend([raw, summary_path])

    publication.fsync_directory(staging)
    archive_hash = publication.deterministic_archive(archive, members)
    after = resource.getrusage(resource.RUSAGE_SELF)
    manifest = {
        "format": "consistent-lra-prospective-random-baseline-matrix-v1",
        "scope": "developmental prospective seeded family instance only",
        "original_figure_replication": False,
        "cohort": COHORT,
        "native_identity": cohort_identity,
        "arm_count": len(records),
        "archive": archive.name,
        "archive_sha256": archive_hash,
        "records": records,
        "scientific_gate_advanced": False,
        "performance_claim_eligible": False,
        "confirmation": False,
        "rss_semantics": "per-arm ru_maxrss is cumulative process high-water mark",
        "argv": sys.argv,
        "thread_environment": thread_environment,
        "environment": {"python": sys.version, "numpy": numpy.__version__,
                        "scipy": scipy.__version__, "sklearn": sklearn.__version__},
        "usage": {"wall_seconds": time.perf_counter() - start,
                  "cpu_seconds": after.ru_utime + after.ru_stime - before.ru_utime - before.ru_stime,
                  "max_rss_kib": after.ru_maxrss},
        "source_hashes": {"runner": publication.sha256(Path(__file__)),
                          "publication_helpers": publication.sha256(Path(publication.__file__)),
                          "native_baselines.py": publication.sha256(Path(native_baselines.__file__)),
                          "baseline_qualify.py": publication.sha256(Path(baseline_qualify.__file__))},
    }
    expected_hashes = {archive.name: archive_hash}
    for record in records:
        expected_hashes[f"{staging.name}/{record['raw_member']}"] = record["raw_sha256"]
        expected_hashes[f"{staging.name}/{record['summary_member']}"] = record["summary_sha256"]
    observations = {}
    for path in [archive, *published_members]:
        relative = path.relative_to(output.parent).as_posix()
        status = path.stat()
        observations[relative] = {"sha256": publication.sha256(path),
                                  "bytes": status.st_size, "inode": status.st_ino,
                                  "mtime_ns": status.st_mtime_ns, "ctime_ns": status.st_ctime_ns}
    if set(observations) != set(expected_hashes):
        raise ValueError("publication inventory differs from expectation")
    if any(observations[path]["sha256"] != digest for path, digest in expected_hashes.items()):
        raise ValueError("published bytes changed before manifest publication")
    manifest["publication_observations"] = observations
    partial_manifest = output.with_name(output.name + ".partial")
    with partial_manifest.open("x", encoding="utf-8") as stream:
        json.dump(manifest, stream, allow_nan=False, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    publication.publish_no_replace(partial_manifest, output)
    print(json.dumps({"output": str(output), "usage": manifest["usage"],
                      "arms": 13, "original_figure_replication": False,
                      "scientific_gate_advanced": False}))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
