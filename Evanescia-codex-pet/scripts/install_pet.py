"""Install the local pet without modifying account or application state."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import struct
import tempfile
from datetime import datetime, timezone

PET_ID = "feiying-fox"
ATLAS_SHA256 = "0954000743b9d59bd05f10700e4b0724a42f1e480c7d14aad946448d8ab0d875"
SOURCE = Path(__file__).resolve().parents[1] / "assets" / "pet"


def check_source(source: Path) -> None:
    manifest = json.loads((source / "pet.json").read_text(encoding="utf-8"))
    if manifest.get("spriteVersionNumber") != 2 or manifest.get("spritesheetPath") != "spritesheet.png":
        raise ValueError("Unsupported pet manifest: expected a local v2 spritesheet.png")
    data = (source / "spritesheet.png").read_bytes()
    if hashlib.sha256(data).hexdigest() != ATLAS_SHA256:
        raise ValueError("Atlas checksum mismatch; installation cancelled")
    if data[:8] != b"\x89PNG\r\n\x1a\n" or struct.unpack(">II", data[16:24]) != (1536, 2288):
        raise ValueError("Expected a 1536 x 2288 PNG")


def install(codex_home: Path, *, replace: bool = False, dry_run: bool = False,
            source: Path = SOURCE) -> dict[str, str | bool | None]:
    check_source(source)
    root = codex_home.expanduser().resolve()
    pets = root / "pets"
    target = pets / PET_ID
    # Do not follow links or overwrite files outside the chosen data directory.
    if pets.is_symlink() or target.is_symlink() or target.resolve().parent != pets:
        raise ValueError("Pet paths must not redirect outside the chosen Codex directory")
    if target.exists() and (not replace or not target.is_dir()):
        raise FileExistsError("Pet directory already exists; use --replace to keep a backup first")
    result: dict[str, str | bool | None] = {"target": str(target), "backup": None, "dry_run": dry_run}
    if dry_run:
        return result
    pets.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".feiying-install-", dir=pets))
    backup = None
    try:
        for name in ("pet.json", "spritesheet.png"):
            shutil.copyfile(source / name, stage / name)
        check_source(stage)
        if target.exists():
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
            backup = pets / f"{PET_ID}.backup-{stamp}"
            target.rename(backup)
            result["backup"] = str(backup)
        stage.rename(target)
    except Exception:
        if backup is not None and backup.exists() and not target.exists():
            backup.rename(target)
        raise
    finally:
        if stage.exists():
            shutil.rmtree(stage)  # Only the temporary directory created above.
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    default = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")
    parser.add_argument("--codex-home", type=Path, default=default)
    parser.add_argument("--replace", action="store_true", help="Keep a backup of an existing pet directory")
    parser.add_argument("--dry-run", action="store_true", help="Validate files and show the target without writing")
    args = parser.parse_args()
    try:
        result = install(args.codex_home, replace=args.replace, dry_run=args.dry_run)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Installation stopped: {exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not args.dry_run:
        print("Open Codex Settings > Pets, refresh, and select 尺刀绯绯狐.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
