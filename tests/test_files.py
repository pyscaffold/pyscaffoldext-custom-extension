from pathlib import Path

from pyscaffold import cli


def test_files(tmpfolder):
    args = ["--no-config", "--custom-extension", "pyscaffoldext-some_extension"]
    # --no-config: avoid extra config from dev's machine interference
    cli.main(args)
    files = (
        "README.rst",
        "CONTRIBUTING.rst",
        ".cirrus.yml",
        ".pre-commit-config.yaml",
        ".github/workflows/publish-package.yml",
    )
    for file in files:
        assert Path("pyscaffoldext-some_extension", file).exists()


def test_files_when_other_ci_is_used(tmpfolder):
    # CustomExtension should not produce files if other CI extension is used
    args = ["--no-config", "--gitlab", "--custom-extension", "pyscaffoldext-otherext"]
    # --no-config: avoid extra config from dev's machine interference
    cli.main(args)
    files = (
        ".cirrus.yml",
        ".github/workflows/publish-package.yml",
    )
    for file in files:
        assert not Path("pyscaffoldext-otherext", file).exists()
