from .parser import find_bibtex_in_string
from .github import get_github_bib
import requests
import re


__all__ = ["get_pypi_bib"]


def get_pypi_bib(package, version=None):
    """
    Scrapes the PyPI ``description`` field of a package for BibTeX entries.
    Returns a string.

    """
    if version is None:
        r = requests.get(f"https://pypi.org/pypi/{package}/json")
    else:
        r = requests.get(f"https://pypi.org/pypi/{package}/{version}/json")
    info = r.json()
    description = info.get("info", {}).get("description", "")

    # Look for the entry directly in the description
    bib = find_bibtex_in_string(description)

    # Try to find the GitHub URL anywhere in the ``info```
    results = re.findall(
        "https://github.com/([a-zA-Z0-9\-_]*)/([a-zA-Z0-9\-_]*)",
        str(info),
    )
    for user, repo in set(results):
        bib += get_github_bib(f"{user}/{repo}")
    return bib