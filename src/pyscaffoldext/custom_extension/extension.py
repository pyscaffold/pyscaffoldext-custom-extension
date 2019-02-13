# -*- coding: utf-8 -*-
"""
Main logic to create custom extensions
"""
from pyscaffold.api import Extension, helpers
from pyscaffold.extensions.namespace import (
    add_namespace,
    enforce_namespace_options
)
from pyscaffold.extensions.no_skeleton import NoSkeleton
from pyscaffold.extensions.pre_commit import PreCommit
from pyscaffold.extensions.tox import Tox
from pyscaffold.extensions.travis import Travis
from pyscaffold.extensions.namespace import Namespace
from pyscaffold.update import ConfigUpdater, parse_version, pyscaffold_version

from . import templates
from .templates import get_class_name_from_pkg_name

PYSCAFFOLDEXT_NS = "pyscaffoldext"
EXTENSION_FILE_NAME = "extension"


class InvalidProjectNameException(RuntimeError):
    """Project name does not comply with convention of an extension"""

    DEFAULT_MESSAGE = (
        "An extension project name should start with "
        "``pyscaffoldext-`` or use ``--force`` to overwrite.")

    def __init__(self, message=DEFAULT_MESSAGE, *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class CustomExtension(Extension):
    """Configures a project to start creating extensions"""

    def activate(self, actions):
        """Activate extension

        Args:
            actions (list): list of actions to perform

        Returns:
            list: updated list of actions
        """
        default_commands = [NoSkeleton, Tox, PreCommit, Travis]
        for command in default_commands:
            actions = command(command.__name__).activate(actions)
        # set the namesapce accordingly
        namespace = Namespace(Namespace.__name__)
        namespace.args = [PYSCAFFOLDEXT_NS]
        actions = namespace.activate(actions)

        actions = self.register(
                actions,
                check_project_name,
                before='define_structure'
        )

        actions = self.register(
                actions,
                add_custom_extension_structure,
                after='remove_files'
        )

        actions = self.register(
                actions,
                add_readme,
                after="add_custom_extension_structure"
        )

        actions = self.register(
                actions,
                add_conftest,
                after="add_readme"
        )

        actions = self.register(
                actions,
                add_test_custom_extension,
                after="add_conftest"
        )

        actions = self.register(
                actions,
                modify_setupcfg,
                after="add_test_custom_extension"
        )

        return actions


def modify_setupcfg(struct, opts):
    """Modify setup.cfg to add install_requires and pytest settings

    Args:
        struct (dict): project representation as (possibly) nested
            :obj:`dict`.
        opts (dict): given options, see :obj:`create_project` for
            an extensive list.

    Returns:
        struct, opts: updated project representation and options
    """
    setupcfg_path = [opts["project"], "setup.cfg"]
    # add important namespace settings
    opts["namespace"] = [PYSCAFFOLDEXT_NS]
    struct = helpers.modify(struct, setupcfg_path, add_install_requires)
    struct = helpers.modify(struct, setupcfg_path, add_pytest_requirements)
    struct = helpers.modify(struct, setupcfg_path,
                            lambda x: add_entry_point(x, opts))
    return struct, opts


def add_entry_point(setupcfg_str, opts):
    """Adds the extension's entry_point to setup.cfg

    Args:
        setupcfg_str (str): content of setup.cfg as string
        opts (dict): given options, see :obj:`create_project` for
            an extensive list.

    Returns:
       str: setup.cfg with install_requires
    """
    entry_points_key = "options.entry_points"

    setupcfg = ConfigUpdater()
    setupcfg.read_string(setupcfg_str)

    if not setupcfg.has_section(entry_points_key):
        setupcfg["options"].add_after.section(entry_points_key)

    entry_points = setupcfg[entry_points_key]
    entry_points.insert_at(0).option("pyscaffold.cli")
    entry_points["pyscaffold.cli"].set_values(
        ["{} = {}.{}.{}:{}".format(
            opts["package"],
            opts["namespace"][-1],
            opts["package"],
            EXTENSION_FILE_NAME,
            get_class_name_from_pkg_name(opts))]
    )

    return str(setupcfg)


def add_install_requires(setupcfg_str):
    """Add PyScaffold dependency to install_requires

    Args:
        setupcfg_str (str): content of setup.cfg as string

    Returns:
       str: setup.cfg with install_requires
    """
    setupcfg = ConfigUpdater()
    setupcfg.read_string(setupcfg_str)
    options = setupcfg['options']
    version_str = get_install_requires_version()
    if 'install_requires' in options:
        options['install_requires'].value = version_str
    else:
        options['package_dir'].add_after.option('install_requires',
                                                version_str)
    return str(setupcfg)


def add_pytest_requirements(setupcfg_str):
    """Add [options.extras_require] testing requirements for py.test

    Args:
        setupcfg_str (str): content of setup.cfg as string

    Returns:
       str: setup.cfg with install_requires
    """
    setupcfg = ConfigUpdater()
    setupcfg.read_string(setupcfg_str)
    extras_require = setupcfg['options.extras_require']
    extras_require['testing'].set_values(['flake8',
                                          'pytest',
                                          'pytest-cov',
                                          'pytest-virtualenv',
                                          'pytest-xdist'])
    return str(setupcfg)


def get_install_requires_version():
    """Retrieves pyscaffold version for install_requires

    Returns:
        str: install_requires definition
    """
    require_str = "pyscaffold>={major}.{minor}a0,<{next_major}.0a0"
    major, minor, *rest = (parse_version(pyscaffold_version)
                           .base_version.split('.'))
    next_major = int(major) + 1
    return require_str.format(major=major, minor=minor, next_major=next_major)


def add_custom_extension_structure(struct, opts):
    """Adds basic module for custom extension

    Args:
        struct (dict): project representation as (possibly) nested
            :obj:`dict`.
        opts (dict): given options, see :obj:`create_project` for
            an extensive list.

    Returns:
        struct, opts: updated project representation and options
    """
    custom_extension_file_content = templates.extension(opts)
    filename = "{}.py".format(EXTENSION_FILE_NAME)
    path = [opts["project"], "src", opts["package"], filename]
    struct = helpers.ensure(struct, path,
                            custom_extension_file_content,
                            helpers.NO_OVERWRITE)

    return struct, opts


def add_readme(struct, opts):
    """Adds README template

    Args:
        struct (dict): project representation as (possibly) nested
            :obj:`dict`.
        opts (dict): given options, see :obj:`create_project` for
            an extensive list.

    Returns:
        struct, opts: updated project representation and options
    """
    file_content = templates.readme(opts)
    path = [opts["project"], "README.rst"]
    struct = helpers.ensure(struct, path,
                            file_content,
                            helpers.NO_OVERWRITE)

    return struct, opts


def add_conftest(struct, opts):
    """Adds improved tests/conftest.py

    Args:
        struct (dict): project representation as (possibly) nested
            :obj:`dict`.
        opts (dict): given options, see :obj:`create_project` for
            an extensive list.

    Returns:
        struct, opts: updated project representation and options
    """
    file_content = templates.conftest(opts)
    path = [opts["project"], "tests", "conftest.py"]
    struct = helpers.ensure(struct, path,
                            file_content,
                            helpers.NO_OVERWRITE)

    return struct, opts


def add_test_custom_extension(struct, opts):
    """Adds tests/test_custom_extension.py

    Args:
        struct (dict): project representation as (possibly) nested
            :obj:`dict`.
        opts (dict): given options, see :obj:`create_project` for
            an extensive list.

    Returns:
        struct, opts: updated project representation and options
    """
    file_content = templates.test_custom_extension(opts)
    path = [opts["project"], "tests", "test_custom_extension.py"]
    struct = helpers.ensure(struct, path,
                            file_content,
                            helpers.NO_OVERWRITE)

    return struct, opts


def check_project_name(struct, opts):
    """Enforce the naming convention of PyScaffold extensions

    The project name must start with 'pyscaffoldext-' and
    the package name shouldn't contain the redundant
    'pyscaffoldext_' in the beginning of the name.

    Args:
        struct (dict): project representation as (possibly) nested
            :obj:`dict`.
        opts (dict): given options, see :obj:`create_project` for
            an extensive list.

    Returns:
        struct, opts: updated project representation and options
    """
    if not opts['project'].startswith('pyscaffoldext-') and not opts['force']:
        raise InvalidProjectNameException

    if opts["package"].startswith('pyscaffoldext_'):
        opts["package"] = opts["package"].replace("pyscaffoldext_", "")

    return struct, opts
