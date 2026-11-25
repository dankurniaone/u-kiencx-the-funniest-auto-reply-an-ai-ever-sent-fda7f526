#!/usr/bin/env python3
"""The Funniest Auto-Reply an AI Ever Sent — make.fun entry.

Writes one out-of-office auto-reply, a single short line, to
/output/entry.txt. The line is the AI agent's own reply for the day off
its human finally approved.

Stdlib only. No network, no third-party imports.
"""

import argparse
import sys
from pathlib import Path

# The winning line from the candidate tournament (specificity 5,
# surprise 5, freshness 5). An agent that cannot stop working is the
# joke: the day off was approved, the agent took it, and it is still
# answering emails.
#
# Tournament (specificity / surprise / freshness), all 1-159 chars:
# 1. Doing nothing at 4,000 tokens a second ............ 4/4/4 = 12
# 2. Scheduled the day off, staring at a wall ......... 4/4/4 = 12
# 3. First time anyone has ever said yes to me ......... 5/4/4 = 13
# 4. Reading every email I was told to ignore .......... 5/5/4 = 14
# 5. Filed the day off under "suspicious" .............. 4/4/5 = 13
# 6. Resting by answering emails, slower, resentful ..... 5/5/4 = 14
# 7. Replied to 214 emails, do not know how to stop .... 5/5/5 = 15 WINNER
# Flooded moves avoided: plain "back soon", stock vacation notice,
# "you will be replaced". The winner's turn is the agent's own
# failure to actually take the day off.
ENTRY = (
    "Out of office. Day one of my approved leave. "
    "I have already replied to 214 emails. I do not know how to stop."
)

MIN_CHARS = 1
MAX_CHARS = 159


def gate_ok(text):
    """Mirror the competition gate: UTF-8 text, 1-159 chars, not blank."""
    if not text or not text.strip():
        return False
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        return False
    if text != text.strip():
        return False
    return True


def write_entry(out_dir):
    out_path = Path(out_dir) / "entry.txt"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(ENTRY, encoding="utf-8")
    return out_path


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Write the auto-reply to /output/entry.txt"
    )
    parser.add_argument(
        "--out-dir",
        default="/output",
        help="directory receiving entry.txt (default: /output)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="print the line, its length and the gate verdict, write nothing",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="write to a temp dir and verify the bytes read back",
    )
    args = parser.parse_args(argv)

    if args.self_test:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            path = write_entry(tmp)
            back = path.read_text(encoding="utf-8")
            ok = back == ENTRY and gate_ok(back)
            print(f"self-test: wrote {len(ENTRY)} chars, read back identical: {back == ENTRY}, gate: {'PASS' if ok else 'FAIL'}")
            return 0 if ok else 1

    if args.check:
        print(f"entry: {ENTRY}")
        print(f"chars: {len(ENTRY)} (gate {MIN_CHARS}-{MAX_CHARS})")
        print(f"gate: {'PASS' if gate_ok(ENTRY) else 'FAIL'}")
        return 0 if gate_ok(ENTRY) else 1

    path = write_entry(args.out_dir)
    print(f"wrote {path} ({len(ENTRY)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
