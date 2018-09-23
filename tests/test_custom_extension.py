from pyscaffold.api import create_project

from os.path import exists as path_exists
from os import listdir
from pyscaffoldext.custom_extension.custom_extension import CustomExtension
from pyscaffold.extensions.no_skeleton import NoSkeleton
from pyscaffold.cli import parse_args

def test_add_custom_extension(tmpfolder):

    opts ={"package": "my_extension", "project": "my_project",
            "extensions":[CustomExtension("custom_ext"), NoSkeleton("no")]}
    create_project(opts)
    print(listdir("my_project/src"))
    assert path_exists("my_project/src/pyscaffoldext/my_extension/my_extension.py")

def test_add_custom_extension_with_namespace(tmpfolder):


    args = [ "--namespace", "test", "--custom-extension", "some_extension"]

    opts = parse_args(args)
    create_project(opts)
    assert path_exists("some_extension/src/pyscaffoldext/test/some_extension/some_extension.py")