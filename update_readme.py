#!/usr/bin/env python3
import csv
from datetime import datetime
from pathlib import Path


def csv_to_markdown_table() -> str:
    """Read measurements.csv and generate a markdown table."""
    rows = []
    with open("measurements.csv", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(
                f"| {row['library']} "
                f"| [{row['cold_ms']}ms]({row['run_url']}) "
                f"| [{row['warm_ms']}ms]({row['run_url']}) "
                f"| [{row['version']}]({row['version_url']}) "
                f"| {row['last_updated']} |"
            )

    header = "| library | cold | warm (10 runs) | version | measured on |"
    separator = "| --- | --- | --- | --- | --- |"
    return "\n".join([header, separator] + rows)


def update_readme(markdown_table: str):
    """Update README.md with the markdown table."""
    readme_path = Path("README.md")
    readme = readme_path.read_text()

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    # Split at the dashdashhelp.win URL line
    parts = readme.split("https://dashdashhelp.win\n")
    if len(parts) == 2:
        new_readme = (
            parts[0]
            + "https://dashdashhelp.win\n\n"
            + markdown_table
            + "\n\n"
            + f"Last updated: {timestamp}\n"
        )

        readme_path.write_text(new_readme)


if __name__ == "__main__":
    markdown_table = csv_to_markdown_table()
    update_readme(markdown_table)

    print("Updated README.md with markdown table")
