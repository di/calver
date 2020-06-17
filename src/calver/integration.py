import datetime

DEFAULT_FORMAT = "%Y.%m.%d"


def version(dist, keyword, value):
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

    dist.metadata.version = generate_version()
