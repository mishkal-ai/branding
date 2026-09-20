# Repository controls

The GitHub Actions workflow runs source/manifests checks and distribution tests
for pull requests and pushes to `main`, using read-only repository permissions.
Its required check name is `brand-kit`.

`.github/main-protection.json` is a GitHub branch-protection API payload for this
private repository. It requires the current CI check, an up-to-date branch, one
approving review from someone other than the last pusher, resolved conversations,
linear history, and administrator enforcement. Force pushes and branch deletion
are disabled. It grants no repository access.

Applying it changes remote policy and is intentionally not part of source
verification. An authorized administrator may apply it only after confirming
the repository, default branch, plan-supported features, and check name:

```sh
gh api --method PUT \
  repos/mishkal-ai/branding/branches/main/protection \
  --input .github/main-protection.json
```

Presence of the payload does not prove that remote protection is configured.
