# -*- coding: utf-8 -*-
import os
import string
from pkg_resources import resource_string


def get_template(name):
    """Retrieve the template by name

    Args:
        name: name of template

    Returns:
        :obj:`string.Template`: template
    """
    file_name = "{name}.template".format(name=name)
    data = resource_string(__name__, file_name)
    # we assure that line endings are converted to '\n' for all OS
    data = data.decode(encoding="utf-8").replace(os.linesep, "\n")
    return string.Template(data)


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


def readme(opts):
    """Template of README.rst

    Args:
        opts: mapping parameters as dictionary

    Returns:
        str: file content as string
    """
    template = get_template("readme")
    return template.safe_substitute(opts)


def test_custom_extension(opts):
    """Template of test_custom_extension.py

    Args:
        opts: mapping parameters as dictionary

    Returns:
        str: file content as string
    """
    template = get_template("test_custom_extension")
    return template.safe_substitute(opts)


def conftest(opts):
    """Template of improved conftest.py

    Args:
        opts: mapping parameters as dictionary

    Returns:
        str: file content as string
    """
    template = get_template("conftest")
    return template.safe_substitute(opts)
