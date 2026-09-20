# Branding repository agent guide

This repository owns Mishkal visual source assets, distribution metadata and
brand guidance. It does not own application behavior, deployment, or consumer
layout decisions. Current user scope governs; this guide does not authorize
publishing, tagging, merging, deployment, or changes in consumer repositories.

## Working rules

- Preserve approved artwork geometry, clear-space frames, palette roles and
  installed-app icon treatment. Do not redraw assets without explicit approval.
- Keep browser favicons distinct from installed-app icons: the browser favicon
  is Mishkal Teal on transparency; app and touch icons are white on Deep Navy.
- Keep `brand-tokens.css` side-effect free. Optional local font loading belongs
  in `font-faces.css` and consumers may choose their own loading mechanism.
- Change the web allowlist in `scripts/brand_distribution.py` deliberately.
  Consumer paths are a contract; coordinate their changes with every consumer.
- Regenerate both manifests after release-file changes, then run the complete
  verification commands below. `Asset-Manifest.json` intentionally excludes
  itself, and `Web-Distribution.json` is not self-hashed.
- Font binaries must retain the matching bundled SIL Open Font License files.
  Never place credentials or private consumer data in this repository.
- Preserve unrelated work. Do not hand-edit generated checksums, discard user
  changes, or claim that source checks establish deployed consumer state.

## Required checks

```sh
python3 scripts/brand_distribution.py generate --check
python3 scripts/brand_distribution.py check-source
python3 -m unittest discover -s tests -v
```

Update `README.md`, `CHANGELOG.md`, and the relevant document under `docs/`
when behavior, release contents, or the consumer contract changes.
