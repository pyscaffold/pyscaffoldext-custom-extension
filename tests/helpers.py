import os
import stat
import traceback
from pathlib import Path
from shutil import rmtree
from time import sleep
from uuid import uuid4
from warnings import warn


def uniqstr():
    """Generates a unique random long string every time it is called"""
    return str(uuid4())


def rmpath(path):
    """Carelessly/recursively remove path.
    If an error occurs it will just be ignored, so not suitable for every usage.
    The best is to use this function for paths inside pytest tmp directories, and with
    some hope pytest will also do some cleanup itself.
    """
    try:
        rmtree(str(path), onerror=set_writable)
    except FileNotFoundError:
        return
    except Exception:
        msg = f"rmpath: Impossible to remove {path}, probably an OS issue...\n\n"
        warn(msg + traceback.format_exc())


def set_writable(func, path, _exc_info):
    sleep(1)  # Sometimes just giving time to the SO, works

    if not Path(path).exists():
        return  # we just want to remove files anyway

    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)

    # now it either works or re-raise the exception
    func(path)
