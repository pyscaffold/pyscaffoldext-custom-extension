from os.path import exists as path_exists

from pyscaffold import cli


def test_readme(tmpfolder):
    args = ["--no-config", "--custom-extension", "pyscaffoldext-some_extension"]
    # --no-config: avoid extra config from dev's machine interference
    cli.main(args)
    assert path_exists("pyscaffoldext-some_extension/README.rst")
