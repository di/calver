import datetime
import os

from . import commands

DEFAULT_FORMAT = "%Y.%m.%d"

VERSION_FILE = '.calver-version'


def read_version_file(dist):
    # FIXME: Can we get the project directory?
    src = dist.src_root or os.getcwd()
    fn = os.path.join(src, VERSION_FILE)
    with open(fn, 'rt') as f:
        return f.read()


def version(dist, keyword, value):
    if not value:
        return
    elif value is True:
        generate_version = lambda: datetime.datetime.now().strftime(DEFAULT_FORMAT)  # noqa: E501
    elif isinstance(value, str):
        generate_version = lambda: datetime.datetime.now().strftime(value)
    elif getattr(value, "__call__", None):
        generate_version = value
    else:
        return

    assert 'sdist' not in dist.cmdclass, "FIXME: Handle an already-overridden sdist"
    dist.cmdclass['sdist'] = commands.sdist

    try:
        dist.metadata.version = read_version_file(dist)
    except FileNotFoundError:
        dist.metadata.version = generate_version()
