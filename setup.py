# =================================================================
#
# Authors: Benjamin Webb <40066515+webb-ben@users.noreply.github.com>
#
# Copyright (c) 2025 Lincoln Institute of Land Policy
#
# Licensed under the MIT License.
#
# =================================================================

from setuptools import setup
from pathlib import Path


def read(filename):
    """read file contents"""

    fullpath = Path(__file__).resolve().parent / filename

    with fullpath.open() as fh:
        contents = fh.read().strip()

    return contents


setup(
    name="pre-commit-hooks",
    version="0.1.0",
    py_modules=["src.add_header"],
    entry_points={
        "console_scripts": [
            "add-header=src.add_header:main",
        ],
    },
    install_requires=read('requirements.txt').splitlines(),
)
