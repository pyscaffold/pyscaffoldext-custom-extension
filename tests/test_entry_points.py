from pathlib import Path

from configupdater import ConfigUpdater
from pyscaffold import cli


def test_entry_point(tmpfolder):
    args = ["--no-config", "--custom-extension", "pyscaffoldext-some_extension"]
    # --no-config: avoid extra config from dev's machine interference
    cli.main(args)
    assert Path("pyscaffoldext-some_extension/setup.cfg").exists()

    setup_cfg = ConfigUpdater()
    setup_cfg.read_string(Path("pyscaffoldext-some_extension/setup.cfg").read_text())
    entry_point = setup_cfg.get("options.entry_points", "pyscaffold.cli").value
    expected = "\nsome_extension = pyscaffoldext.some_extension.extension:SomeExtension"
    assert entry_point == expected
