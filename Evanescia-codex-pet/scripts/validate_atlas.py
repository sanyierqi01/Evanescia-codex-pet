"""Verify published atlas structure, transparency and checksum."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image

FRAME_COUNTS = [6, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8]
EXPECTED_SHA256 = "0954000743b9d59bd05f10700e4b0724a42f1e480c7d14aad946448d8ab0d875"
DEFAULT_ATLAS = Path(__file__).resolve().parents[1] / "assets" / "pet" / "spritesheet.png"


def validate(path: Path, *, check_digest: bool = True) -> dict:
    errors = []
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    with Image.open(path) as img:
        if img.size != (1536, 2288):
            errors.append("Expected size 1536 x 2288")
        if img.mode != "RGBA":
            errors.append("Expected RGBA PNG")
        if not errors:
            alpha = img.getchannel("A")
            for row, count in enumerate(FRAME_COUNTS):
                for col in range(8):
                    cell = alpha.crop((col * 192, row * 208, (col + 1) * 192, (row + 1) * 208))
                    has_pixels = cell.getbbox() is not None
                    if has_pixels != (col < count):
                        errors.append(f"Unexpected transparency at row {row}, column {col}")
            if alpha.getextrema()[0] != 0:
                errors.append("Atlas has no transparent background")
    if check_digest and digest != EXPECTED_SHA256:
        errors.append("Checksum differs from the reviewed release atlas")
    return {"ok": not errors, "sha256": digest, "frames": sum(FRAME_COUNTS), "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("atlas", nargs="?", type=Path, default=DEFAULT_ATLAS)
    parser.add_argument("--allow-modified", action="store_true", help="Check structure without matching release SHA")
    args = parser.parse_args()
    result = validate(args.atlas, check_digest=not args.allow_modified)
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
