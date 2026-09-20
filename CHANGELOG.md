# Changelog

## Unreleased

- Document public, exact-revision consumer acquisition and remove the obsolete
  private-repository credential requirement. This changes no artwork, release
  version, web distribution or consumer lock.

- Cancel superseded CI runs within the same pull request and add a provisional
  10-minute `brand-kit` timeout. Keep all checks and `main` runs; document usage
  reporting and regenerate the full inventory without changing brand assets,
  release version or the web distribution.

- Align standalone triage, review, task publication and documentation gates with
  the six-repository workflow; clarify Branding and frontend ownership and
  managed Codex configuration. Artwork, version and web distribution are unchanged.

## 1.1.0 - 2026-09-20

- Adopt the approved transparent Mishkal Teal browser favicons from webapp
  revision `65f7a3374e3b60c326692a6d05a680eff38a5a36`; installed-app and touch
  icons remain white-on-Navy.
- Add a deterministic, checksummed web distribution and consumer sync/check
  tool that preflights all manifest paths and consumer topology before writing,
  rejects root/managed-path symlinks and unsupported or misplaced entries, and
  refuses extras without traversing extra directories or deleting entries.
  Invalid paths or topology leave the whole consumer tree unchanged; regular
  missing/tampered files remain repairable and matching files retain mtimes.
- Generate a deterministic consumer `brand.lock.json` binding version, exact
  committed Branding source and web-manifest checksum; validate it in read-only
  consumer CI and reject dirty/uncommitted source identities.
- Separate semantic design tokens from optional local `@font-face`
  declarations.
- Correct the canonical PDF and identity-preview filenames.
- Add repository guidance, automated verification, and a proposed repository
  `main` protection payload.

## 1.0.0 - 2026-09-19

- Initial production kit for the approved A1.2 / Light direction.
