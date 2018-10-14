from os.path import exists as path_exists

import pytest

from pyscaffold.api import create_project
from pyscaffold.cli import parse_args

from pyscaffoldext.custom_extension.custom_extension import (
    InvalidProjectNameException
)


def test_naming_convention_project_name(tmpfolder):
    args = ["--namespace", "test.second_level",
            "--custom-extension", "some_extension"]
    with pytest.raises(InvalidProjectNameException):
        opts = parse_args(args)
        create_project(opts)


def test_naming_convention_package_name(tmpfolder):
    args = ["--namespace", "test.second_level",
            "--custom-extension", "pyscaffoldext-some_extension"]

    opts = parse_args(args)
    create_project(opts)
    assert not path_exists("pyscaffoldext-some_extension/src/pyscaffoldext/"
                           "some_extension")


def test_naming_convention_force(tmpfolder):
    args = ["--force", "--namespace", "test.second_level",
            "--custom-extension", "some_extension"]

    opts = parse_args(args)
    create_project(opts)
    assert not path_exists("pyscaffoldext-some_extension/src/pyscaffoldext/"
                           "some_extension")
