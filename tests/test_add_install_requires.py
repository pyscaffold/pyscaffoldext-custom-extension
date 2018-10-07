from os.path import exists as path_exists

from pyscaffold.api import create_project
from pyscaffold.cli import parse_args
from pyscaffold.contrib.configupdater import ConfigUpdater


def test_add_install_requires(tmpfolder):
    args = ["--custom-extension", "pyscaffoldext-some_extension"]

    opts = parse_args(args)
    create_project(opts)
    assert path_exists("pyscaffoldext-some_extension/setup.cfg")

    config_updater = ConfigUpdater()

    with open("pyscaffoldext-some_extension/setup.cfg") as f:
        config_updater.read_file(f)

    install_requires = config_updater.get("options", "install_requires").value

    assert "pyscaffold" in install_requires
