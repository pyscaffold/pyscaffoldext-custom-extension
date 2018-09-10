import configparser
import io

from pyscaffold.api import helpers
from pyscaffold.extensions.no_skeleton import NoSkeleton

from .templates import extension


class CustomExtension(NoSkeleton):
    """
    Test
    """

    def activate(self, actions):
        actions = self.register(
                actions,
                self.add_custom_extension_structure,
                after='define_structure')
        return self.register(
                actions,
                self.add_entry_point,
                after='add_custom_extension_structure')

    def add_custom_extension_structure(self, struct, opts):
        custom_extension_file_content = extension(
                self.get_class_name_from_opts(opts))
        filename = "{}.py".format(opts["package"])
        struct = helpers.ensure(struct, [opts["project"],
                                         "src",
                                         opts["package"],
                                         filename],
                                custom_extension_file_content,
                                helpers.NO_OVERWRITE)

        return struct, opts

    def add_entry_point(self, struct, opts):
        setup_cfg_content = struct[opts["project"]]["setup.cfg"][0]
        config = configparser.ConfigParser()
        config.read_string(setup_cfg_content)
        config.remove_section("options.entry_points")
        config.add_section("options.entry_points")
        config.set("options.entry_points", "pyscaffold.cli",
                   "{}={}.{}:{}".format(opts["package"],
                                        opts["package"],
                                        opts["package"],
                                        self.get_class_name_from_opts(opts)))
        buffer = io.StringIO()
        config.write(buffer)

        struct[opts["project"]]["setup.cfg"] = buffer.getvalue()

        return struct, opts

    @staticmethod
    def get_class_name_from_opts(opts):
        pkg_name = opts["package"]
        return "".join(map(str.capitalize, pkg_name.split("_")))
