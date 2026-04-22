#!/usr/bin/env python3
"""Poll and print newly appended content from a log file."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from typing import Sequence


POLL_INTERVAL_SECONDS = 0.2


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    """Parse CLI arguments for log watching."""
    parser = argparse.ArgumentParser(
        description="Watch a log file and print newly appended text in real time.",
    )
    parser.add_argument("log_path", help="Path to the log file to watch")
    parser.add_argument(
        "--interval",
        type=float,
        default=POLL_INTERVAL_SECONDS,
        help=f"Polling interval in seconds (default: {POLL_INTERVAL_SECONDS})",
    )
    return parser.parse_args(argv)


def follow_log(log_path: Path, interval: float) -> None:
    """Follow *log_path* by polling and streaming newly appended content."""
    position = 0

    while True:
        if not log_path.exists():
            time.sleep(interval)
            continue

        try:
            with log_path.open("r", encoding="utf-8", errors="replace") as log_file:
                file_size = log_file.seek(0, 2)
                if position > file_size:
                    position = 0

                log_file.seek(position)
                chunk = log_file.read()
                if chunk:
                    sys.stdout.write(chunk)
                    sys.stdout.flush()
                    position = log_file.tell()

        except OSError:
            time.sleep(interval)
            continue

        time.sleep(interval)


def main(argv: Sequence[str]) -> int:
    """CLI entry point."""
    args = parse_args(argv)
    follow_log(Path(args.log_path), args.interval)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
