"""Place for fixtures and configuration that will be used in most of the tests.
A nice option is to put your ``autouse`` fixtures here.
"""
from __future__ import absolute_import, division, print_function

import logging
import os
import shlex
import stat
from shutil import rmtree
from uuid import uuid4

import pytest


def set_writable(func, path, exc_info):
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise RuntimeError


@pytest.fixture
def tmpfolder(tmpdir):
    old_path = os.getcwd()
    newpath = str(tmpdir)
    os.chdir(newpath)
    try:
        yield tmpdir
    finally:
        os.chdir(old_path)
        rmtree(newpath, onerror=set_writable)


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


@pytest.fixture
def logger(monkeypatch):
    pyscaffold = __import__("pyscaffold", globals(), locals(), ["log"])
    logger_obj = pyscaffold.log.logger
    monkeypatch.setattr(logger_obj, "propagate", True)  # <- needed for caplog
    yield logger_obj


def uniqstr():
    """Generates a unique random long string every time it is called"""
    return str(uuid4())


@pytest.fixture(autouse=True)
def isolated_logger(request, logger, monkeypatch):
    # In Python the common idiom of using logging is to share the same log
    # globally, even between threads. While this is usually OK because
    # internally Python takes care of locking the shared resources, it also
    # makes very difficult to build things on top of the logging system without
    # using the same global approach.
    # For simplicity, to make things easier for extension developers and because
    # PyScaffold not really uses multiple threads, this is the case in
    # `pyscaffold.log`.
    # On the other hand, shared state and streams can make the testing
    # environment a real pain, since we are messing with everything all the
    # time, specially when running tests in parallel (so we not guarantee the
    # execution order).
    # This fixture do a huge effort in trying to isolate as much as possible
    # each test function regarding logging. We keep the global object, so the
    # tests can be seamless, but internally replace the underlying native
    # loggers and handlers for "one-shot" ones.
    # (Of course, we can keep the same global object just because the plugins
    # for running tests in parallel are based in multiple processes instead of
    # threads, otherwise we would need another strategy)

    if "original_logger" in request.keywords:
        # Some tests need to check the original implementation to make sure
        # side effects of the shared object are consistent. We have to try to
        # make them as few as possible.
        yield logger
        return

    # Get a fresh new logger, not used anywhere
    raw_logger = logging.getLogger(uniqstr())
    # ^  Python docs advert against instantiating Loggers directly and instruct
    #    devs to use `getLogger`. So we use a unique name to guarantee we get a
    #    new logger each time.
    raw_logger.setLevel(logging.NOTSET)
    new_handler = logging.StreamHandler()

    # Replace the internals of the LogAdapter
    # --> Messing with global state: don't try this at home ...
    #     (if we start to use threads, we cannot do this)

    # Be lazy to import modules due to coverage warnings
    # (see @FlorianWilhelm comments on #174)
    from pyscaffold.log import ReportFormatter

    monkeypatch.setattr(logger, "propagate", True)
    monkeypatch.setattr(logger, "nesting", 0)
    monkeypatch.setattr(logger, "wrapped", raw_logger)
    monkeypatch.setattr(logger, "handler", new_handler)
    monkeypatch.setattr(logger, "formatter", ReportFormatter())
    # <--

    try:
        yield logger
    finally:
        new_handler.close()
        # ^  Force the handler to not be re-used
