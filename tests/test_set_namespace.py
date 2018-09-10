from pyscaffold.cli import parse_args

from pyscaffoldext.custom_extension.custom_extension import (
    set_pyscaffoldext_namespace
)


def test_set_namespace():
    args = ["project",
            "-p", "some_package"]
    opts = parse_args(args)
    struct = {"project": {"src": {"some_package": {"file1": "Content"}}}}
    ns_struct, _ = set_pyscaffoldext_namespace(struct, opts)
    ns_pkg_struct = ns_struct["project"]["src"]
    assert ["project"] == list(ns_struct.keys())
    assert "some_package" not in list(ns_struct.keys())
    assert "some_package" in list(ns_pkg_struct["pyscaffoldext"].keys())


def test_set_namespace_with_existing_namespace_option():
    args = ["project",
            "-p", "some_package", "--namespace", "some_namespace"]
    opts = parse_args(args)
    struct = {"project": {"src": {"some_package": {"file1": "Content"}}}}
    ns_struct, _ = set_pyscaffoldext_namespace(struct, opts)
    ns_pkg_struct = ns_struct["project"]["src"]
    assert ["project"] == list(ns_struct.keys())
    assert "some_package" not in list(ns_struct.keys())
    assert "some_package" in list(ns_pkg_struct["pyscaffoldext"]["some_namespace"].keys())
