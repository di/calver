import os
import sys

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


def calver_version(value):
    src = os.path.join(here, "src")

    sys.path.insert(0, src)

    from calver.integration import _get_version

    return _get_version(value)


setup(
    name="calver",
    description="Setuptools extension for CalVer package versions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/di/calver",
    author="Dustin Ingram",
    author_email="di@python.org",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
    ],
    keywords="calver",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.5",
    entry_points={
        "distutils.setup_keywords": [
            "use_calver = calver.integration:version",
        ],
    },
    version=calver_version(True),
)
