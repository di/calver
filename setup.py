import os
import sys

from setuptools import setup


def calver_version(value):
    here = os.path.abspath(os.path.dirname(__file__))
    src = os.path.join(here, "src")

    sys.path.insert(0, src)

    from calver.integration import _get_version

    return _get_version(value)


setup(
    version=calver_version(True),
)
