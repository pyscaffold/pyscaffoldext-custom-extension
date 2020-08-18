import logging
from pathlib import Path

import pytest
from pyscaffold import cli
from pyscaffold.file_system import chdir
from pyscaffold.shell import get_executable

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
        run_common_tasks()
        putup = get_executable("putup", prefix=".venv", include_path=False)
        assert putup

    run(putup, "--venv", "--some-extension", "the_actual_project")
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
