#!/usr/bin/env python3
"""Update a row in index.html by ID using proper HTML parsing."""

import argparse
import re
import sys
from html.parser import HTMLParser
from html import escape


def build_row(row_id: str, command: str, time_ms: int, version: str,
              version_url: str, run_url: str, install: str, pr: str = "-") -> str:
    """Build a table row HTML string."""
    css_class = "ok" if time_ms < 200 else "slow"
    return (
        f'<tr id="{row_id}">'
        f'<td><code>{escape(command)}</code></td>'
        f'<td class="{css_class}"><a href="{run_url}">{time_ms}ms</a></td>'
        f'<td><a href="{version_url}">{escape(version)}</a></td>'
        f'<td>{install}</td>'
        f'<td>{pr}</td>'
        f'</tr>'
    )


def update_row(html_content: str, row_id: str, new_row: str) -> str:
    """Replace a table row by ID in HTML content."""
    # Pattern to match <tr id="row_id">...</tr> including multiline content
    pattern = rf'<tr id="{re.escape(row_id)}"[^>]*>.*?</tr>'

    match = re.search(pattern, html_content, re.DOTALL)
    if not match:
        print(f"Error: Row with id='{row_id}' not found in HTML", file=sys.stderr)
        sys.exit(1)

    return html_content[:match.start()] + new_row + html_content[match.end():]


def main():
    parser = argparse.ArgumentParser(description="Update a row in index.html")
    parser.add_argument("--file", default="index.html", help="HTML file to update")
    parser.add_argument("--id", required=True, help="Row ID to update")
    parser.add_argument("--command", required=True, help="CLI command")
    parser.add_argument("--time-ms", type=int, required=True, help="Time in milliseconds")
    parser.add_argument("--version", required=True, help="Version string")
    parser.add_argument("--version-url", required=True, help="URL for version link")
    parser.add_argument("--run-url", required=True, help="URL for workflow run")
    parser.add_argument("--install", required=True, help="Install instructions (raw HTML)")
    parser.add_argument("--pr", default="-", help="PR link or dash")

    args = parser.parse_args()

    with open(args.file, "r") as f:
        html_content = f.read()

    new_row = build_row(
        row_id=args.id,
        command=args.command,
        time_ms=args.time_ms,
        version=args.version,
        version_url=args.version_url,
        run_url=args.run_url,
        install=args.install,
        pr=args.pr
    )

    updated_html = update_row(html_content, args.id, new_row)

    with open(args.file, "w") as f:
        f.write(updated_html)

    print(f"Updated row '{args.id}': {args.time_ms}ms @ {args.version}")


if __name__ == "__main__":
    main()
