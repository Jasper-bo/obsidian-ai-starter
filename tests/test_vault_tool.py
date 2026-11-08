"""Behavioral checks: preserve notes, stay in Vault, search current Chinese text."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "skills/obsidian-ai-starter/scripts/vault_tool.py"


class VaultToolTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="vault-skill-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.vault = self.base / "中文 空间" / "个人知识库"

    def run_tool(self, command, *arguments, expected=0):
        result = subprocess.run([sys.executable, str(SCRIPT), command, "--vault", str(self.vault), *arguments],
                                capture_output=True, encoding="utf-8")
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_dry_run_and_idempotent_init(self):
        result = self.run_tool("init")
        self.assertEqual(result["mode"], "dry-run")
        self.assertFalse(self.vault.exists())
        self.run_tool("init", "--apply")
        note = self.vault / "开始这里.md"
        note.write_text("# 用户自己的首页\n", encoding="utf-8")
        before = {p.relative_to(self.vault): p.read_bytes() for p in self.vault.rglob("*") if p.is_file()}
        again = self.run_tool("init", "--apply")
        after = {p.relative_to(self.vault): p.read_bytes() for p in self.vault.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(again["created"], [])
        self.assertTrue(self.run_tool("doctor")["passed"])

    def test_chinese_search_citations_and_updates(self):
        self.run_tool("init", "--apply")
        note = self.vault / "10-来源/项目会议.md"
        note.write_text("# 项目\n预算为2300元\n会议时间周四14:30\n", encoding="utf-8")
        result = self.run_tool("search", "--query", "项目预算是多少")
        hit = next(item for item in result["results"] if item["file"].endswith("项目会议.md"))
        self.assertEqual(hit["line"], 2)
        self.assertEqual(hit["excerpt"][1]["text"], "预算为2300元")
        note.write_text("# 项目\n预算为2600元\n会议时间周四14:30\n", encoding="utf-8")
        updated = self.run_tool("search", "--query", "预算")
        self.assertIn("2600", json.dumps(updated, ensure_ascii=False))
        self.assertNotIn("2300", json.dumps(updated, ensure_ascii=False))
        self.assertEqual(self.run_tool("search", "--query", "负责人姓名")["results"], [])

    def test_symlink_cannot_write_outside_or_leak_in_search(self):
        outside = self.base / "outside"
        outside.mkdir()
        self.vault.mkdir(parents=True)
        (self.vault / "10-来源").symlink_to(outside, target_is_directory=True)
        self.run_tool("init", "--apply", expected=2)
        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse((self.vault / "开始这里.md").exists())
        (outside / "secret.md").write_text("秘密预算9988", encoding="utf-8")
        self.assertEqual(self.run_tool("search", "--query", "秘密预算")["results"], [])

    def test_invalid_layout_fails_before_writes(self):
        self.vault.mkdir(parents=True)
        (self.vault / "开始这里.md").mkdir()
        self.run_tool("init", "--apply", expected=2)
        self.assertFalse((self.vault / "00-收件箱").exists())

    def test_bom_and_invalid_encoding_are_reported(self):
        self.run_tool("init", "--apply")
        (self.vault / "10-来源/BOM.md").write_text("预算123", encoding="utf-8-sig")
        (self.vault / "10-来源/破损.md").write_bytes(b"\xff\xfe\xfa")
        result = self.run_tool("search", "--query", "预算")
        self.assertTrue(result["results"])
        self.assertEqual(len(result["skipped"]), 1)
        self.assertFalse(self.run_tool("doctor", expected=1)["passed"])


if __name__ == "__main__":
    unittest.main()
