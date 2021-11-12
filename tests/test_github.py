from citeyoursoftware.github import (
    get_github_citation_bib,
    get_github_citation_cff,
)
from pybtex.database import parse_string


def test_github_bib():
    """
    Test scraping a GitHub repo for a CITATION.bib file

    """
    bib = get_github_citation_bib(
        "scipy/scipy", "550b28e345623c79fa5a67a8873c3562326c0b3f"
    )
    bib = parse_string(bib, "bibtex")
    assert "SciPy" in bib.entries["2020SciPy-NMeth"].fields["title"]


def test_github_cff():
    """
    Test scraping a GitHub repo for a CITATION.cff file

    """
    bib = get_github_citation_cff(
        "rodluger/starry", "2f42236039d4835b123bb7016109a89b839aa673"
    )
    bib = parse_string(bib, "bibtex")
    assert bib.entries["starry"].fields["title"] == "starry"
