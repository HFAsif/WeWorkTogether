#!/usr/bin/env python3
"""Check relative inline Markdown links and images without network access.

This is a deliberately small checker, not a full CommonMark parser.
See docs/link-checker-design.md for the supported input subset.
"""

import argparse
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


INLINE_LINK = re.compile(
    r'!?\[[^\]\n]*\]\(\s*(?:<(?P<angle>[^>\n]+)>|(?P<plain>[^\s)]+))'
    r'(?:\s+["\'][^"\']*["\'])?\s*\)'
)
FENCE = re.compile(r'^ {0,3}(?P<marks>\x60{3,}|~{3,})')
URI_SCHEME = re.compile(r'^[a-zA-Z][a-zA-Z0-9+.-]*:')
INLINE_CODE_DELIMITERS = re.compile(r'\x60+')
SKIP_DIRS = {'.git', '.venv', 'venv', '__pycache__', 'node_modules'}


def link_targets(line: str):
    """Return local path strings from basic inline links/images on one line."""
    for match in INLINE_LINK.finditer(line):
        raw = match.group('angle') or match.group('plain')
        if not raw or raw.startswith(('#', '//')) or URI_SCHEME.match(raw):
            continue
        target = unquote(urlsplit(raw).path)
        if target:
            yield raw, target


def mask_inline_code(line: str) -> str:
    """Blank out complete backtick code spans before finding Markdown links."""
    runs = list(INLINE_CODE_DELIMITERS.finditer(line))
    masked = list(line)
    index = 0
    while index < len(runs):
        opening = runs[index]
        closing = next((
            j for j in range(index + 1, len(runs))
            if len(runs[j].group()) == len(opening.group())
        ), None)
        if closing is None:
            index += 1
            continue
        end = runs[closing].end()
        masked[opening.start():end] = ' ' * (end - opening.start())
        index = closing + 1
    return ''.join(masked)


def missing_links(markdown_file: Path):
    """Yield (source line, raw target) for broken local destinations."""
    try:
        lines = markdown_file.read_text(encoding='utf-8-sig').splitlines()
    except (OSError, UnicodeError) as exc:
        raise ValueError(f'{markdown_file}: unable to read UTF-8 Markdown: {exc}') from exc

    fenced_char = None
    fenced_len = 0
    for line_number, line in enumerate(lines, start=1):
        match = FENCE.match(line)
        if match:
            marks = match.group('marks')
            if fenced_char is None:
                fenced_char, fenced_len = marks[0], len(marks)
                continue
            if marks[0] == fenced_char and len(marks) >= fenced_len:
                fenced_char, fenced_len = None, 0
                continue
        if fenced_char is not None:
            continue
        for raw, target in link_targets(mask_inline_code(line)):
            target_path = markdown_file.parent / Path(target)
            if not target_path.exists():
                yield line_number, raw


def scan(root: Path) -> int:
    checked_files = 0
    bad_links = 0
    for markdown_file in sorted(root.rglob('*.md')):
        if any(part in SKIP_DIRS for part in markdown_file.relative_to(root).parts):
            continue
        checked_files += 1
        for line_number, target in missing_links(markdown_file):
            bad_links += 1
            print(f'{markdown_file.relative_to(root)}:{line_number}: missing local link: {target}')
    if bad_links:
        print(f'{bad_links} broken local link(s) in {checked_files} Markdown file(s).')
        return 1
    print(f'OK: checked {checked_files} Markdown file(s); no broken local links.')
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1],
                        help='folder to scan (default: repository root)')
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if not root.is_dir():
        print(f'Invalid Markdown scan directory: {root}', file=sys.stderr)
        return 2
    try:
        return scan(root)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
