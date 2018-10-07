from os.path import exists as path_exists

from pyscaffold.api import create_project
from pyscaffold.cli import parse_args


def test_no_skeleton(tmpfolder):
    args = ["--custom-extension", "pyscaffoldext-some_extension"]

    opts = parse_args(args)
    create_project(opts)

    assert not path_exists("pyscaffoldext-some_extension/src/pyscaffoldext/"
                           "some_extension/skeleton.py")


def test_tox(tmpfolder):
    args = ["--custom-extension", "pyscaffoldext-some_extension"]

    opts = parse_args(args)
    create_project(opts)
    assert path_exists("pyscaffoldext-some_extension/tox.ini")


def test_pre_commit(tmpfolder):
    args = ["--custom-extension", "pyscaffoldext-some_extension"]

    opts = parse_args(args)
    create_project(opts)

    assert path_exists("pyscaffoldext-some_extension/.pre-commit-config.yaml")
