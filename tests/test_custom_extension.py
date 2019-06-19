from os.path import exists as path_exists

from pyscaffold.api import create_project
from pyscaffold.cli import parse_args, process_opts

from pyscaffoldext.custom_extension.extension import NamespaceError

import pytest


def test_add_custom_extension(tmpfolder):
    args = ["pyscaffoldext-my_project", "--custom-extension",
            "--package", "my_extension"]
    opts = parse_args(args)
    opts = process_opts(opts)
    create_project(opts)
    assert path_exists("pyscaffoldext-my_project/src/pyscaffoldext/"
                       "my_extension/extension.py")


def test_add_custom_extension_with_namespace(tmpfolder):
    # we expect the second namespace to be just ignored
    args = ["--namespace", "test", "--custom-extension",
            "pyscaffoldext-some_extension"]
    opts = parse_args(args)
    opts = process_opts(opts)
    with pytest.raises(NamespaceError):
        create_project(opts)
