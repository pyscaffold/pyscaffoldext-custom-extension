from pathlib import Path

from pyscaffold import cli


def test_files(tmpfolder):
    args = ["--no-config", "--custom-extension", "pyscaffoldext-some_extension"]
    # --no-config: avoid extra config from dev's machine interference
    cli.main(args)
    files = (
        "README.rst",
        "CONTRIBUTING.rst",
        ".pre-commit-config.yaml",
        ".github/workflows/publish-package.yml",
    )
    for file in files:
        assert Path("pyscaffoldext-some_extension", file).exists()
