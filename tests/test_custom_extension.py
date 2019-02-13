from os.path import exists as path_exists

from pyscaffold.api import create_project
from pyscaffold.cli import parse_args

from pyscaffoldext.custom_extension.extension import CustomExtension


def test_add_custom_extension(tmpfolder):
    opts = {"package": "my_extension", "project": "pyscaffoldext-my_project",
            "extensions": [CustomExtension("custom_ext")]}
    create_project(opts)
    assert path_exists("pyscaffoldext-my_project/src/pyscaffoldext/"
                       "my_extension/extension.py")


def test_add_custom_extension_with_namespace(tmpfolder):
    # we expect the second namespace to be just ignored
    args = ["--namespace", "test", "--custom-extension",
            "pyscaffoldext-some_extension"]

    opts = parse_args(args)
    create_project(opts)
    assert path_exists("pyscaffoldext-some_extension/src/pyscaffoldext"
                       "/some_extension/extension.py")
