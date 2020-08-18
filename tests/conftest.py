"""Place for fixtures and configuration that will be used in most of the tests.
A nice option is to put your ``autouse`` fixtures here.
Functions that can be imported and re-used are more suitable for the ``helpers`` file.
"""
import logging
import os

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
