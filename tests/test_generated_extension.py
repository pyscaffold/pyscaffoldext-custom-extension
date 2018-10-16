import os
from subprocess import call

from pyscaffold.api import create_project
from pyscaffold.cli import parse_args


def test_generated_extension(tmpfolder):
    args = ["--custom-extension", "pyscaffoldext-some_extension"]

    opts = parse_args(args)
    create_project(opts)
    os.chdir("pyscaffoldext-some_extension")
    flake8_extension_res = call("flake8")
    assert flake8_extension_res == 0

    call(["python", "setup.py", "install"])
    os.chdir("..")
    call(["putup", "--some-extension", "the_actual_project"])
    assert os.path.exists("the_actual_project/setup.cfg")

    os.chdir("the_actual_project")
    flake8_project_res = call("flake8")
    assert flake8_project_res == 0
