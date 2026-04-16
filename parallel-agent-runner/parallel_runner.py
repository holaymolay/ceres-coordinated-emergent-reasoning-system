#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import List, Optional


def run_cmd(cmd: str) -> dict:
    start = datetime.utcnow().isoformat() + 'Z'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = proc.communicate()
    end = datetime.utcnow().isoformat() + 'Z'
    return {
        "cmd": cmd,
        "returncode": proc.returncode,
        "stdout": stdout,
        "stderr": stderr,
        "start": start,
        "end": end,
    }


def log_entry(entry: dict, log_file: Optional[Path]) -> None:
    if log_file:
        with log_file.open("a") as f:
            f.write(json.dumps(entry) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="CERES parallel agent runner")
    parser.add_argument("--cmd", action="append", required=True, help="Command to run (repeatable)")
    parser.add_argument("--concurrency", type=int, default=2, help="Max parallel commands")
    parser.add_argument("--log-file", type=Path, help="Optional JSONL log file")
    args = parser.parse_args()

    cmds: List[str] = args.cmd
    results = []
    failed = False

    with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        future_to_cmd = {executor.submit(run_cmd, cmd): cmd for cmd in cmds}
        for future in as_completed(future_to_cmd):
            res = future.result()
            results.append(res)
            log_entry(res, args.log_file)
            sys.stdout.write(f"\n=== CMD: {res['cmd']}\n")
            sys.stdout.write(res["stdout"])
            if res["stderr"]:
                sys.stderr.write(res["stderr"])
            if res["returncode"] != 0:
                failed = True

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
