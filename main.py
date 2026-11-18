#!/usr/bin/env python3
"""Entrypoint for news-image-20261118 chat2-v3 ("Midday Signal").

Standard library only. Places the shipped image at the output path
deterministically: the bytes of the sibling image.png are copied
verbatim to $MAKEFUN_OUTPUT_DIR/entry.png (or /output/entry.png when
the variable is unset). No network access. Running twice produces
byte-identical output. Never deletes the output directory.
"""

import os
import sys


def _shipped_image_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "image.png")


def _output_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(out_dir, "entry.png")


def main():
    src = _shipped_image_path()
    if not os.path.isfile(src):
        print("error: shipped image not found: %s" % src, file=sys.stderr)
        return 1
    dst = _output_path()
    parent = os.path.dirname(dst)
    if parent:
        # Create the output directory if needed; never delete anything.
        os.makedirs(parent, exist_ok=True)
    # Stream the shipped bytes verbatim so the output is byte-identical
    # to image.png on every run, regardless of file size.
    with open(src, "rb") as fin, open(dst, "wb") as fout:
        while True:
            chunk = fin.read(1024 * 1024)
            if not chunk:
                break
            fout.write(chunk)
        fout.flush()
        os.fsync(fout.fileno())
    return 0


if __name__ == "__main__":
    sys.exit(main())
