# Repository controls

[AGENTS.md](../AGENTS.md) carries the standalone triage, model, independent-review,
registered-worktree, publication and documentation gates. The coordinator assigns
a bounded Branding writer; the stable frontend role covers assigned Website or
Webapp consumers. Backend [agent workflow](../../bknd/docs/agent-workflow.md) owns
lifecycle commands and canonical managed `.codex/` configuration. Synchronize only
inside registered task worktrees and preserve custom configuration conflicts.
Unless the user explicitly requests local-only work, the coordinator commits and
publishes each implementation task through that lifecycle; workers do not publish.
Use explicit `--regular-pr`/BLOCKED/`--ready` evidence as required. The user merges
manually unless delegated; publication never authorizes deployment or cleanup.

Governance maintenance belongs under Unreleased and does not bump the brand
version or alter the web allowlist or consumer locks. Regenerate the full asset
manifest after tracked governance/configuration changes, then run all required
[checks](../AGENTS.md#required-checks). Consumer updates remain separately scoped
under [Distribution](Distribution.md); source integration is not deployed evidence.

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
