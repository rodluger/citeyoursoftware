from .parser import find_bibtex_in_string
import requests
from urllib.request import Request, urlopen
import os
import json
import subprocess


__all__ = ["get_github_bib"]


API_KEY = os.getenv("GH_API_KEY", None)


def get_github_citation_cff(slug, commit_ish=None):
    """
    Scrapes a GitHub repo for a CITATION.cff and converts it to BibTeX.

    Note that the current approach doesn't output `preferred-citation`

        https://github.com/citation-file-format/cff-converter-python/issues/158

    and it names the reference `YourReferenceHere`.

    """
    if commit_ish is None:
        # Get the default branch name
        req = Request(f"https://api.github.com/repos/{slug}")
        req.add_header("Accept", "application/vnd.github.v3+json")
        req.add_header("Authorization", f"token {API_KEY}")
        resp = urlopen(req)
        content = resp.read()
        content = json.loads(content)
        commit_ish = content["default_branch"]

    # Look for a `CITATION.cff` file & download it
    r = requests.get(
        f"https://raw.githubusercontent.com/{slug}/{commit_ish}/CITATION.cff"
    )
    if r.status_code < 400:
        cff = r.content.decode("utf-8")
        with open(".CITATION_TEMP.cff", "w") as f:
            print(cff, file=f)

        # Convert to BibTex
        bib = subprocess.check_output(
            ["cffconvert", "-i", ".CITATION_TEMP.cff", "-f", "bibtex"]
        ).decode("utf-8")
        os.remove(".CITATION_TEMP.cff")

        # Replace the placeholder name with the package name
        repo = slug.split("/")[1]
        bib = bib.replace("YourReferenceHere", repo)

        # Parse into a list
        bib = find_bibtex_in_string(bib)
    else:
        bib = []

    return bib


def get_github_citation_bib(slug, commit_ish=None):
    """
    Scrapes a GitHub repo for a CITATION.bib file.

    """
    if commit_ish is None:
        # Get the default branch name
        req = Request(f"https://api.github.com/repos/{slug}")
        req.add_header("Accept", "application/vnd.github.v3+json")
        req.add_header("Authorization", f"token {API_KEY}")
        resp = urlopen(req)
        content = resp.read()
        content = json.loads(content)
        commit_ish = content["default_branch"]

    # Look for a `CITATION.bib` file & download it
    r = requests.get(
        f"https://raw.githubusercontent.com/{slug}/{commit_ish}/CITATION.bib"
    )
    if r.status_code < 400:
        bib = find_bibtex_in_string(r.content.decode("utf-8"))
    else:
        bib = []

    return bib


def get_github_citation_astropy(slug, commit_ish=None):
    """
    Scrapes a GitHub repo for a repo/CITATION file (astropy convention).

    """
    if commit_ish is None:
        # Get the default branch name
        req = Request(f"https://api.github.com/repos/{slug}")
        req.add_header("Accept", "application/vnd.github.v3+json")
        req.add_header("Authorization", f"token {API_KEY}")
        resp = urlopen(req)
        content = resp.read()
        content = json.loads(content)
        commit_ish = content["default_branch"]

    # Look for a `{repo}/CITATION` file & download it
    repo = slug.split("/")[1]
    r = requests.get(
        f"https://raw.githubusercontent.com/{slug}/{commit_ish}/{repo}/CITATION"
    )
    if r.status_code < 400:
        bib = find_bibtex_in_string(r.content.decode("utf-8"))
    else:
        bib = []

    return bib


def get_github_bib(slug, commit_ish=None):
    """
    Scrapes a GitHub repo for citation information. Returns a BibTeX string.

    """
    return (
        get_github_citation_cff(slug, commit_ish)
        + get_github_citation_bib(slug, commit_ish)
        + get_github_citation_astropy(slug, commit_ish)
    )
