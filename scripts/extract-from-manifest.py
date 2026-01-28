#!/usr/bin/env python3
"""Extract a subset of a tarball based on a manifest JSON."""

from __future__ import annotations

import argparse
import json
import tarfile
from pathlib import Path


def load_manifest(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    paths = data.get("paths", [])
    return [p.strip("/") for p in paths if isinstance(p, str)]


def safe_member_name(name: str, prefix: str) -> str | None:
    if not name.startswith(prefix):
        return None
    rel = name[len(prefix) :].lstrip("/")
    if not rel or rel.startswith("..") or "/.." in rel:
        return None
    return rel


def extract_from_tar(tar_path: Path, manifest: list[str], dest: Path) -> None:
    with tarfile.open(tar_path, "r:*") as tar:
        members = tar.getmembers()
        if not members:
            raise SystemExit("Tarball is empty.")
        root_prefix = members[0].name.split("/")[0]
        prefix = root_prefix + "/"

        allowed = set(manifest)
        for member in members:
            rel = safe_member_name(member.name, prefix)
            if rel is None:
                continue
            top = rel.split("/", 1)[0]
            if top in allowed or rel in allowed:
                member.name = rel
                tar.extract(member, path=dest)


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract tarball paths listed in a manifest JSON.")
    parser.add_argument("tarball", help="Path to tar.gz")
    parser.add_argument("manifest", help="Path to manifest JSON (local file)")
    parser.add_argument("dest", help="Destination directory")
    args = parser.parse_args()

    tar_path = Path(args.tarball)
    manifest_path = Path(args.manifest)
    dest = Path(args.dest)
    if not tar_path.exists():
        raise SystemExit(f"Tarball not found: {tar_path}")
    if not manifest_path.exists():
        raise SystemExit(f"Manifest not found: {manifest_path}")
    dest.mkdir(parents=True, exist_ok=True)

    manifest = load_manifest(manifest_path)
    if not manifest:
        raise SystemExit("Manifest is empty.")
    extract_from_tar(tar_path, manifest, dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
