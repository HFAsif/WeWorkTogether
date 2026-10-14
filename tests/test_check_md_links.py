"""Contract tests for the offline Markdown link checker (issue #2).

The CLI and CI have been implemented; these tests guard supported behavior.
Run after implementation: python -m unittest discover -s tests -v
"""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


CHECKER = Path(__file__).resolve().parents[1] / "scripts" / "check_md_links.py"


class OfflineMarkdownLinksTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, relative_path: str, content: str = "") -> Path:
        file_path = self.root / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        return file_path

    def run_checker(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CHECKER), "--root", str(self.root)],
            cwd=self.root,
            text=True,
            capture_output=True,
            timeout=15,
            check=False,
        )

    def assert_valid(self):
        outcome = self.run_checker()
        self.assertEqual(
            outcome.returncode,
            0,
            f"Expected all local links to resolve:\n{outcome.stdout}\n{outcome.stderr}",
        )

    def assert_missing(self, target: str, source: str = "README.md"):
        outcome = self.run_checker()
        self.assertEqual(
            outcome.returncode,
            1,
            f"Expected a broken-link status:\n{outcome.stdout}\n{outcome.stderr}",
        )
        diagnostic = outcome.stdout + outcome.stderr
        self.assertIn(target, diagnostic)
        self.assertIn(source, diagnostic)

    def test_resolves_valid_relative_file_link(self):
        self.write("README.md", "[guide](docs/guide.md)\n")
        self.write("docs/guide.md", "# Guide\n")
        self.assert_valid()

    def test_reports_missing_relative_file(self):
        self.write("README.md", "[broken](does-not-exist.md)\n")
        self.assert_missing("does-not-exist.md")

    def test_resolves_parent_directory_from_markdown_file(self):
        self.write("README.md", "# Home\n")
        self.write("docs/guide.md", "[home](../README.md)\n")
        self.assert_valid()

    def test_ignores_external_urls_and_fragment_only_links(self):
        self.write(
            "README.md",
            "[web](https://example.org) [insecure](http://example.org)\n"
            "[contact](mailto:hello@example.org) [section](#welcome)\n"
            "[protocol-relative](//example.org/doc)\n",
        )
        self.assert_valid()

    def test_decodes_local_filename_and_ignores_query_fragment(self):
        self.write("README.md", "[encoded](docs/guide%20one.md?view=1#intro)\n")
        self.write("docs/guide one.md", "# Intro\n")
        self.assert_valid()

    def test_accepts_local_directory_target(self):
        self.write("README.md", "[templates](.github/ISSUE_TEMPLATE/)\n")
        self.write(".github/ISSUE_TEMPLATE/example.yml", "name: Sample\n")
        self.assert_valid()

    def test_ignores_links_inside_backtick_code_fences(self):
        self.write(
            "README.md",
            "# Sample\n\n```md\n[not a real link](missing.md)\n```\n"
            "[real link](guide.md)\n",
        )
        self.write("guide.md", "# Guide\n")
        self.assert_valid()

    def test_reports_missing_image_asset(self):
        self.write("README.md", "![missing image](assets/no-image.png)\n")
        self.assert_missing("assets/no-image.png")


    def test_handles_tilde_fence(self):
        self.write("README.md", "~~~md\n[not a real link](missing.md)\n~~~\n")
        self.assert_valid()

    def test_reports_multiple_broken_links(self):
        self.write("README.md", "[a](bad-one.md)\n![b](bad-two.png)\n")
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("README.md:1", result.stdout)
        self.assertIn("README.md:2", result.stdout)
        self.assertIn("bad-one.md", result.stdout)
        self.assertIn("bad-two.png", result.stdout)

    def test_invalid_root(self):
        path = self.root / "missing-dir"
        result = subprocess.run(
            [sys.executable, str(CHECKER), "--root", str(path)],
            capture_output=True, text=True, timeout=15, check=False,
        )
        self.assertEqual(result.returncode, 2)


    def test_ignores_single_backtick_code_example(self):
        self.write("README.md", "Example: `[fake](does-not-exist.md)`\n")
        self.assert_valid()

    def test_ignores_double_backtick_code_example(self):
        self.write("README.md", "Use ``[fake](does-not-exist.md)`` and [real](guide.md)\n")
        self.write("guide.md", "# Guide\n")
        self.assert_valid()

    def test_still_reports_real_link_beside_inline_code(self):
        self.write("README.md", "`[fake](ignore-me.md)` [bad](really-missing.md)\n")
        outcome = self.run_checker()
        self.assertEqual(outcome.returncode, 1, outcome.stdout + outcome.stderr)
        self.assertIn("really-missing.md", outcome.stdout)
        self.assertNotIn("ignore-me.md", outcome.stdout)

    def test_code_fence_info_string_is_not_a_closing_fence(self):
        self.write(
            "README.md",
            "~~~md\n~~~python\n[not a link](missing.md)\n~~~\n",
        )
        self.assert_valid()

    def test_link_after_actual_fence_close_is_checked(self):
        self.write(
            "README.md",
            "~~~md\n~~~python\n[inside](ignore.md)\n~~~\n[outside](missing.md)\n",
        )
        self.assert_missing("missing.md")

    def test_long_fence_requires_equally_long_closing_fence(self):
        self.write(
            "README.md",
            "~~~~md\n~~~\n[inside](missing.md)\n~~~~\n",
        )
        self.assert_valid()


if __name__ == "__main__":
    unittest.main()
