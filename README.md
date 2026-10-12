# WeWorkTogether

A small, public starter repository for collaborating on GitHub through clear issues, focused pull requests, and reproducible changes.

## Purpose

The goal is to make it easy for a contributor to understand an improvement, implement it on a separate branch, verify the result, and leave enough evidence for another person to reproduce it.

This repository starts with lightweight documentation rather than a specific application or framework.

## Working agreement

- **One change per pull request.** Keep unrelated fixes separate.
- **Evidence over assumptions.** State what you tested and what is still unknown.
- **Make changes reversible.** Avoid force-pushing shared branches or rewriting history.
- **Be respectful.** Explain disagreements in terms of observable behavior.
- **Protect secrets.** Never commit tokens, passwords, private keys, or personal data.

## Collaboration workflow

1. Describe a genuine problem or improvement in an issue, including acceptance criteria.
2. Create a feature branch from the default branch.
3. Make and verify the smallest complete change.
4. Open a pull request with a summary, test evidence, and any risks.
5. Merge only when the checks appropriate to the change have passed.

## Repository structure

- [`README.md`](README.md) — project purpose and lightweight collaboration workflow.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — detailed contributor instructions.
- [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md) — change description and verification checklist.
- [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE) — structured improvement proposals and bug reports.

## Contributing

Documentation improvements, practical examples, and small reusable collaboration tools are welcome. Read [the contribution guide](CONTRIBUTING.md) before opening a pull request. Explain why the change is useful and how it was checked.

## Looking for contributors

**First collaboration opportunity:** [Build an offline Markdown link checker (issue #2)](https://github.com/HFAsif/WeWorkTogether/issues/2).

A contributor can help build a small Python 3 tool to check local documentation links without external dependencies. The [draft pull request #3](https://github.com/HFAsif/WeWorkTogether/pull/3) already includes a design and eight acceptance tests. The checker implementation, CI workflow, documentation, and genuine collaborative review are still needed.

If interested, comment on issue #2 with what you would like to work on. No prior relationship with the maintainer is necessary. Please read [CONTRIBUTING.md](CONTRIBUTING.md) and use a fork or coordinate branch access before changing code. Actual contributions will be credited accurately.

## Security

If you discover a sensitive vulnerability, avoid posting exploit details or credentials in a public issue. Contact the maintainer through an appropriate private channel.

## Beginner-Friendly Usage

The tool should be simple enough for beginners.

Users should be able to check links with one command.

Broken links should display clear error messages.

No extra software packages should be required.
