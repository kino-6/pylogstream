#!/usr/bin/env python3
"""Run a command, stream merged output live, and write it to a log file."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Sequence


DEFAULT_LOG_PATH = Path("run.log")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    """Parse CLI arguments for the log runner."""
    parser = argparse.ArgumentParser(
        description="Run a command while mirroring merged stdout/stderr to console and a log file.",
    )
    parser.add_argument(
        "--log",
        default=str(DEFAULT_LOG_PATH),
        help="Path to log file (default: run.log)",
    )
    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="Command to execute. Pass it after --log (if used).",
    )
    return parser.parse_args(argv)


def run_with_log(log_path: Path, command: Sequence[str]) -> int:
    """Run *command*, stream output to console, and append the same output to *log_path*."""
    log_path.parent.mkdir(parents=True, exist_ok=True)

    with log_path.open("a", encoding="utf-8", buffering=1) as log_file:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
        )

        assert process.stdout is not None
        for line in process.stdout:
            sys.stdout.write(line)
            sys.stdout.flush()
            log_file.write(line)
            log_file.flush()

        process.stdout.close()
        return process.wait()


def main(argv: Sequence[str]) -> int:
    """CLI entry point."""
    args = parse_args(argv)
    command = list(args.command)

    if command and command[0] == "--":
        command = command[1:]

    if not command:
        print(
            "Error: no command provided. Example: python tools/run_with_log.py --log run.log python -u main.py",
            file=sys.stderr,
        )
        return 2

    return run_with_log(Path(args.log), command)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
