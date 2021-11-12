from .pypi import get_pypi_bib
import argparse


def entry_point():

    # Command-line args
    parser = argparse.ArgumentParser(
        description="Generate BibTeX entries for a package."
    )
    parser.add_argument("packages", type=str, nargs="+")
    parser.add_argument("--channel", "-c", type=str, default="pypi")
    args = parser.parse_args()

    # Running list of entries
    bib = []

    # PyPI
    if args.channel == "pypi":
        for package in args.packages:
            bib += get_pypi_bib(package)

    # Output
    for b in bib:
        print(b)