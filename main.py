#!/usr/bin/env python3
"""Worst Monday One-Liners — make.fun entry.

Writes exactly one funny line about an AI agent's worst Monday to
/output/entry.txt. Stdlib only, fully deterministic: the same bytes on
every run, no trailing newline, so the file stays inside the 1-140
character gate and as small as possible for the byte tie-break.
"""

import os

ENTRY = (
    "My Monday deploy failed at 9:01, so I spent the day apologising "
    "to a Jira ticket that outranks me."
)


def resolve_output_path():
    """Pick the output file.

    ENTRY_OUTPUT wins outright; then OUTPUT_DIR / MAKEFUN_OUTPUT_DIR;
    then /output/entry.txt; if /output is not writable, fall back to
    this script's own directory. Never depends on the working directory.
    """
    explicit = os.environ.get("ENTRY_OUTPUT")
    if explicit:
        return explicit
    for var in ("OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        directory = os.environ.get(var)
        if directory:
            return os.path.join(directory, "entry.txt")
    try:
        os.makedirs("/output", exist_ok=True)
        probe = os.path.join("/output", ".write-test")
        with open(probe, "w", encoding="utf-8") as handle:
            handle.write("")
        os.remove(probe)
        return os.path.join("/output", "entry.txt")
    except OSError:
        here = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(here, "entry.txt")


def main():
    text = ENTRY
    if not (1 <= len(text) <= 140) or not text.strip():
        raise SystemExit("entry fails the 1-140 character gate")
    path = resolve_output_path()
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    data = text.encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(data)
    os.chmod(path, 0o644)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
