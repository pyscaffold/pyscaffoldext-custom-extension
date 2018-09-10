from pyscaffold.cli import parse_args, run
from pyscaffoldext.custom_extension.custom_extension import set_pyscaffoldext_namespace
from pyscaffold.utils import prepare_namespace

def test_set_namespace():
    args = ["project",
            "-p", "package"]
    opts = parse_args(args)
    struct = {"project": {"src": {"package": {"file1": "Content"}}}}
    ns_struct, _ = set_pyscaffoldext_namespace(struct, opts)
    ns_pkg_struct = ns_struct["project"]["src"]
    assert ["project"] == list(ns_struct.keys())
    assert "package" not in list(ns_struct.keys())
    assert "package" in list(ns_pkg_struct["pyscaffoldext"].keys())
