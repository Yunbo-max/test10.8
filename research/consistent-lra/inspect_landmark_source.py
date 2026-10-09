"""Mechanical Landmark source integrity only; no numerical/scientific scoring."""

import argparse
import hashlib
import json
import math
import resource
import time
from pathlib import Path


EXPECTED = {
    "git_blob": "4c63060bbefcb38e0c705cea1f883d2fb7121f2c",
    "sha256": "29fb87018e59049a52314c847c5ac2a4eaa3b875f7cd8467621fe074fbbc298b",
    "rows": 71952,
    "columns": 2704,
    "pattern_entries": 1151232,
    "numeric_nonzeros": 1146848,
    "explicit_zeros": 4384,
}


def stream_hashes(path: Path):
    size = path.stat().st_size
    git_hash = hashlib.sha1()
    git_hash.update(b"blob " + str(size).encode("ascii") + b"\0")
    sha256 = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            git_hash.update(chunk)
            sha256.update(chunk)
    return size, git_hash.hexdigest(), sha256.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--landmark", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    start = time.perf_counter()
    source = Path(args.landmark)
    byte_count, git_blob, sha256 = stream_hashes(source)
    if git_blob != EXPECTED["git_blob"] or sha256 != EXPECTED["sha256"]:
        raise ValueError("Landmark source identity differs from the frozen author blob")

    metadata = []
    dimensions = None
    pattern_entries = 0
    numeric_nonzeros = 0
    explicit_zeros = 0
    first5000_entries = 0
    first5000_nonzeros = 0
    first5000_zeros = 0
    first5000_row_counts = [0] * 5000
    first5000_columns = set()
    previous_coordinate = None
    adjacent_duplicate_coordinates = 0
    coordinate_order_is_column_then_row = True

    with source.open("rt", encoding="utf-8") as handle:
        banner = handle.readline().rstrip("\n")
        if banner != "%%MatrixMarket matrix coordinate real general":
            raise ValueError("unexpected MatrixMarket banner")
        for line in handle:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("%"):
                metadata.append(stripped)
                continue
            if dimensions is None:
                fields = stripped.split()
                if len(fields) != 3:
                    raise ValueError("invalid MatrixMarket dimensions")
                dimensions = tuple(map(int, fields))
                continue
            fields = stripped.split()
            if len(fields) != 3:
                raise ValueError("invalid MatrixMarket coordinate")
            row = int(fields[0])
            column = int(fields[1])
            value = float(fields[2])
            if not (1 <= row <= dimensions[0] and 1 <= column <= dimensions[1]):
                raise ValueError("coordinate outside declared dimensions")
            if not math.isfinite(value):
                raise ValueError("non-finite MatrixMarket value")
            coordinate = (column, row)
            if previous_coordinate is not None:
                if coordinate < previous_coordinate:
                    coordinate_order_is_column_then_row = False
                if coordinate == previous_coordinate:
                    adjacent_duplicate_coordinates += 1
            previous_coordinate = coordinate
            pattern_entries += 1
            if value == 0.0:
                explicit_zeros += 1
            else:
                numeric_nonzeros += 1
            if row <= 5000:
                first5000_entries += 1
                first5000_row_counts[row - 1] += 1
                first5000_columns.add(column)
                if value == 0.0:
                    first5000_zeros += 1
                else:
                    first5000_nonzeros += 1

    if dimensions is None:
        raise ValueError("missing MatrixMarket dimensions")
    if dimensions != (EXPECTED["rows"], EXPECTED["columns"], EXPECTED["pattern_entries"]):
        raise ValueError("declared Landmark dimensions differ")
    if pattern_entries != EXPECTED["pattern_entries"]:
        raise ValueError("coordinate count differs")
    if numeric_nonzeros != EXPECTED["numeric_nonzeros"] or explicit_zeros != EXPECTED["explicit_zeros"]:
        raise ValueError("numeric/explicit-zero counts differ from official metadata")

    usage = resource.getrusage(resource.RUSAGE_SELF)
    result = {
        "format": "landmark-mechanical-source-integrity-v1",
        "source_identity": {
            "upstream": "samsonzhou/consistent-LRA@d607c4f6467216c470d1e3b93989d44d5fcdec97",
            "path": "landmark.mtx",
            "git_blob": git_blob,
            "sha256": sha256,
            "bytes": byte_count,
        },
        "matrix_market": {
            "banner": banner,
            "rows": dimensions[0],
            "columns": dimensions[1],
            "pattern_entries": pattern_entries,
            "numeric_nonzeros": numeric_nonzeros,
            "explicit_zeros": explicit_zeros,
            "metadata_lines": metadata,
            "coordinate_order_is_column_then_row": coordinate_order_is_column_then_row,
            "adjacent_duplicate_coordinates": adjacent_duplicate_coordinates,
        },
        "published_prefix": {
            "rows": 5000,
            "columns": dimensions[1],
            "pattern_entries": first5000_entries,
            "numeric_nonzeros": first5000_nonzeros,
            "explicit_zeros": first5000_zeros,
            "nonempty_rows": sum(count > 0 for count in first5000_row_counts),
            "nonempty_columns": len(first5000_columns),
            "minimum_pattern_entries_per_row": min(first5000_row_counts),
            "maximum_pattern_entries_per_row": max(first5000_row_counts),
            "source_order": "first 5000 released rows without reordering or value modification",
        },
        "official_metadata_counts_match": True,
        "numerical_qualification": False,
        "scientific_gate_advanced": False,
        "usage": {
            "wall_seconds": time.perf_counter() - start,
            "process_cpu_seconds": usage.ru_utime + usage.ru_stime,
            "max_rss_kib": usage.ru_maxrss,
        },
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "usage": result["usage"]}, allow_nan=False))


if __name__ == "__main__":
    main()
