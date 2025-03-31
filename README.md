# CalVer

The `calver` package is a [setuptools](https://pypi.org/p/setuptools) extension
for automatically defining your Python package version as a calendar version.

## Usage

First, ensure `calver` is present during the project's build step by specifying
it as one of the build requirements:

`pyproject.toml`:
```toml
[build-system]
requires = ["setuptools>=42", "calver"]
```

To enable generating the version automatically based on the date, add the
following to `setup.py`:

`setup.py`:
```python
from setuptools import setup

setup(
    ...
    use_calver=True,
    setup_requires=['calver'],
    ...
)
```

You can test that it is working with:

```console
$ python setup.py --version
2020.6.16
```

## Configuration

By default, when setting `use_calver=True`, it uses the following to generate
the version string:

```pycon
>>> import datetime
>>> datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y.%m.%d")
2020.6.16
```

You can override the format string by passing it instead of `True`:

`setup.py`:
```python
from setuptools import setup

setup(
    ...
    use_calver="%Y.%m.%d.%H.%M",
    setup_requires=['calver'],
    ...
)
```

You can override the current date/time by passing the environment variable
`SOURCE_DATE_EPOCH`, which should be a Unix timestamp in seconds. 
This is useful for reproducible builds (see https://reproducible-builds.org/docs/source-date-epoch/):

```console
env SOURCE_DATE_EPOCH=1743428011000 python setup.py --version
```

You can override this entirely by passing a callable instead, which will be called
with no arguments at build time:

`setup.py`:
```python
import datetime
from setuptools import setup

def long_now_version():
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    return now.strftime("%Y").zfill(5) + "." + now.strftime("%m.%d")

setup(
    ...
    use_calver=long_now_version,
    setup_requires=['calver'],
    ...
)
```
