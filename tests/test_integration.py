import datetime

import pytest
import pretend

from calver.integration import version, DEFAULT_FORMAT


@pytest.fixture
def original_version():
    return pretend.stub()


@pytest.fixture
def dist(original_version):
    return pretend.stub(metadata=pretend.stub(version=original_version))


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
    v = pretend.stub()
    value = lambda: v

    version(dist, keyword, value) is None

    assert dist.metadata.version == v
