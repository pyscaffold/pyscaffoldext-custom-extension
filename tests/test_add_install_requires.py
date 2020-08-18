from pathlib import Path

from configupdater import ConfigUpdater
from pyscaffold import cli


def test_add_install_requires(tmpfolder):
    args = ["--no-config", "--custom-extension", "pyscaffoldext-some_extension"]
    # --no-config: avoid extra config from dev's machine interference
    cli.main(args)
    assert Path("pyscaffoldext-some_extension/setup.cfg").exists()

    setup_cfg = ConfigUpdater()
    setup_cfg.read_string(Path("pyscaffoldext-some_extension/setup.cfg").read_text())

    install_requires = setup_cfg.get("options", "install_requires").value
    assert "pyscaffold" in install_requires
