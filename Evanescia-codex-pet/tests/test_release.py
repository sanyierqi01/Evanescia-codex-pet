import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image

from scripts.install_pet import SOURCE, install
from scripts.validate_atlas import DEFAULT_ATLAS, validate


class ReleaseTests(unittest.TestCase):
    def test_reviewed_atlas(self):
        self.assertEqual(validate(DEFAULT_ATLAS)["errors"], [])

    def test_missing_frame_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "missing.png"
            with Image.open(DEFAULT_ATLAS) as img:
                img.paste((0, 0, 0, 0), (0, 0, 192, 208))
                img.save(path)
            result = validate(path, check_digest=False)
            self.assertFalse(result["ok"])
            self.assertIn("row 0, column 0", result["errors"][0])

    def test_install_dry_run_and_backup(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "codex-data"
            install(home, dry_run=True)
            self.assertFalse(home.exists())
            result = install(home)
            target = Path(result["target"])
            self.assertEqual((target / "spritesheet.png").read_bytes(), (SOURCE / "spritesheet.png").read_bytes())
            marker = target / "existing-user-file.txt"
            marker.write_text("keep me", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                install(home)
            result = install(home, replace=True)
            self.assertEqual((Path(result["backup"]) / marker.name).read_text(), "keep me")
            self.assertEqual(sorted(p.name for p in target.iterdir()), ["pet.json", "spritesheet.png"])
            self.assertFalse((home / ".codex-global-state.json").exists())

    def test_themes_parse(self):
        root = Path(__file__).resolve().parents[1]
        for variant in ("dark", "light"):
            text = (root / "themes" / f"codex-theme-{variant}.txt").read_text(encoding="utf-8").strip()
            prefix, payload = text.split(":", 1)
            self.assertEqual(prefix, "codex-theme-v1")
            theme = json.loads(payload)
            self.assertEqual(theme["variant"], variant)
            for key in ("accent", "surface", "ink"):
                self.assertRegex(theme["theme"][key], r"^#[0-9a-fA-F]{6}$")


if __name__ == "__main__":
    unittest.main()
