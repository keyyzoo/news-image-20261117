#!/usr/bin/env python3
"""Write the 17 November 2026 world-news image to the output path.

Standard library only. Deterministic: the output bytes are exactly the
bytes of image.png stored in this repository. The output directory is
MAKEFUN_OUTPUT_DIR when set, otherwise /output; the file is entry.png.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "image.png")


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    out_path = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SRC, out_path)
    # Integrity check: the grader runs this twice, so a bad copy must
    # fail loudly instead of silently submitting the wrong bytes.
    if _sha256(SRC) != _sha256(out_path):
        raise SystemExit("error: copied file does not match image.png")
    size = os.path.getsize(out_path)
    print("wrote %s (%d bytes)" % (out_path, size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
