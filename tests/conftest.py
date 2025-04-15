import os

import pretend
import pytest

import calver.integration


@pytest.fixture
def original_version():
    return pretend.stub()


@pytest.fixture
def dist(original_version):
    return pretend.stub(metadata=pretend.stub(version=original_version))


@pytest.fixture
def keyword():
    return pretend.stub()


@pytest.fixture
def ignore_pkginfo(monkeypatch):
    # Ensure that the test doesn't unintently prefer to read from a PKG_INFO
    # that might exist in the source directory, e.g. when testing a sdist
    # https://github.com/di/calver/issues/20
    monkeypatch.setattr(
        calver.integration, "get_pkginfo_contents", pretend.raiser(FileNotFoundError)
    )


@pytest.fixture
def source_date_epoch(monkeypatch):
    _source_date_epoch = 1234567890
    monkeypatch.setenv("SOURCE_DATE_EPOCH", str(_source_date_epoch))
    yield _source_date_epoch
    monkeypatch.delenv("SOURCE_DATE_EPOCH")
