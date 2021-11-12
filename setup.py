"""Install script for `citeyoursoftware`."""
import os
from setuptools import find_packages, setup

setup(
    name="citeyoursoftware",
    author="Rodrigo Luger",
    author_email="rodluger@gmail.com",
    url="https://github.com/rodluger/citeyoursoftware",
    description="a tool for automatic software citations",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    use_scm_version={
        "write_to": os.path.join(
            "citeyoursoftware", "citeyoursoftware_version.py"
        ),
        "write_to_template": '__version__ = "{version}"\n',
    },
    install_requires=["setuptools_scm", "pyyaml", "pybtex"],
    entry_points={
        "console_scripts": ["cyfs=citeyoursoftware.main:entry_point"]
    },
    setup_requires=["setuptools_scm"],
    include_package_data=True,
    zip_safe=False,
)
