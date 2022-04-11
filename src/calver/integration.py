import datetime
import os

DEFAULT_FORMAT = "%Y.%m.%d"


def get_pkginfo_contents():
    path = os.path.join(os.path.abspath("."), "PKG-INFO")
    with open(path, encoding="utf-8") as fp:
        return fp.read()


def pkginfo_version():
    try:
        content = get_pkginfo_contents()
    except FileNotFoundError:
        return

    data = dict(x.split(": ", 1) for x in content.splitlines() if ": " in x)

    version = data.get("Version")
    if version != "UNKNOWN":
        return version


def _get_version(value):
    if not value:
        return
    elif value is True:
        generate_version = lambda: datetime.datetime.now().strftime(DEFAULT_FORMAT)
    elif isinstance(value, str):
        generate_version = lambda: datetime.datetime.now().strftime(value)
    elif getattr(value, "__call__", None):
        generate_version = value
    else:
        return

    return pkginfo_version() or generate_version()


def version(dist, keyword, value):
    _version = _get_version(value)

    if _version:
        dist.metadata.version = _version
