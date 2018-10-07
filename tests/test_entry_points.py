from os.path import exists as path_exists

from pyscaffold.api import create_project
from pyscaffold.cli import parse_args
from pyscaffold.contrib.configupdater import ConfigUpdater


def test_entry_point_with_namespace(tmpfolder):
    args = ["--namespace", "test", "--custom-extension",
            "pyscaffoldext-some_extension"]

    opts = parse_args(args)
    create_project(opts)
    assert path_exists("pyscaffoldext-some_extension/setup.cfg")

    config_updater = ConfigUpdater()

    with open("pyscaffoldext-some_extension/setup.cfg") as f:
        config_updater.read_file(f)

    entry_point = config_updater.get("options.entry_points",
                                     "pyscaffold.cli").value
    assert entry_point == "some_extension=pyscaffoldext." \
                          "test.some_extension.extension:SomeExtension"


def test_entry_point(tmpfolder):
    args = ["--custom-extension", "pyscaffoldext-some_extension"]

    opts = parse_args(args)
    create_project(opts)
    assert path_exists("pyscaffoldext-some_extension/setup.cfg")

    config_updater = ConfigUpdater()
    with open("pyscaffoldext-some_extension/setup.cfg") as f:
        config_updater.read_file(f)
    entry_point = config_updater.get("options.entry_points",
                                     "pyscaffold.cli").value
    assert entry_point == "some_extension=pyscaffoldext." \
                          "some_extension.extension:SomeExtension"
