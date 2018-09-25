from os.path import exists as path_exists

from pyscaffold.api import create_project
from pyscaffold.cli import parse_args

from pyscaffoldext.custom_extension.custom_extension import CustomExtension


def test_add_custom_extension(tmpfolder):
    opts = {"package": "my_extension", "project": "my_project",
            "extensions": [CustomExtension("custom_ext")]}
    create_project(opts)
    assert path_exists("my_project/src/pyscaffoldext/"
                       "my_extension/my_extension.py")


def test_add_custom_extension_with_namespace(tmpfolder):
    args = ["--namespace", "test", "--custom-extension",
            "some_extension"]

    opts = parse_args(args)
    create_project(opts)
    assert path_exists("some_extension/src/pyscaffoldext/"
                       "test/some_extension/some_extension.py")


def test_add_custom_extension_with_namespace_2(tmpfolder):
    args = ["--namespace", "test.second_level",
            "--custom-extension", "some_extension"]

    opts = parse_args(args)
    create_project(opts)
    assert path_exists(
            "some_extension/src/pyscaffoldext/test/second_level/"
            "some_extension/some_extension.py")


def test_add_custom_extension_with_namespace_3(tmpfolder):
    args = ["--namespace", "test.second_level.third_level",
            "--custom-extension", "some_extension"]

    opts = parse_args(args)
    create_project(opts)
    assert path_exists(
            "some_extension/src/pyscaffoldext/test/second_level/"
            "third_level/some_extension/some_extension.py")
