"""Place for fixtures and configuration that will be used in most of the tests.
A nice option is to put your ``autouse`` fixtures here.
"""
from __future__ import absolute_import, division, print_function

import logging
import os
import shlex

import pytest
from pyscaffold.log import ReportFormatter

from .helpers import rmpath, uniqstr


@pytest.fixture
def tmpfolder(tmp_path):
    old_path = os.getcwd()
    new_path = tmp_path / uniqstr()
    new_path.mkdir(parents=True, exist_ok=True)
    os.chdir(str(new_path))
    try:
        yield new_path
    finally:
        os.chdir(old_path)
        rmpath(new_path)


@pytest.fixture
def venv(virtualenv):
    """Create a virtualenv for each test"""
    return virtualenv


@pytest.fixture
def venv_run(venv):
    """Run a command inside the venv"""

    def _run(*args, **kwargs):
        # pytest-virtualenv doesn't play nicely with external os.chdir
        # so let's be explicit about it...
        kwargs["cd"] = os.getcwd()
        kwargs["capture"] = True
        if len(args) == 1 and isinstance(args[0], str):
            args = shlex.split(args[0])
        return venv.run(args, **kwargs).strip()

    return _run


@pytest.fixture(autouse=True)
def isolated_logger(request, monkeypatch):
    """See isolated_logger in pyscaffold/tests/conftest.py to see why this fixture
    is important to guarantee tests checking logs work as expected.
    This just work for multiprocess environments, not multithread.
    """
    if "original_logger" in request.keywords:
        yield
        return

    # Get a fresh new logger, not used anywhere
    raw_logger = logging.getLogger(uniqstr())
    raw_logger.setLevel(logging.NOTSET)
    new_handler = logging.StreamHandler()

    patches = {
        "propagate": True,  # <- needed for caplog
        "nesting": 0,
        "wrapped": raw_logger,
        "handler": new_handler,
        "formatter": ReportFormatter(),
    }
    for key, value in patches.items():
        monkeypatch.setattr(f"pyscaffold.log.logger.{key}", value)

    try:
        yield
    finally:
        new_handler.close()
