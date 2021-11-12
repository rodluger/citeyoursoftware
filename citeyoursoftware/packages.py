import subprocess
import yaml
import re


__all__ = ["get_packages"]


def get_user_packages(env_file="environment.yml", exclude=["python"]):
    """
    Returns a dictionary of packages listed by the user in a conda env file.

    """
    with open(env_file, "r") as f:
        info = yaml.safe_load(f)
    conda_channels = info.get("channels", ["defaults"])
    from_conda = [dep for dep in info.get("dependencies", []) if type(dep) is str]
    from_pypi = [
        item
        for sublist in [
            dep["pip"]
            for dep in info.get("dependencies", [])
            if type(dep) is dict and list(dep)[0] == "pip"
        ]
        for item in sublist
    ]
    packages = {}
    for source, channel in zip([from_conda, from_pypi], [conda_channels, "pypi"]):
        for package in source:
            # Is this a GitHub-hosted package?
            match = re.match("git\+https://github\.com/(.*?)/(.*?)\.git(.*?)$", package)
            if match is not None:
                user, name, _ = match.groups()
                version = None
                url = f"https://github\.com/{user}/{name}"
                if name not in exclude:
                    packages[name] = {"version": version, "channel": "git", "url": url}
            else:
                match = re.match("(.*?)([=<>!]+)(.*?)$", package)
                if match is not None:
                    name, operator, version = match.groups()
                    version = operator + version
                else:
                    name = package
                    operator = None
                    version = None
                if name not in exclude:
                    packages[name] = {
                        "version": version,
                        "channel": channel,
                        "url": None,
                    }
    return packages


def get_conda_packages(env_path=None):
    """
    Returns a dictionary of all packages in a given conda environment.

    """
    if env_path is None:
        info = subprocess.check_output(["conda", "list"])
    else:
        info = subprocess.check_output(["conda", "list", "-p", env_path])
    info = info.decode("utf-8").split("\n")
    packages = {}
    for line in info:
        if not line.startswith("#"):
            line = line.split(" ")
            package_info = []
            for entry in line:
                if len(entry):
                    package_info.append(entry)
            if len(package_info) == 3:
                name, version, _ = package_info
                channel = None
            elif len(package_info) == 4:
                name, version, _, channel = package_info
            else:
                continue
            packages[name] = {"version": version, "channel": channel}
    return packages


def get_packages(env_file="environment.yml", env_path=None, exclude=["python"]):
    """
    Returns a dictionary of packages listed by the user in a conda env file,
    annotated with the exact resolved version in the conda environment, the
    channel (conda, conda-forge, pypi, etc), and a url (which may be ``None``).

    Each entry in the dictionary has the format

    ```
    package_name : {
        "version": version,
        "channel": channel,
        "url": url
    }
    ```

    """
    # Get user-listed packages
    packages = get_user_packages(env_file=env_file, exclude=exclude)

    # Get all packages in the env
    conda_packages = get_conda_packages(env_path=env_path)

    # Update the user-defined list with exact versions and channels
    for package in packages:
        packages[package]["version"] = conda_packages[package]["version"]
        if conda_packages[package]["channel"] is not None:
            packages[package]["channel"] = conda_packages[package]["channel"]

    return packages