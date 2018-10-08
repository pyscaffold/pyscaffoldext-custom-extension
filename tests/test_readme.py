from os.path import exists as path_exists

from pyscaffold.api import create_project
from pyscaffold.cli import parse_args


def test_readme(tmpfolder):
    args = ["--custom-extension", "pyscaffoldext-some_extension"]

    opts = parse_args(args)
    create_project(opts)
    assert path_exists("pyscaffoldext-some_extension/README.rst")
