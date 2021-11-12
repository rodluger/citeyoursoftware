from citeyoursoftware.pypi import get_pypi_bib
from pybtex.database import parse_string


def test_emcee3():
    """
    Test scraping the PyPI ``description`` field for the ``emcee`` BibTeX entry.

    """
    bib = get_pypi_bib("emcee", version="3.1.1")[0]
    bib = parse_string(bib, "bibtex")
    assert bib.entries["emcee"].fields["title"] == "emcee: The MCMC Hammer"