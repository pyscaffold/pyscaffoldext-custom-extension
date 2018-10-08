from pyscaffold.api import Extension, helpers
from pyscaffold.extensions.namespace import (
    add_namespace,
    enforce_namespace_options
)
from pyscaffold.extensions.no_skeleton import NoSkeleton
from pyscaffold.extensions.pre_commit import PreCommit
from pyscaffold.extensions.tox import Tox
from pyscaffold.update import ConfigUpdater, parse_version, pyscaffold_version

from .templates import extension, readme

PYSCAFFOLDEXT_NS = "pyscaffoldext"
EXTENSION_FILE_NAME = "extension"


class InvalidProjectNameException(BaseException):
    """Project name does not comply with convention of an extension"""

    DEFAULT_MESSAGE = (
        "An extension project name should start with "
        "``pyscaffoldext-`` or use ``--force`` to overwrite.")

    def __init__(self, message=DEFAULT_MESSAGE, *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class CustomExtension(Extension):
    """
    Configures a project to start creating extensions
    without further changes
    """

    def activate(self, actions):
        default_commands = [NoSkeleton, Tox, PreCommit]
        for command in default_commands:
            actions = command(command.__name__).activate(actions)

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
                set_pyscaffoldext_namespace,
                after="add_readme"
        )

        actions = self.register(
                actions,
                add_install_requires,
                after="set_pyscaffoldext_namespace"
        )
        return self.register(
                actions,
                self.add_entry_point,
                after='set_pyscaffoldext_namespace'
        )

    def add_entry_point(self, struct, opts):
        entry_points_key = "options.entry_points"

        setup_cfg_content = struct[opts["project"]]["setup.cfg"][0]

        config = ConfigUpdater()
        config.read_string(setup_cfg_content)

        config.remove_section(entry_points_key)
        config.add_section(entry_points_key)

        config.set(entry_points_key, "pyscaffold.cli",
                   "{}={}.{}.{}:{}".format(opts["package"],
                                           opts["namespace"][-1],
                                           opts["package"],
                                           EXTENSION_FILE_NAME,
                                           get_class_name_from_opts(opts))
                   )

        struct[opts["project"]]["setup.cfg"] = str(config)

        return struct, opts


def add_install_requires(struct, opts):
    """
    Add PyScaffold dependency to install_requires
    :param struct:
    :param opts:
    :return:
    """
    setupcfg = ConfigUpdater()
    setupcfg.read_string(struct[opts["project"]]["setup.cfg"])
    options = setupcfg['options']

    version_str = get_install_requires_version()

    options['package_dir'].add_after.option('install_requires', version_str)
    struct[opts["project"]]["setup.cfg"] = str(setupcfg)

    return struct, opts


def set_pyscaffoldext_namespace(struct, opts):
    """
    Add the pyscaffoldext namespace as the outermost namespace of
    the project to create. If the namespace parameter is
    already specified, pyscaffoldext is prepended to the specified
    namespace.
    :param struct:
    :param opts:
    :return:
    """
    namespace_parameter = opts.get("namespace", None)
    namespace_list = [PYSCAFFOLDEXT_NS]

    if isinstance(namespace_parameter, list):
        namespace_list.append(namespace_parameter[-1])
    elif isinstance(namespace_parameter, str):
        namespace_list.append(namespace_parameter)

    opts["namespace"] = ".".join(namespace_list)
    struct, opts = enforce_namespace_options(struct, opts)

    if not namespace_parameter:
        struct, opts = add_namespace(struct, opts)

    return struct, opts


def get_install_requires_version():
    require_str = "pyscaffold>={major}.{minor}a0,<{next_major}.0a0"
    major, minor, *rest = (parse_version(pyscaffold_version)
                           .base_version.split('.'))
    next_major = int(major) + 1
    return require_str.format(major=major, minor=minor, next_major=next_major)


def get_class_name_from_opts(opts):
    pkg_name = opts["package"]
    return "".join(map(str.capitalize, pkg_name.split("_")))


def add_custom_extension_structure(struct, opts):
    """
    Adds an empty class that will serve as the skeleton
    for the logic of the extension to create
    :param struct:
    :param opts:
    :return:
    """
    custom_extension_file_content = extension(
            get_class_name_from_opts(opts))
    filename = "{}.py".format(EXTENSION_FILE_NAME)

    path = [opts["project"], "src", opts["package"], filename]
    struct = helpers.ensure(struct, path,
                            custom_extension_file_content,
                            helpers.NO_OVERWRITE)

    return struct, opts


def add_readme(struct, opts):
    """
    Add README template
    :param struct:
    :param opts:
    :return:
    """
    file_content = readme(
            get_class_name_from_opts(opts))
    filename = "README.rst"

    path = [opts["project"], filename]
    struct = helpers.ensure(struct, path,
                            file_content,
                            helpers.NO_OVERWRITE)

    return struct, opts


def check_project_name(struct, opts):
    """
    Enforce the naming convention of PyScaffold extensions.
    The project name must start with 'pyscaffoldext-' and
    the package name shouldn't contain the redundant
    'pyscaffoldext_' in the beginning of the name.
    :param struct:
    :param opts:
    :return:
    """
    if not opts['project'].startswith('pyscaffoldext-') and not opts['force']:
        raise InvalidProjectNameException("An extension project name"
                                          "should start with "
                                          "'pyscaffoldext-")

    if opts["package"].startswith('pyscaffoldext_'):
        opts["package"] = opts["package"].replace("pyscaffoldext_", "")

    return struct, opts
