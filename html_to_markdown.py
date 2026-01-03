#!/usr/bin/env python3
"""Convert HTML table from index.html to markdown and update README."""

import re
from datetime import datetime
from markdownify import markdownify as md


def extract_table(html_content: str) -> str:
    """Extract the benchmark table from HTML."""
    # Find the table with id="bench"
    match = re.search(
        r'<table id="bench">.*?</table>',
        html_content,
        re.DOTALL
    )
    if not match:
        raise ValueError("Could not find table with id='bench'")
    return match.group(0)


def clean_markdown_table(markdown: str) -> str:
    """Clean up the markdown table."""
    # Remove extra whitespace and clean up formatting
    lines = [line.strip() for line in markdown.strip().split('\n') if line.strip()]
    return '\n'.join(lines)


def update_readme(markdown_table: str):
    """Update README.md with the markdown table."""
    with open("README.md", "r") as f:
        readme = f.read()

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    # Split at the dashdashhelp.win URL line
    parts = readme.split("https://dashdashhelp.win\n")
    if len(parts) == 2:
        new_readme = (
            parts[0] +
            "https://dashdashhelp.win\n\n" +
            markdown_table + "\n\n" +
            f"Last updated: {timestamp}\n"
        )

        with open("README.md", "w") as f:
            f.write(new_readme)


if __name__ == "__main__":
    with open("index.html", "r") as f:
        html_content = f.read()

    table_html = extract_table(html_content)
    markdown_table = md(table_html, heading_style="ATX")
    markdown_table = clean_markdown_table(markdown_table)
    update_readme(markdown_table)

    print("Updated README.md with markdown table")
