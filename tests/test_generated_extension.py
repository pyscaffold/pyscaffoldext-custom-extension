from os.path import exists as path_exists

from pyscaffold.api import create_project
from pyscaffold.cli import parse_args, process_opts
from pyscaffold.utils import chdir


def test_generated_extension(tmpfolder, venv_run):
    args = ["--custom-extension", "pyscaffoldext-some_extension"]

    opts = parse_args(args)
    opts = process_opts(opts)
    create_project(opts)
    with chdir("pyscaffoldext-some_extension"):
        assert "" == venv_run("flake8")
        venv_run("python setup.py install")

    venv_run("putup --some-extension the_actual_project")
    assert path_exists("the_actual_project/setup.cfg")

    with chdir("the_actual_project"):
        assert "" == venv_run("flake8")


def test_generated_extension_without_prefix(tmpfolder, caplog):
    # Ensure prefix is added by default
    args = ["--custom-extension", "some_extension"]

    opts = parse_args(args)
    opts = process_opts(opts)
    create_project(opts)
    assert path_exists("pyscaffoldext-some_extension")

    # Ensure an explanation on how to use
    # `--force` to avoid preffixing is given
    logs = caplog.text
    assert "--force" in logs
