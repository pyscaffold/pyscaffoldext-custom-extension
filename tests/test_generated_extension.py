import logging
import os
from pathlib import Path
from subprocess import CalledProcessError

import pytest
from pyscaffold import cli, shell
from pyscaffold.file_system import chdir

from .helpers import run, run_common_tasks


@pytest.mark.slow
@pytest.mark.system
def test_generated_extension(tmpfolder):
    args = [
        "--no-config",  # <- avoid extra config from dev's machine interference
        "--venv",  # <- generate a venv that we will use to install the project
        "--custom-extension",
        "pyscaffoldext-some_extension",
    ]

    cli.main(args)
    with chdir("pyscaffoldext-some_extension"):
        try:
            run_common_tasks()
        except CalledProcessError as ex:
            if os.name == "nt" and "too long" in ex.output:
                pytest.skip("Windows really have a problem with long paths....")
            else:
                raise
        putup = shell.get_executable("putup", prefix=".venv", include_path=False)
        assert putup

    run(putup, "--some-extension", "the_actual_project")
    assert Path("the_actual_project/setup.cfg").exists()


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
