import datetime
import pathlib

DEFAULT_FORMAT = "%Y.%m.%d"

VERSION_FILE = '.calver-version'


def read_version_file(dist):
    # FIXME: Can we get the project directory?
    fn = pathlib.Path.cwd() / VERSION_FILE
    return fn.read_text()


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

    try:
        dist.metadata.version = read_version_file(dist)
    except FileNotFoundError:
        dist.metadata.version = generate_version()
