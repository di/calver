import datetime

import pretend
import pytest

from calver.integration import DEFAULT_FORMAT, version


@pytest.fixture
def original_version():
    return pretend.stub()


@pytest.fixture
def dist(original_version):
    return pretend.stub(
        metadata=pretend.stub(version=original_version),
        cmdclass={},
        src_root=None,
    )


@pytest.fixture
def keyword():
    return pretend.stub()


@pytest.mark.parametrize("value", [None, False, ""])
def test_version_missing(dist, keyword, original_version, value):
    version(dist, keyword, value)

    assert dist.metadata.version == original_version


def test_version_true(dist, keyword):
    value = True

    version(dist, keyword, value) is None

    assert dist.metadata.version == datetime.datetime.now().strftime(DEFAULT_FORMAT)


def test_version_str(dist, keyword):
    value = "%c"

    version(dist, keyword, value) is None

    assert dist.metadata.version == datetime.datetime.now().strftime(value)


def test_version_callable(dist, keyword):
    ver = pretend.stub()
    value = lambda: ver

    version(dist, keyword, value) is None

    assert dist.metadata.version == ver


def test_run_twice(dist, keyword):
    value = True

    version(dist, keyword, value)
    version(dist, keyword, value)
