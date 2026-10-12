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

## Check documentation links

Use the [offline Markdown link checker](scripts/check_md_links.py) to find missing local links and image targets in documentation. It uses Python 3's standard library, so no extra packages, internet connection, or GitHub token are required.

### One-command quick start

From the repository root, run:

~~~sh
python scripts/check_md_links.py
~~~

A successful scan displays a message such as:

~~~text
OK: checked 3 Markdown file(s); no broken local links.
~~~

For a broken link, the checker prints the affected file, line number, and target, for example:

~~~text
README.md:12: missing local link: missing-guide.md
~~~

The command returns exit code **0** when local links exist and **1** when a target is missing. It does not test whether external web links are reachable.

To check a different folder, run `python scripts/check_md_links.py --root path/to/project`. To run the automated checks, use:

~~~sh
python -m unittest discover -s tests -v
~~~

For supported formats and limitations, see the [checker design](docs/link-checker-design.md).

## Contributing

Documentation improvements, practical examples, and small reusable collaboration tools are welcome. Read [the contribution guide](CONTRIBUTING.md) before opening a pull request. Explain why the change is useful and how it was checked.

## Looking for contributors

Our first feature, the offline Markdown checker, was implemented and merged in [PR #3](https://github.com/HFAsif/WeWorkTogether/pull/3). The beginner-friendly documentation ideas and formatting were contributed by [HFImran in PR #4](https://github.com/HFAsif/WeWorkTogether/pull/4); this guide connects those usability goals to a tested command.

Contributions and real improvements remain welcome. Before proposing a change, read [CONTRIBUTING.md](CONTRIBUTING.md), review existing issues, and open a focused PR describing what you verified.

## Security

If you discover a sensitive vulnerability, avoid posting exploit details or credentials in a public issue. Contact the maintainer through an appropriate private channel.

## Beginner-Friendly Usage

The core usability requirements contributed in [HFImran's PR #4](https://github.com/HFAsif/WeWorkTogether/pull/4) are:

- Simple enough for a beginner: open a terminal in the repository folder and run **one command**.
- Detect broken relative Markdown links automatically.
- Show clear errors telling the user which file, line, and target are broken.
- Work without installing additional Python packages.

The **One-command quick start** above demonstrates these requirements with the checker implemented in PR #3.
