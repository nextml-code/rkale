from pathlib import Path

import pytest
from rkale import __version__
from rkale.config import path
from rkale.exceptions import DataRootError
from rkale.project_operations import get_destinations
from rkale.utils import check_paths


def test_version():
    assert __version__ == "0.2.6"


def test_path():
    assert path(Path("test"), "sub_test") == Path("test/sub_test").resolve()
    with pytest.raises(DataRootError):
        path(Path("test"), "../sub_test")


def test_get_destinations():
    assert get_destinations("root", "remote", "dataset", True) == (
        "root/dataset",
        "remote:/dataset",
    )
    assert get_destinations("root", "remote", "dataset", False) == (
        "remote:/dataset",
        "root/dataset",
    )


def test_check_paths():
    check_paths([("~/test", "remote:/test")])
    with pytest.raises(DataRootError):
        check_paths([("~/test", "remote:")])
    with pytest.raises(DataRootError):
        check_paths([("~", "remote:/test")])
