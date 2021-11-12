from .parser import find_bibtex_in_string
import requests


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
    return find_bibtex_in_string(description)