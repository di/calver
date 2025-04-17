import datetime
import os

import pretend
import pytest

import calver.integration


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
