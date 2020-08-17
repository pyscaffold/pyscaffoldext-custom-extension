# -*- coding: utf-8 -*-
from functools import partial

from pyscaffold import templates

get_template = partial(templates.get_template, relative_to=__name__)


def get_class_name_from_pkg_name(opts):
    """Generate a class name from package name

    Args:
        opts (dict): given options, see :obj:`create_project` for
            an extensive list.

    Returns:
        str: class name of extension
    """
    pkg_name = opts["package"]
    return "".join(map(str.capitalize, pkg_name.split("_")))


def extension(opts):
    """Template of extension.py

    Args:
        opts: mapping parameters as dictionary

    Returns:
        str: file content as string
    """
    template = get_template("extension")
    opts["extension_class_name"] = get_class_name_from_pkg_name(opts)
    return template.safe_substitute(opts)
