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

## Security

If you discover a sensitive vulnerability, avoid posting exploit details or credentials in a public issue. Contact the maintainer through an appropriate private channel.
