import logging
from pathlib import Path

from pyscaffold import cli
from pyscaffold.file_system import chdir


def test_generated_extension(tmpfolder, venv_run):
    args = ["--no-config", "--custom-extension", "pyscaffoldext-some_extension"]
    # --no-config: avoid extra config from dev's machine interference

    cli.main(args)
    with chdir("pyscaffoldext-some_extension"):
        assert "" == venv_run("flake8")
        venv_run("python setup.py install")

    venv_run("putup --some-extension the_actual_project")
    assert Path("the_actual_project/setup.cfg").exists()

    with chdir("the_actual_project"):
        assert "" == venv_run("flake8")


def test_generated_extension_without_prefix(tmpfolder, caplog):
    caplog.set_level(logging.WARNING)
    # Ensure prefix is added by default
    args = ["--no-config", "--custom-extension", "some_extension"]
    # --no-config: avoid extra config from dev's machine interference

    cli.main(args)
    assert Path("pyscaffoldext-some_extension").exists()

    # Ensure an explanation on how to use
    # `--force` to avoid preffixing is given
    logs = caplog.text
    assert "--force" in logs
