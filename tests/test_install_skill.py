"""Exercise complete installation and backup preservation in synthetic directories."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1] / 'skills/claude-environment-setup/scripts/install_skill.py'
spec = importlib.util.spec_from_file_location('install_skill', SOURCE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class InstallTests(unittest.TestCase):
    def source(self, root):
        src = root / 'source'
        (src / 'references').mkdir(parents=True)
        (src / 'assets').mkdir()
        (src / 'SKILL.md').write_text('new skill')
        (src / 'references/install.md').write_text('self-contained')
        (src / 'assets/fixture.png').write_bytes(b'synthetic-image')
        return src

    def test_fresh_install_includes_nested_assets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); src = self.source(root)
            dst = root / 'tool/skills/claude-environment-setup'
            result = mod.install(src, dst)
            self.assertIsNone(result['backup'])
            for p in src.rglob('*'):
                if p.is_file():
                    self.assertEqual(p.read_bytes(), (dst / p.relative_to(src)).read_bytes())

    def test_existing_custom_files_preserved_in_backup(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); src = self.source(root)
            dst = root / 'tool/skills/claude-environment-setup'
            dst.mkdir(parents=True)
            (dst / 'custom.md').write_text('user edit')
            result = mod.install(src, dst)
            backup = Path(result['backup'])
            self.assertEqual((backup / 'custom.md').read_text(), 'user edit')
            self.assertNotIn(dst.parent, backup.parents)
            self.assertTrue((dst / 'SKILL.md').is_file())

    def test_source_can_be_installed_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); src = self.source(root)
            result = mod.install(src, src)
            self.assertEqual((src / 'SKILL.md').read_text(), 'new skill')
            self.assertTrue(Path(result['backup']).is_dir())


if __name__ == '__main__':
    unittest.main()
