# Web distribution contract

`Web-Distribution.json` is the approved web subset of brand kit 1.1.0. Schema
version 1 records the release `version`, deterministic `order`, `selfHash`
policy, exact artifact `provenance`, managed consumer paths, and sorted file
records containing source `path`, `consumerPath`, `bytes`, and SHA-256.

The current contract places supporting font binaries under `app/fonts`, while
logos, icons, licenses and semantic tokens live under `public/brand`.
Consumer-owned `public/brand/SOURCE.md` is outside managed roots and is
preserved. Consumer paths are a contract: coordinate changes with consumers.

## Versioning and release procedure

The kit follows semantic versioning: incompatible consumer-path or contract
changes require a major version; additive approved assets/features use a minor
version; compatible corrections use a patch version. Release `1.1.0` is named
`v1.1.0` in Git tags/releases. A published version/tag must not be retargeted;
corrections require a new version. The lock records the version without the `v`
prefix and binds the full commit, not a mutable branch or tag name.

1. Make approved changes and update `RELEASE_VERSION`, the allowlist and current
   documentation in the same task.
2. Run `python3 scripts/brand_distribution.py generate` after all source,
   documentation, and test edits.
3. Run the three checks in `docs/Verification.md` and inspect the complete diff.
4. Publish the reviewed task through the repository lifecycle. After the user
   merges it, verify the clean release commit and its checks. Only when separately
   authorized, create the immutable `v1.1.0` tag and release at that exact commit;
   record its commit and `Web-Distribution.json` SHA-256 in the release notes.
5. In a separately authorized consumer task, acquire that committed source,
   run `sync`, review the assets and lock diff together, update consumer-owned
   provenance notes, and run consumer CI before publication. Tagging or release
   publication does not sync or deploy consumers.

Generation writes `Web-Distribution.json` before calculating the full release
inventory. `Asset-Manifest.json` therefore checksums the web manifest but
excludes itself. The web manifest includes neither manifest, avoiding recursive
hash dependencies.

## Consumer lock and upgrades

Sync writes a deterministic root `brand.lock.json` after copying the assets:

```json
{
  "schemaVersion": 1,
  "repository": "mishkal-ai/branding",
  "version": "1.1.0",
  "revision": "<full Branding commit>",
  "webDistributionSha256": "<SHA-256 of exact Web-Distribution.json bytes>"
}
```

The angle-bracket values above are documentation placeholders; sync computes
both values. Commit this lock alongside the consumer assets. It is generated
consumer metadata, not a copied source asset, and therefore has no entry in the
web manifest's source-file hashes. Matching assets and matching lock bytes keep
their modification times. `check-consumer` is read-only and rejects absent,
malformed, stale or mismatched locks as well as asset drift.

Both consumer commands require a clean, committed Branding checkout. All release
files must be committed at its `HEAD` and match their Git blob bytes. Dirty,
staged, untracked or status-hidden modifications cannot claim a committed release
identity. `generate`, `check-source` and unit tests still support work in progress;
they do not establish a publishable revision. Source archives without Git metadata
cannot be used for sync/check-consumer.

To upgrade, explicitly acquire and verify the approved new Branding commit, then
run its `sync` command. Sync repairs or replaces a regular stale/malformed lock;
it rejects a symlink or unsupported lock entry before any asset writes. Review
the version, revision, checksum and asset changes together. An empty new commit
still changes the lock revision even when its manifest checksum is identical.

## Consumer-local CI

Consumer CI must acquire the locked source from the trusted
`mishkal-ai/branding` repository using normal read-only repository credentials.
Read `revision` from the committed consumer lock, require a full lowercase
40- or 64-character hexadecimal commit, and check out that exact commit in a
separate Branding directory in detached-HEAD mode. Do not use an unpinned
`main`, a moving tag, or an arbitrary sibling checkout. Confirm the acquired
checkout's `git rev-parse HEAD` equals the requested revision before invoking
its checker. No credentials belong in the lock or repository.

From the consumer root, with that checkout supplied as `BRANDING_ROOT`:

```sh
python3 "$BRANDING_ROOT/scripts/brand_distribution.py" check-consumer --consumer-root .
```

This invocation is read-only in the consumer and requires no consumer sync in CI.
The checker independently verifies the source's clean committed bytes, matches
the lock's exact commit/version/manifest checksum, then verifies every managed
asset and the topology. A provided source checkout at a different commit fails
even if the assets happen to match. A missing lock fails; CI must not repair it
by running sync. Acquiring the source requires Git repository access; verification
itself uses only Python's standard library and local Git, with no network access.

For example, a CI acquisition step may validate the lock revision before passing
it as the `ref` input of its trusted checkout action:

```sh
python3 -c 'import json, re; lock = json.load(open("brand.lock.json")); revision = lock["revision"]; assert isinstance(revision, str) and re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", revision); print(revision)'
```

The checkout repository is fixed in CI configuration; never derive a clone URL
or executable path from lock contents. Review lock updates as dependency upgrades.

## Filesystem safety

Sync validates all manifest paths and preflights the consumer root, every managed
destination, intervening component, and managed directory before its first write.
It rejects symlinks (including root, internal, external, dangling, and matching-byte
links), unsupported entry types, and files/directories in the wrong position.
Unexpected files and directories fail preflight; extra directories are not
traversed and no extras are deleted. Diagnostics identify the consumer-relative
offender (`.` denotes the consumer root). Invalid paths or topology leave the
entire consumer tree unchanged, including files that otherwise need repair.

Missing or tampered regular files remain repairable; matching regular files keep
their modification times. Consumer verification uses the same topology checks.
Run with exclusive access to the consumer tree: preflight is not protection
against concurrent filesystem changes, and per-file atomic replacement is not
a transaction rolling back unrelated I/O failures during sync.
