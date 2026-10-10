"""Versioned atomic NPZ persistence with durability and command-local validation."""
import hashlib
import os
from pathlib import Path
import uuid
import zipfile
import json

import numpy as np


def atomic_write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(value, indent=2, allow_nan=False, sort_keys=True) + "\n").encode()
    temporary = path.with_name(f".{path.name}.tmp-{uuid.uuid4().hex}")
    descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if temporary.exists():
            temporary.unlink()


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def validate_npz(path, required_keys):
    path = Path(path)
    with zipfile.ZipFile(path, "r") as archive:
        bad_member = archive.testzip()
        if bad_member is not None:
            raise RuntimeError(f"NPZ CRC failure: {bad_member}")
    with np.load(path, allow_pickle=False) as arrays:
        missing = sorted(set(required_keys) - set(arrays.files))
        if missing:
            raise RuntimeError(f"NPZ missing keys: {missing}")
        inventory = {key: {"shape": list(arrays[key].shape), "dtype": str(arrays[key].dtype)} for key in arrays.files}
    return {"zip_crc_pass": True, "np_load_pass": True, "inventory": inventory, "sha256": sha256(path), "size_bytes": path.stat().st_size}


def atomic_savez(path, arrays, required_keys):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(f"versioned output already exists: {path}")
    temporary = path.with_name(f".{path.name}.tmp-{uuid.uuid4().hex}.npz")
    try:
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "wb") as handle:
            np.savez_compressed(handle, **arrays)
            handle.flush()
            os.fsync(handle.fileno())
        temporary_validation = validate_npz(temporary, required_keys)
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
        final_validation = validate_npz(path, required_keys)
        if final_validation["sha256"] != temporary_validation["sha256"]:
            raise RuntimeError("hash changed across atomic replacement")
        return final_validation
    finally:
        if temporary.exists():
            temporary.unlink()
