# =================================================================
#
# Authors: Benjamin Webb <40066515+webb-ben@users.noreply.github.com>
#
# Copyright (c) 2025 Lincoln Institute of Land Policy
#
# Licensed under the MIT License.
#
# =================================================================

import sys
import subprocess
from pathlib import Path
from datetime import datetime

HEADER_TEMPLATE = """
# =================================================================
#
{authors}
#
# Copyright (c) {year} Lincoln Institute of Land Policy
#
# Licensed under the {license_type}.
#
# =================================================================
"""


def get_authors(filepath):
    """Retrieve unique authors from git log for a given file."""
    result = subprocess.run(
        ["git", "log", "--follow", "--format=%aN <%aE>", filepath],
        capture_output=True, text=True
    )
    authors = sorted(set(result.stdout.strip().split("\n")) - {''})
    return "\n".join(f"# Authors: {author}" for author in authors)


def get_latest_commit_year(filepath):
    """Retrieve the most recent commit year for the file."""
    result = subprocess.run(
        ["git", "log", "-1", "--format=%ad", "--date=format:%Y", filepath],
        capture_output=True, text=True
    )
    return result.stdout.strip() or str(datetime.now().year)


def get_license_type():
    """Read the LICENSE file and determine the license type."""
    license_path = Path("LICENSE")
    if not license_path.exists():
        return "MIT License"  # Default to MIT if no LICENSE file is found

    content = license_path.read_text().lower()
    if "mit license" in content:
        return "MIT License"
    elif "apache license" in content:
        return "Apache License 2.0"
    elif "gnu general public license" in content:
        return "GNU General Public License"
    elif "bsd license" in content:
        return "BSD License"
    else:
        return "Unknown License"


def process_file(filepath):
    """Add or update the copyright header in a file."""
    path = Path(filepath)
    content = path.read_text().splitlines()

    authors = get_authors(filepath)
    year = get_latest_commit_year(filepath)
    license_type = get_license_type()

    new_header = HEADER_TEMPLATE.format(
        authors=authors,
        year=year,
        license_type=license_type
    ).strip()

    # Check if the file already has a header
    header_end_idx = -1
    found = False
    for i, line in enumerate(content):  # Look in the first 10 lines
        if line.strip() == "# =================================================================": # noqa
            if found:
                header_end_idx = i + 1
                break
            else:
                found = True

    if found:
        # Modify or prepend header
        if header_end_idx > 0:
            content = content[header_end_idx:]  # Remove existing header

        path.write_text(new_header + "\n" + "\n".join(content) + "\n")


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        process_file(filename)
