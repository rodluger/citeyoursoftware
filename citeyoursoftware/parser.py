import re


__all__ = ["find_bibtex_in_string"]


def get_closing_brace_index(string):
    """
    Returns the index of the last closing bracek `{` in a BibTeX entry.

    """
    count = 0
    for i, s in enumerate(string):
        if s == "{":
            count += 1
        elif s == "}":
            count -= 1
            if count == 0:
                return i
    return 0


def find_bibtex_in_string(string):
    """
    Returns a list of all valid BibTeX entries in a string.

    """
    bib = []
    while True:
        match = re.search("@[a-z,A-Z]*{", string)
        if match is None:
            break
        else:
            start = match.span()[0]
            length = get_closing_brace_index(string[start:])
            if length:
                bib.append(string[start : start + length + 1])
                string = string[start + length + 1 :]
            else:
                break
    return bib