from pathlib import Path

from pyscaffold import cli


def test_no_skeleton(tmpfolder):
    args = ["--no-config", "--custom-extension", "pyscaffoldext-some_extension"]
    # --no-config: avoid extra config from dev's machine interference
    cli.main(args)

    file = "pyscaffoldext-some_extension/src/pyscaffoldext/some_extension/skeleton.py"
    assert not Path(file).exists()


def test_tox(tmpfolder):
    args = ["--no-config", "--custom-extension", "pyscaffoldext-some_extension"]
    # --no-config: avoid extra config from dev's machine interference
    cli.main(args)
    assert Path("pyscaffoldext-some_extension/tox.ini").exists()


def test_pre_commit(tmpfolder):
    args = ["--no-config", "--custom-extension", "pyscaffoldext-some_extension"]
    # --no-config: avoid extra config from dev's machine interference
    cli.main(args)
    assert Path("pyscaffoldext-some_extension/.pre-commit-config.yaml").exists()
