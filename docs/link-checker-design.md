# Offline Markdown link checker: collaboration design

Related issue: [#2](https://github.com/HFAsif/WeWorkTogether/issues/2).

## Motivation

The repository's README and contributor instructions refer to local documentation files. A small, deterministic checker can catch broken relative links before a documentation change is merged. It must run with standard Python 3 and no network access.

## Command line

```sh
python scripts/check_md_links.py
python scripts/check_md_links.py --root path/to/docs-project
python -m unittest discover -s tests -v
```

When `--root` is omitted, use the repository containing the script, not the caller's current working directory. When it is supplied, recursively scan the supplied directory for `*.md` files.

Exit status:

- `0`: no missing local targets found.
- `1`: at least one missing local target found; include the source filename and missing target in readable output.
- `2` (optional): invalid command line or inaccessible root, with a useful error.

Print one diagnostic per broken link. Filenames should be relative to the scan root where possible. Include a source line number if the parser can reliably provide it. Multiple broken links should all be reported during a single scan.

## Links to check

Recognize ordinary inline Markdown links and images:

```md
[contributor guide](CONTRIBUTING.md)
![logo](assets/logo.png)
[design](docs/design.md#scope)
[encoded](guide%20one.md?preview=1)
```

Resolve the path relative to the file containing the Markdown link. URL-decode local target paths and ignore query strings and fragments when testing existence. A target is valid if it names an existing file **or directory**.

Ignore external links (`http://`, `https://`, `mailto:`, protocol-relative URLs such as `//example.org`) and fragment-only links (`#scope`). Do not treat link-looking text within fenced code blocks as links. Triple backtick fences must be supported; supporting tildes is a welcome extension.

Use simple, readable parsing for v1. Full CommonMark parsing, reference-link definitions, online link checks, and in-page heading validation are out of scope.

## Test contract

The tests call:

```text
python scripts/check_md_links.py --root <temporary-directory>
```

Temporary fixture directories contain Markdown files with valid and invalid links. Tests assert the exit code and require broken-link output to include its source Markdown filename and missing path. Tests use only the standard library and do not contact external services.

These tests deliberately precede the checker implementation, so a missing-script failure on this **draft** branch is expected until the collaborator implements it.

## Work split and honest co-authorship

HFAsif prepared the issue/specification and first acceptance tests. A real collaborator can implement the checker and CI workflow and improve tests. The two should review a shared change together, including at least one substantive fix, before labeling any *single commit* as co-authored. Credit a collaborator using the GitHub-linked/noreply email they provide privately. Do not add a co-author trailer solely to obtain an achievement.

Keep the draft PR unmerged until implementation, reproducible tests, and attribution have been reviewed.
