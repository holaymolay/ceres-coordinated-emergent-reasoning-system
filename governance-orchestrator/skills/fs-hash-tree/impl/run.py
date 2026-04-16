#!/usr/bin/env python3

from __future__ import annotations

import fnmatch
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any


def eprint_json(event: str, payload: dict[str, Any]) -> None:
    sys.stderr.write(json.dumps({"event": event, **payload}, separators=(",", ":"), sort_keys=True) + "\n")


def sha_file(path: Path, algorithm: str) -> str:
    hasher = hashlib.new(algorithm)
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def matches_any(path_posix: str, patterns: list[str]) -> bool:
    for pattern in patterns:
        if fnmatch.fnmatch(path_posix, pattern):
            return True
    return False


def main() -> int:
    try:
        input_obj = json.load(sys.stdin)
        if not isinstance(input_obj, dict):
            raise ValueError("input must be a JSON object")
        root_raw = input_obj.get("root")
        if not isinstance(root_raw, str) or not root_raw:
            raise ValueError("root must be a non-empty string")

        algorithm = input_obj.get("algorithm", "sha256")
        if algorithm not in {"sha256", "sha1", "md5"}:
            raise ValueError("algorithm must be one of: sha256, sha1, md5")

        exclude = input_obj.get("exclude", [])
        if exclude is None:
            exclude = []
        if not isinstance(exclude, list) or any(not isinstance(p, str) or not p for p in exclude):
            raise ValueError("exclude must be an array of non-empty strings")

        root_path = Path(root_raw).resolve()
        if not root_path.exists() or not root_path.is_dir():
            raise ValueError("root must be an existing directory")

        files: list[dict[str, Any]] = []
        for dirpath, dirnames, filenames in os.walk(root_path, topdown=True, followlinks=False):
            dir_path = Path(dirpath)
            rel_dir = dir_path.relative_to(root_path).as_posix()
            if rel_dir == ".":
                rel_dir = ""

            dirnames.sort()
            filenames.sort()

            pruned_dirnames = []
            for d in dirnames:
                rel = f"{rel_dir}/{d}" if rel_dir else d
                if matches_any(rel, exclude):
                    continue
                pruned_dirnames.append(d)
            dirnames[:] = pruned_dirnames

            for filename in filenames:
                file_path = dir_path / filename
                if file_path.is_symlink() or not file_path.is_file():
                    continue
                rel = f"{rel_dir}/{filename}" if rel_dir else filename
                if matches_any(rel, exclude):
                    continue
                digest = sha_file(file_path, algorithm)
                size = file_path.stat().st_size
                files.append({"path": rel, "digest": digest, "size": size})

        files.sort(key=lambda x: x["path"])
        tree_hasher = hashlib.new(algorithm)
        for entry in files:
            tree_hasher.update(entry["path"].encode("utf-8"))
            tree_hasher.update(b"\0")
            tree_hasher.update(entry["digest"].encode("ascii"))
            tree_hasher.update(b"\0")

        output = {
            "algorithm": algorithm,
            "root": str(root_path),
            "treeDigest": tree_hasher.hexdigest(),
            "fileCount": len(files),
            "files": files,
        }
        sys.stdout.write(json.dumps(output, separators=(",", ":"), sort_keys=True) + "\n")
        return 0
    except Exception as e:
        eprint_json("error", {"message": str(e)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

