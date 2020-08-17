# -*- coding: utf-8 -*-
"""
Main logic to create custom extensions
"""
from functools import reduce
from typing import List

from packaging.version import Version
from pyscaffold.actions import Action, ActionParams, ScaffoldOpts, Structure
from pyscaffold.extensions import Extension, include
from pyscaffold.extensions.namespace import Namespace
from pyscaffold.extensions.no_skeleton import NoSkeleton
from pyscaffold.extensions.pre_commit import PreCommit
from pyscaffold.extensions.travis import Travis
from pyscaffold.log import logger
from pyscaffold.operations import no_overwrite
from pyscaffold.structure import Leaf, ResolvedLeaf, merge, reify_content, resolve_leaf
from pyscaffold.update import ConfigUpdater, pyscaffold_version

from . import templates
from .templates import get_class_name_from_pkg_name, get_template

PYSCAFFOLDEXT_NS = "pyscaffoldext"
EXTENSION_FILE_NAME = "extension"
NO_OVERWRITE = no_overwrite()

INVALID_PROJECT_NAME = (
    "The prefix ``pyscaffoldext-`` will be added to the package name "
    "(as in PyPI/pip install). "
    "If that is not your intention, please use ``--force`` to overwrite."
)
"""Project name does not comply with convention of an extension"""


class NamespaceError(RuntimeError):
    """No additional namespace is allowed"""

    DEFAULT_MESSAGE = (
        "It's not possible to define a custom namespace "
        "when using ``--custom-extension``."
    )

    def __init__(self, message=DEFAULT_MESSAGE, *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class CustomExtension(Extension):
    """Configures a project to start creating extensions"""

    def augment_cli(self, parser):
        """Augments the command-line interface parser

        A command line argument ``--FLAG`` where FLAG=``self.name`` is added
        which appends ``self.activate`` to the list of extensions. As help
        text the docstring of the extension class is used.
        In most cases this method does not need to be overwritten.

        Args:
            parser: current parser object
        """

        parser.add_argument(
            self.flag,
            help=self.help_text,
            nargs=0,
            action=include(NoSkeleton(), Namespace(), PreCommit(), Travis(), self),
        )
        return self

    def activate(self, actions: List[Action]) -> List[Action]:
        """Activate extension, see :obj:`~pyscaffold.extension.Extension.activate`."""
        actions = self.register(actions, enforce_options, after="get_default_options")
        actions = self.register(actions, add_files)
        return actions


def enforce_options(struct: Structure, opts: ScaffoldOpts) -> ActionParams:
    """The following options should be enforced:

    - Fixed ``namespace`` value of pyscaffoldext (and no extra namespace)
    - The project name must start with ``pyscaffoldext-``.
    - The package name shouldn't contain the redundant ``pyscaffoldext_`` in the
      beginning of the name.

    See :obj:`pyscaffold.actions.Action`.
    """
    opts = opts.copy()
    namespace = opts.setdefault("namespace", PYSCAFFOLDEXT_NS)
    if namespace != PYSCAFFOLDEXT_NS:
        raise NamespaceError()

    if not opts["name"].startswith("pyscaffoldext-") and not opts["force"]:
        logger.warning(INVALID_PROJECT_NAME)
        opts["name"] = "pyscaffoldext-" + opts["name"]
        project = opts["project_path"]
        if not project.name.startswith("pyscaffoldext-"):
            opts["project_path"] = project.parent / ("pyscaffoldext-" + project.name)

    if opts["package"].startswith("pyscaffoldext_"):
        opts["package"] = opts["package"].replace("pyscaffoldext_", "")

    return struct, opts


def add_files(struct: Structure, opts: ScaffoldOpts) -> ActionParams:
    """Add custom extension files. See :obj:`pyscaffold.actions.Action`"""

    files: Structure = {
        "README.rst": (get_template("readme"), NO_OVERWRITE),
        "setup.cfg": modify_setupcfg(struct["setup.cfg"], opts),
        "src": {
            opts["package"]: {
                f"{EXTENSION_FILE_NAME}.py": (templates.extension, NO_OVERWRITE)
            }
        },
        "tests": {
            "conftest.py": (get_template("conftest"), NO_OVERWRITE),
            "test_custom_extension.py": (
                get_template("test_custom_extension"),
                NO_OVERWRITE,
            ),
        },
    }

    return merge(struct, files), opts


def modify_setupcfg(definition: Leaf, opts: ScaffoldOpts) -> ResolvedLeaf:
    """Modify setup.cfg to add install_requires and pytest settings before it is
    written.
    See :obj:`pyscaffold.operations`.
    """
    contents, original_op = resolve_leaf(definition)

    if contents is None:
        raise ValueError("File contents for setup.cfg should not be None")

    setupcfg = ConfigUpdater()
    setupcfg.read_string(reify_content(contents, opts))

    modifiers = (add_install_requires, add_pytest_requirements, add_entry_point)
    new_setupcfg = reduce(lambda acc, fn: fn(acc, opts), modifiers, setupcfg)

    return str(new_setupcfg), original_op


def add_entry_point(setupcfg: ConfigUpdater, opts: ScaffoldOpts) -> ConfigUpdater:
    """Adds the extension's entry_point to setup.cfg"""
    entry_points_key = "options.entry_points"

    if not setupcfg.has_section(entry_points_key):
        setupcfg["options"].add_after.section(entry_points_key)

    entry_points = setupcfg[entry_points_key]
    entry_points.insert_at(0).option("pyscaffold.cli")
    entry_points["pyscaffold.cli"].set_values(
        [
            "{} = {}.{}.{}:{}".format(
                opts["package"],
                opts["namespace"],
                opts["package"],
                EXTENSION_FILE_NAME,
                get_class_name_from_pkg_name(opts),
            )
        ]
    )

    return setupcfg


def add_install_requires(setupcfg: ConfigUpdater, _opts) -> ConfigUpdater:
    """Add PyScaffold dependency to install_requires """
    options = setupcfg["options"]
    version_str = get_install_requires_version()
    if "install_requires" in options:
        options["install_requires"].value = version_str
    else:
        options["package_dir"].add_after.option("install_requires", version_str)
    return setupcfg


def add_pytest_requirements(setupcfg: ConfigUpdater, _opts) -> ConfigUpdater:
    """Add [options.extras_require] testing requirements for py.test"""
    extras_require = setupcfg["options.extras_require"]
    extras_require["testing"].set_values(
        ["flake8", "pytest", "pytest-cov", "pytest-virtualenv", "pytest-xdist"]
    )
    return setupcfg


def get_install_requires_version():
    """Retrieves pyscaffold version for install_requires

    Returns:
        str: install_requires definition
    """
    current_version = Version(pyscaffold_version)
    major, minor, *_ = current_version.base_version.split(".")
    next_major = int(major) + 1

    min_version = Version(f"{major}.{minor}")
    if current_version.is_prerelease:
        min_version = current_version

    return f"pyscaffold>={min_version.public},<{next_major}"
