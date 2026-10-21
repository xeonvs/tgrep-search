from __future__ import annotations

import errno
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import tempfile
import time
import unittest


SUPPORTED_VERSION = "1.2.4"
NEEDLE = "behavioral_fixture_hit"


def find_tgrep() -> tuple[str | None, str | None]:
    binary = shutil.which(os.environ.get("TGREP_BIN", "tgrep"))
    if binary is None:
        return None, None
    result = subprocess.run(
        [binary, "--version"], text=True, capture_output=True, check=False, timeout=10
    )
    fields = result.stdout.strip().split()
    version = fields[-1] if result.returncode == 0 and fields else None
    return binary, version


TGREP, TGREP_VERSION = find_tgrep()
RG = shutil.which("rg")
GIT = shutil.which("git")
HAS_SUPPORTED_TGREP = TGREP is not None and TGREP_VERSION == SUPPORTED_VERSION
SKIP_REASON = (
    f"requires optional tgrep {SUPPORTED_VERSION}; "
    f"detected {TGREP_VERSION or 'no usable binary'}"
)


def run(
    argv: list[str],
    *,
    cwd: Path,
    env: dict[str, str],
    expected: int = 0,
    timeout: float = 30,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
        timeout=timeout,
    )
    if result.returncode != expected:
        raise AssertionError(
            f"{argv!r}: expected exit {expected}, got {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def fixture_environment(home: Path) -> dict[str, str]:
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env.update(
        {
            "HOME": str(home),
            "USERPROFILE": str(home),
            "XDG_CONFIG_HOME": str(home),
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": str(home / "gitconfig"),
            "GIT_TERMINAL_PROMPT": "0",
        }
    )
    return env


def stop_owned_process(child: subprocess.Popen[bytes]) -> None:
    if child.poll() is None:
        try:
            if os.name == "nt":
                child.terminate()
            else:
                os.killpg(child.pid, signal.SIGTERM)
            child.wait(timeout=5)
        except (ProcessLookupError, subprocess.TimeoutExpired):
            if child.poll() is None:
                if os.name == "nt":
                    child.kill()
                else:
                    os.killpg(child.pid, signal.SIGKILL)
                child.wait(timeout=5)


@unittest.skipUnless(HAS_SUPPORTED_TGREP, SKIP_REASON)
class TgrepCliTest(unittest.TestCase):
    def setUp(self) -> None:
        if GIT is None:
            self.skipTest("git is required for ignore-aware fixtures")
        self.temporary = tempfile.TemporaryDirectory(prefix="tgrep-cli-test-")
        self.addCleanup(self.temporary.cleanup)
        self.scratch = Path(self.temporary.name).resolve()
        self.home = self.scratch / "home"
        self.root = self.scratch / "repo"
        self.index = self.scratch / "index"
        self.home.mkdir()
        self.root.mkdir()
        self.env = fixture_environment(self.home)
        self.git("init", "-q")
        (self.root / ".gitignore").write_text("ignored.py\n", encoding="utf-8")
        fixtures = {
            "visible.py": f"print('{NEEDLE} visible')\n",
            "explicit.txt": f"{NEEDLE} explicit\n",
            "other.js": f"const marker = '{NEEDLE}';\n",
            ".hidden.py": f"print('{NEEDLE} hidden')\n",
            "ignored.py": f"print('{NEEDLE} ignored')\n",
        }
        for name, content in fixtures.items():
            (self.root / name).write_text(content, encoding="utf-8")
        self.cli("index", "--index-path", str(self.index), ".", timeout=60)

    def git(self, *args: str) -> subprocess.CompletedProcess[str]:
        assert GIT is not None
        return run([GIT, *args], cwd=self.root, env=self.env)

    def cli(
        self, *args: str, expected: int = 0, timeout: float = 30
    ) -> subprocess.CompletedProcess[str]:
        assert TGREP is not None
        return run(
            [TGREP, *args],
            cwd=self.root,
            env=self.env,
            expected=expected,
            timeout=timeout,
        )

    @staticmethod
    def paths(stdout: str) -> set[str]:
        return {line.removeprefix("./") for line in stdout.splitlines() if line}

    def test_indexed_search_matches_ripgrep_scan(self) -> None:
        if RG is None:
            self.skipTest("rg is required for parity validation")
        options = ["--sort", "path", "--color", "never", "-n", "-H", "-F"]
        indexed = self.cli("--index-path", str(self.index), *options, "--", NEEDLE, ".")
        scanned = run(
            [RG, *options, "--", NEEDLE, "."], cwd=self.root, env=self.env
        )
        self.assertEqual(indexed.stdout, scanned.stdout)

    def test_membership_filters_and_explicit_file_bypass(self) -> None:
        def files(*options: str) -> set[str]:
            result = self.cli(
                "--index-path", str(self.index), *options, "--files", "--sort", "path", "."
            )
            return self.paths(result.stdout)

        self.assertNotIn(".hidden.py", files())
        self.assertNotIn("ignored.py", files())
        self.assertIn(".hidden.py", files("--hidden"))
        self.assertNotIn("ignored.py", files("--hidden"))
        self.assertIn("ignored.py", files("--hidden", "--no-ignore"))
        self.assertEqual(files("-g", "*.py"), {"visible.py"})
        typed = self.cli(
            "--index-path", str(self.index), "-l", "-t", "py", "-F", "--", NEEDLE, "."
        )
        self.assertEqual(self.paths(typed.stdout), {"visible.py"})
        explicit = self.cli(
            "--index-path",
            str(self.index),
            "-l",
            "-t",
            "py",
            "-g",
            "*.py",
            "-F",
            "--",
            NEEDLE,
            "explicit.txt",
        )
        self.assertEqual(self.paths(explicit.stdout), {"explicit.txt"})

    def test_no_index_reads_stale_edit_and_followed_traversal(self) -> None:
        fresh = "post_index_current_content"
        (self.root / "visible.py").write_text(f"print('{fresh}')\n", encoding="utf-8")
        self.cli("--index-path", str(self.index), "-F", "--", fresh, ".", expected=1)
        current = self.cli(
            "--index-path", str(self.index), "--no-index", "-F", "--", fresh, "."
        )
        self.assertIn(fresh, current.stdout)
        if os.name == "nt":
            return
        external = self.scratch / "external"
        external.mkdir()
        followed_marker = "followed_traversal_only"
        (external / "linked.txt").write_text(f"{followed_marker}\n", encoding="utf-8")
        (self.root / "linked").symlink_to(external, target_is_directory=True)
        self.cli(
            "--index-path", str(self.index), "-L", "-F", "--", followed_marker, ".", expected=1
        )
        followed = self.cli(
            "--index-path",
            str(self.index),
            "--no-index",
            "-L",
            "-F",
            "--",
            followed_marker,
            ".",
        )
        self.assertIn("linked/linked.txt", followed.stdout)

    def test_json_and_exit_status_contract(self) -> None:
        result = self.cli(
            "--index-path", str(self.index), "--json", "-F", "--", NEEDLE, "visible.py"
        )
        records = [json.loads(line) for line in result.stdout.splitlines()]
        matches = [record for record in records if record.get("type") == "match"]
        self.assertEqual(len(matches), 1)
        self.assertTrue(matches[0]["data"]["path"]["text"].endswith("visible.py"))
        self.assertEqual(matches[0]["data"]["line_number"], 1)
        self.cli("--index-path", str(self.index), "-q", "-F", "--", NEEDLE, ".")
        self.cli(
            "--index-path", str(self.index), "-q", "-F", "--", "absent", ".", expected=1
        )
        invalid = self.cli("--no-index", "--", "[", ".", expected=2)
        self.assertTrue(invalid.stderr.strip())
        partial = self.cli(
            "--no-index", "-F", "--", NEEDLE, "visible.py", "missing.py", expected=2
        )
        self.assertIn(NEEDLE, partial.stdout)
        self.assertTrue(partial.stderr.strip())

    @unittest.skipIf(os.name == "nt", "Unix-only unrepresentable index paths")
    def test_unrepresentable_index_names_remain_searchable_by_scan(self) -> None:
        special = "special_filename_content"
        (self.root / "back\\slash.txt").write_text(special + "\n", encoding="utf-8")
        raw_name = os.fsencode(self.root) + b"/invalid-\xff.txt"
        expected_files = 1
        try:
            descriptor = os.open(raw_name, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except OSError as error:
            if error.errno != errno.EILSEQ:
                raise
            # Some filesystems (including APFS) forbid invalid UTF-8 names.
        else:
            with os.fdopen(descriptor, "wb") as output:
                output.write((special + "\n").encode())
            expected_files += 1
        built = self.cli("index", "--index-path", str(self.index), ".", timeout=60)
        self.assertTrue(built.stderr.strip(), "unsupported paths must be diagnosed")
        self.cli("--index-path", str(self.index), "-F", "--", special, ".", expected=1)
        scanned = self.cli(
            "--index-path", str(self.index), "--no-index", "-F", "--", special, "."
        )
        self.assertEqual(scanned.stdout.count(special), expected_files)

    def test_ordinary_server_cold_to_ready(self) -> None:
        assert TGREP is not None
        server_index = self.scratch / "server-index"
        log_path = self.scratch / "ordinary-daemon.log"
        descriptor = os.open(log_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(descriptor, "wb") as daemon_log:
            child = subprocess.Popen(
                [TGREP, "serve", ".", "--index-path", str(server_index), "--no-watch"],
                cwd=self.root,
                env=self.env,
                stdin=subprocess.DEVNULL,
                stdout=daemon_log,
                stderr=subprocess.STDOUT,
                start_new_session=os.name != "nt",
            )
            try:
                first = self.cli(
                    "--index-path", str(server_index), "--sort", "path", "-F", "--", NEEDLE, "."
                )
                deadline = time.monotonic() + 30
                ready_status = ""
                while time.monotonic() < deadline:
                    self.assertIsNone(child.poll(), "server exited before becoming ready")
                    probe = subprocess.run(
                        [TGREP, "status", "--index-path", str(server_index), "."],
                        cwd=self.root,
                        env=self.env,
                        text=True,
                        capture_output=True,
                        check=False,
                        timeout=5,
                    )
                    if probe.returncode == 0 and "Indexing:   complete" in probe.stdout:
                        ready_status = probe.stdout
                        break
                    time.sleep(0.05)
                self.assertIn("Indexing:   complete", ready_status)
                ready = self.cli(
                    "--index-path", str(server_index), "--stats", "--sort", "path", "-F", "--", NEEDLE, "."
                )
                # --stats includes timing; compare only matched lines and prove transport.
                matches = lambda text: [line for line in text.splitlines() if NEEDLE in line]
                self.assertEqual(matches(first.stdout), matches(ready.stdout))
                self.assertEqual(len(matches(ready.stdout)), 3)
                self.assertIn("(via server)", ready.stdout + ready.stderr)
            finally:
                stop_owned_process(child)


if __name__ == "__main__":
    unittest.main()
