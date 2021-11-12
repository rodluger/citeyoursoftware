from .packages import get_packages
from .pypi import get_pypi_bib


def get_bibliography(
    env_file="environment.yml", env_path=None, exclude=["python"]
):

    # Get all user-listed packages w/ channels & exact versions
    packages = get_packages(env_file=env_file, env_path=None)

    # Try to find BibTeX entries for all packages
    for name in packages:
        packages[name]["bib"] = []
        version = packages[name]["version"]
        channel = packages[name]["channel"]

        if channel == "pypi":
            packages[name]["bib"] += get_pypi_bib(name, version)

        # TODO!!!

    return packages