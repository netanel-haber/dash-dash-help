#!/usr/bin/env python3
"""Convert HTML table from index.html to markdown and update README."""

from html.parser import HTMLParser
from typing import List, Dict
import re


class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_thead = False
        self.in_tbody = False
        self.in_tr = False
        self.in_td = False
        self.in_th = False
        self.in_a = False
        self.in_code = False
        self.current_href = None
        self.current_cell = ""
        self.headers = []
        self.rows = []
        self.current_row = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag == "table" and attrs_dict.get("id") == "bench":
            self.in_table = True
        elif self.in_table:
            if tag == "thead":
                self.in_thead = True
            elif tag == "tbody":
                self.in_tbody = True
            elif tag == "tr":
                self.in_tr = True
                self.current_row = []
            elif tag == "th":
                self.in_th = True
                self.current_cell = ""
            elif tag == "td":
                self.in_td = True
                self.current_cell = ""
            elif tag == "a":
                self.in_a = True
                self.current_href = attrs_dict.get("href")
            elif tag == "code":
                self.in_code = True

    def handle_endtag(self, tag):
        if tag == "table":
            self.in_table = False
        elif tag == "thead":
            self.in_thead = False
        elif tag == "tbody":
            self.in_tbody = False
        elif tag == "tr":
            self.in_tr = False
            if self.in_thead and self.current_row:
                self.headers = self.current_row
            elif self.in_tbody and self.current_row:
                self.rows.append(self.current_row)
        elif tag == "th":
            self.in_th = False
            self.current_row.append(self.current_cell.strip())
        elif tag == "td":
            self.in_td = False
            self.current_row.append(self.current_cell.strip())
        elif tag == "a":
            self.in_a = False
            self.current_href = None
        elif tag == "code":
            self.in_code = False

    def handle_data(self, data):
        if self.in_th or self.in_td:
            if self.in_a and self.current_href:
                # Create markdown link
                self.current_cell += f"[{data}]({self.current_href})"
            elif self.in_code:
                # Keep code as backticks
                self.current_cell += f"`{data}`"
            else:
                self.current_cell += data


def parse_table(html_content: str) -> tuple[List[str], List[List[str]]]:
    """Parse HTML table and return headers and rows."""
    parser = TableParser()
    parser.feed(html_content)
    return parser.headers, parser.rows


def table_to_markdown(headers: List[str], rows: List[List[str]]) -> str:
    """Convert table data to markdown format."""
    # Filter out "hide-mobile" column (command)
    # Based on the HTML, column 1 is "command" which we'll keep

    md_lines = []

    # Header row
    md_lines.append("| " + " | ".join(headers) + " |")

    # Separator row
    md_lines.append("| " + " | ".join(["-" * len(h) for h in headers]) + " |")

    # Data rows
    for row in rows:
        md_lines.append("| " + " | ".join(row) + " |")

    return "\n".join(md_lines)


def update_readme(markdown_table: str):
    """Update README.md with the markdown table."""
    with open("README.md", "r") as f:
        readme = f.read()

    # Replace everything after the URL with the table and timestamp
    from datetime import datetime
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

    headers, rows = parse_table(html_content)
    markdown_table = table_to_markdown(headers, rows)
    update_readme(markdown_table)

    print("Updated README.md with markdown table")
