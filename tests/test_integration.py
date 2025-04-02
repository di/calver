import datetime

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


@pytest.mark.parametrize("value", [None, False, ""])
def test_version_missing(dist, keyword, original_version, value):
    calver.integration.version(dist, keyword, value)

    assert dist.metadata.version == original_version


def test_version_true(dist, keyword, ignore_pkginfo):
    value = True

    calver.integration.version(dist, keyword, value)

    assert dist.metadata.version == datetime.datetime.now().strftime(
        calver.integration.DEFAULT_FORMAT
    )


def test_version_str(dist, keyword, ignore_pkginfo):
    value = "%c"

    calver.integration.version(dist, keyword, value)

    assert dist.metadata.version == datetime.datetime.utcnow().strftime(value)


def test_version_callable(dist, keyword, ignore_pkginfo):
    v = pretend.stub()

    calver.integration.version(dist, keyword, lambda: v)

    assert dist.metadata.version == v


def test_reads_pkginfo(dist, keyword, monkeypatch):
    pkginfo_contents = "Version: 42"
    monkeypatch.setattr(
        calver.integration, "get_pkginfo_contents", lambda: pkginfo_contents
    )

    calver.integration.version(dist, keyword, True)

    assert dist.metadata.version == "42"


def test_reproducible_build(dist, keyword, source_date_epoch, ignore_pkginfo):
    calver.integration.version(dist, keyword, True)

    assert dist.metadata.version == datetime.datetime.fromtimestamp(
        source_date_epoch, tz=datetime.timezone.utc
    ).strftime(calver.integration.DEFAULT_FORMAT)
