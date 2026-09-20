from __future__ import annotations

import importlib.util
import contextlib
import io
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "brand_distribution", ROOT / "scripts" / "brand_distribution.py"
)
assert SPEC and SPEC.loader
distribution = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(distribution)


class BrandDistributionTests(unittest.TestCase):
    def setUp(self):
        # Topology tests exercise the pending implementation without asserting
        # that this uncommitted task checkout is a publishable source revision.
        patcher = mock.patch.object(distribution, "_source_revision", return_value="a" * 40)
        patcher.start()
        self.addCleanup(patcher.stop)

    def snapshot(self, root):
        """Capture all entries, bytes and modification metadata without following links."""
        entries = {}
        pending = [root]
        while pending:
            path = pending.pop()
            metadata = path.lstat()
            mode = metadata.st_mode
            payload = None
            if stat.S_ISLNK(mode):
                payload = os.readlink(path)
            elif stat.S_ISREG(mode):
                payload = path.read_bytes()
            elif stat.S_ISDIR(mode):
                pending.extend(path / name for name in os.listdir(path))
            entries[path.relative_to(root).as_posix()] = (
                mode, metadata.st_ino, metadata.st_mtime_ns, metadata.st_ctime_ns, payload
            )
        return entries

    def assert_refused_unchanged(self, root, fixture_root, offender):
        before = self.snapshot(fixture_root)
        for operation in (distribution.sync_consumer, distribution.check_consumer):
            with self.assertRaises(distribution.VerificationError) as raised:
                operation(root)
            self.assertIn(offender, str(raised.exception))
            self.assertEqual(before, self.snapshot(fixture_root))

    def test_manifests_are_current_and_consistent(self):
        distribution.generate(check=True)
        manifest = distribution.check_source()
        paths = [entry["path"] for entry in manifest["files"]]
        self.assertEqual(paths, sorted(paths))
        self.assertEqual(len(paths), len(set(paths)))
        self.assertFalse(manifest["selfHash"])
        self.assertNotIn("Web-Distribution.json", paths)

    def test_distributed_fonts_have_sil_licenses(self):
        manifest = distribution.check_source()
        distribution.check_licenses(manifest)
        consumer_paths = {entry["consumerPath"] for entry in manifest["files"]}
        self.assertIn("public/brand/fonts/Manrope-OFL.txt", consumer_paths)
        self.assertIn("public/brand/fonts/IBMPlexMono-OFL.txt", consumer_paths)

    def test_missing_font_license_is_rejected(self):
        manifest = distribution.web_manifest()
        manifest["files"] = [
            entry
            for entry in manifest["files"]
            if entry["path"] != "fonts/Manrope-OFL.txt"
        ]
        with self.assertRaisesRegex(distribution.VerificationError, "without"):
            distribution.check_licenses(manifest)

    def test_sync_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            distribution.sync_consumer(root)
            mtimes = {
                path: (root / path).stat().st_mtime_ns
                for path in (*distribution.WEB_PATHS.values(), distribution.CONSUMER_LOCK)
            }
            distribution.sync_consumer(root)
            self.assertEqual(
                mtimes,
                {
                    path: (root / path).stat().st_mtime_ns
                    for path in (*distribution.WEB_PATHS.values(), distribution.CONSUMER_LOCK)
                },
            )

    def test_missing_file_is_detected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            distribution.sync_consumer(root)
            target = root / "public/brand/icons/favicon.svg"
            target.unlink()
            with self.assertRaisesRegex(distribution.VerificationError, "missing"):
                distribution.check_consumer(root)
            distribution.sync_consumer(root)
            distribution.check_consumer(root)

    def test_tampered_file_is_detected_and_sync_repairs_it(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            distribution.sync_consumer(root)
            target = root / "public/brand/icons/favicon.svg"
            target.write_bytes(target.read_bytes() + b"tamper")
            with self.assertRaisesRegex(distribution.VerificationError, "tampered"):
                distribution.check_consumer(root)
            distribution.sync_consumer(root)
            distribution.check_consumer(root)

    def test_extra_managed_file_is_detected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            distribution.sync_consumer(root)
            extra = root / "public/brand/icons/unapproved.svg"
            extra.write_text("<svg/>", encoding="utf-8")
            with self.assertRaisesRegex(distribution.VerificationError, "extra"):
                distribution.check_consumer(root)

    def test_sync_preserves_unmanaged_consumer_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_note = root / "public/brand/SOURCE.md"
            source_note.parent.mkdir(parents=True)
            source_note.write_text("consumer-owned\n", encoding="utf-8")
            distribution.sync_consumer(root)
            self.assertEqual(source_note.read_text(encoding="utf-8"), "consumer-owned\n")

    def test_managed_file_links_are_rejected_before_repairs(self):
        for destination in ("source-note", "approved", "external", "dangling", "matching"):
            with self.subTest(destination=destination), tempfile.TemporaryDirectory() as temporary:
                fixture = Path(temporary)
                root = fixture / "consumer"
                distribution.sync_consumer(root)
                # The first manifest entry would otherwise be repaired before the link.
                (root / "public/brand/brand-tokens.css").write_bytes(b"needs repair")
                offender = "public/brand/icons/favicon.svg"
                linked_file = root / offender
                matching_bytes = linked_file.read_bytes()
                linked_file.unlink()
                destinations = {
                    "source-note": root / "public/brand/SOURCE.md",
                    "approved": root / "public/brand/icons/favicon.ico",
                    "external": fixture / "outside.svg",
                    "dangling": fixture / "missing.svg",
                    "matching": fixture / "matching.svg",
                }
                target = destinations[destination]
                if destination in ("source-note", "external", "matching"):
                    target.write_bytes(matching_bytes if destination == "matching" else b"preserve")
                linked_file.symlink_to(target)
                self.assert_refused_unchanged(root, fixture, offender)

    def test_managed_directory_and_intervening_links_are_rejected(self):
        for offender in ("app", "public/brand", "public/brand/icons"):
            for destination in ("internal", "external", "dangling"):
                with self.subTest(offender=offender, destination=destination):
                    with tempfile.TemporaryDirectory() as temporary:
                        fixture = Path(temporary)
                        root = fixture / "consumer"
                        root.mkdir()
                        target = (root if destination == "internal" else fixture) / "owned"
                        if destination != "dangling":
                            target.mkdir()
                            (target / "keep.txt").write_bytes(b"preserve")
                        link = root / offender
                        link.parent.mkdir(parents=True, exist_ok=True)
                        link.symlink_to(target, target_is_directory=True)
                        self.assert_refused_unchanged(root, fixture, offender)

    def test_extra_entries_are_rejected_before_repairs_without_traversal(self):
        for kind in ("file", "directory", "file-link", "directory-link", "dangling-link"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temporary:
                fixture = Path(temporary)
                root = fixture / "consumer"
                distribution.sync_consumer(root)
                (root / "public/brand/brand-tokens.css").write_bytes(b"needs repair")
                offender = "public/brand/icons/unapproved"
                extra = root / offender
                if kind == "file":
                    extra.write_bytes(b"preserve")
                elif kind == "directory":
                    extra.mkdir()
                    (extra / "keep.txt").write_bytes(b"preserve")
                elif kind == "file-link":
                    extra.symlink_to(root / "public/brand/icons/favicon.svg")
                elif kind == "directory-link":
                    extra.symlink_to(root, target_is_directory=True)
                else:
                    extra.symlink_to(fixture / "absent")
                original_scandir = os.scandir

                def scan(path):
                    self.assertNotEqual(Path(path), extra, "must not traverse an extra directory")
                    return original_scandir(path)

                with mock.patch.object(distribution.os, "scandir", side_effect=scan):
                    self.assert_refused_unchanged(root, fixture, offender)

    def test_consumer_root_links_are_rejected_in_api_and_cli(self):
        for kind in ("directory", "file", "dangling"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temporary:
                fixture = Path(temporary)
                root = fixture / "consumer"
                target = fixture / "target"
                if kind == "directory":
                    distribution.sync_consumer(target)
                elif kind == "file":
                    target.write_bytes(b"preserve")
                root.symlink_to(target, target_is_directory=kind == "directory")
                self.assert_refused_unchanged(root, fixture, "symlink in managed consumer path: .")
                before = self.snapshot(fixture)
                for command in ("sync", "check-consumer"):
                    errors = io.StringIO()
                    with contextlib.redirect_stderr(errors):
                        self.assertEqual(distribution.main([command, "--consumer-root", str(root)]), 1)
                    self.assertIn("symlink in managed consumer path: .", errors.getvalue())
                    self.assertEqual(before, self.snapshot(fixture))

    def test_invalid_entry_types_are_rejected_before_repairs(self):
        cases = (
            (".", "file"),
            ("public", "file"),
            ("public/brand/icons", "file"),
            ("public/brand/svg/mishkal-wordmark-white.svg", "directory"),
            ("public/brand/icons/favicon.svg", "fifo"),
            ("public/brand/icons/unapproved", "fifo"),
        )
        for offender, kind in cases:
            with self.subTest(offender=offender, kind=kind):
                if kind == "fifo" and not hasattr(os, "mkfifo"):
                    continue
                with tempfile.TemporaryDirectory() as temporary:
                    fixture = Path(temporary)
                    root = fixture / "consumer"
                    target = root / offender
                    target.parent.mkdir(parents=True, exist_ok=True)
                    if kind == "file":
                        target.write_bytes(b"preserve")
                    elif kind == "directory":
                        target.mkdir()
                    else:
                        os.mkfifo(target)
                    self.assert_refused_unchanged(root, fixture, offender)

    def test_late_invalid_manifest_paths_leave_tree_unchanged(self):
        for field in ("path", "consumerPath", "managedConsumerRoots", "managedConsumerFiles"):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                distribution.sync_consumer(root)
                (root / "public/brand/brand-tokens.css").write_bytes(b"needs repair")
                manifest = distribution.web_manifest()
                if field in ("path", "consumerPath"):
                    manifest["files"][-1][field] = "../invalid"
                else:
                    manifest[field].append("../invalid")
                with mock.patch.object(distribution, "check_source", return_value=manifest):
                    self.assert_refused_unchanged(root, root, "../invalid")

    def test_lock_records_exact_source_and_manifest(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            distribution.sync_consumer(root)
            lock = json.loads((root / distribution.CONSUMER_LOCK).read_bytes())
            self.assertEqual(lock, {
                "schemaVersion": 1,
                "repository": "mishkal-ai/branding",
                "version": "1.1.0",
                "revision": "a" * 40,
                "webDistributionSha256": distribution._digest(distribution.WEB_MANIFEST)[1],
            })

    def test_check_rejects_invalid_lock_and_sync_repairs_it(self):
        for kind in ("absent", "malformed", "schemaVersion", "repository", "version", "revision",
                     "webDistributionSha256", "missing-field", "extra-field"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                distribution.sync_consumer(root)
                lock_path = root / distribution.CONSUMER_LOCK
                lock = json.loads(lock_path.read_bytes())
                if kind == "absent":
                    lock_path.unlink()
                elif kind == "malformed":
                    lock_path.write_text("{broken")
                else:
                    if kind == "missing-field":
                        del lock["revision"]
                    else:
                        lock[kind] = "invalid"
                    lock_path.write_bytes(distribution._json_bytes(lock))
                before = self.snapshot(root)
                with self.assertRaisesRegex(distribution.VerificationError, "brand.lock.json"):
                    distribution.check_consumer(root)
                self.assertEqual(before, self.snapshot(root))
                distribution.sync_consumer(root)
                distribution.check_consumer(root)

    def test_lock_topology_is_preflighted_before_asset_repairs(self):
        for kind in ("link", "dangling", "directory", "fifo"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temporary:
                if kind == "fifo" and not hasattr(os, "mkfifo"):
                    continue
                root = Path(temporary)
                distribution.sync_consumer(root)
                lock = root / distribution.CONSUMER_LOCK
                lock.unlink()
                if kind in ("link", "dangling"):
                    lock.symlink_to(root / ("public/brand/brand-tokens.css" if kind == "link" else "absent"))
                elif kind == "directory":
                    lock.mkdir()
                else:
                    os.mkfifo(lock)
                (root / "public/brand/brand-tokens.css").write_bytes(b"needs repair")
                self.assert_refused_unchanged(root, root, "brand.lock.json")

    def test_sync_refuses_symlink_escape(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "consumer"
            outside = Path(temporary) / "outside"
            root.mkdir()
            outside.mkdir()
            (root / "app").symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(distribution.VerificationError, "symlink"):
                distribution.sync_consumer(root)

    def test_sync_refuses_in_root_managed_file_symlink_before_any_write(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            brand = root / "public/brand"
            icons = brand / "icons"
            icons.mkdir(parents=True)
            source_note = brand / "SOURCE.md"
            source_note.write_text("consumer-owned\n", encoding="utf-8")
            (icons / "favicon.svg").symlink_to("../SOURCE.md")

            with self.assertRaisesRegex(distribution.VerificationError, "symlink"):
                distribution.sync_consumer(root)

            self.assertEqual(source_note.read_text(encoding="utf-8"), "consumer-owned\n")
            self.assertFalse((brand / "brand-tokens.css").exists())
            self.assertFalse((root / "app/fonts/Manrope-Variable.ttf").exists())

    def test_check_rejects_extra_symlink_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            distribution.sync_consumer(root)
            outside = root / "consumer-owned"
            outside.mkdir()
            (root / "public/brand/icons/linked-directory").symlink_to(
                outside, target_is_directory=True
            )
            with self.assertRaisesRegex(distribution.VerificationError, "symlink"):
                distribution.check_consumer(root)

    def test_check_rejects_extra_dangling_symlink(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            distribution.sync_consumer(root)
            (root / "public/brand/icons/dangling.svg").symlink_to("missing.svg")
            with self.assertRaisesRegex(distribution.VerificationError, "symlink"):
                distribution.check_consumer(root)

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO is not supported")
    def test_check_rejects_unsupported_managed_entry(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            distribution.sync_consumer(root)
            os.mkfifo(root / "public/brand/icons/not-an-asset")
            with self.assertRaisesRegex(distribution.VerificationError, "unsupported"):
                distribution.check_consumer(root)


class CommittedSourceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.fixture = Path(self.temporary.name)
        self.source = self.fixture / "branding"
        self.consumer = self.fixture / "consumer"
        shutil.copytree(ROOT, self.source, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        patcher = mock.patch.multiple(
            distribution, ROOT=self.source,
            ASSET_MANIFEST=self.source / "Asset-Manifest.json",
            WEB_MANIFEST=self.source / "Web-Distribution.json",
        )
        patcher.start()
        self.addCleanup(patcher.stop)
        distribution.generate(check=False)
        self.git("init", "--quiet")
        self.git("add", ".")
        self.git("commit", "--quiet", "-m", "Temporary test fixture")

    def git(self, *args):
        return subprocess.run(
            ["git", "-C", str(self.source), "-c", "user.name=Test Fixture",
             "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false", *args],
            check=True, capture_output=True, text=True,
        ).stdout.strip()

    def test_committed_cli_sync_check_and_revision_upgrade(self):
        script = self.source / "scripts/brand_distribution.py"
        for command in ("sync", "check-consumer"):
            subprocess.run(
                ["python3", str(script), command, "--consumer-root", str(self.consumer)],
                check=True, capture_output=True, text=True,
            )
        lock = json.loads((self.consumer / distribution.CONSUMER_LOCK).read_bytes())
        first_revision = self.git("rev-parse", "HEAD")
        self.assertEqual(lock["revision"], first_revision)
        self.git("commit", "--quiet", "--allow-empty", "-m", "Next test revision")
        with self.assertRaisesRegex(distribution.VerificationError, "mismatched.*brand.lock.json"):
            distribution.check_consumer(self.consumer)
        distribution.sync_consumer(self.consumer)
        distribution.check_consumer(self.consumer)
        upgraded = json.loads((self.consumer / distribution.CONSUMER_LOCK).read_bytes())
        self.assertEqual(upgraded["revision"], self.git("rev-parse", "HEAD"))
        self.assertNotEqual(upgraded["revision"], first_revision)

    def test_dirty_staged_and_untracked_sources_cannot_write_a_lock(self):
        modified = self.source / "README.md"
        modified.write_bytes(modified.read_bytes() + b"\nChanged in fixture\n")
        distribution.generate(check=False)
        for staged in (False, True):
            with self.subTest(staged=staged):
                if staged:
                    self.git("add", ".")
                with self.assertRaisesRegex(distribution.VerificationError, "dirty or uncommitted"):
                    distribution.sync_consumer(self.consumer)
                self.assertFalse(self.consumer.exists())
        self.git("commit", "--quiet", "-m", "Commit fixture modification")
        (self.source / "untracked.txt").write_text("uncommitted")
        distribution.generate(check=False)
        with self.assertRaisesRegex(distribution.VerificationError, "dirty or uncommitted"):
            distribution.sync_consumer(self.consumer)
        self.assertFalse(self.consumer.exists())

    def test_status_hidden_modifications_are_rejected(self):
        self.git("update-index", "--assume-unchanged", "README.md", "Asset-Manifest.json")
        path = self.source / "README.md"
        path.write_bytes(path.read_bytes() + b"\nHidden change\n")
        distribution.generate(check=False)
        self.assertEqual(self.git("status", "--porcelain"), "")
        with self.assertRaisesRegex(distribution.VerificationError, "differs from committed revision"):
            distribution.sync_consumer(self.consumer)
        self.assertFalse(self.consumer.exists())


if __name__ == "__main__":
    unittest.main()
