import Rhino  # noqa: F401

from compas.plugins import plugin

from .brep import RhinoBrep


@plugin(category="factories", requires=["Rhino"])
def new_brep(*args, **kwargs):
    return object.__new__(RhinoBrep)


@plugin(category="factories", requires=["Rhino"])
def from_native(*args, **kwargs):
    return RhinoBrep.from_native(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def from_box(*args, **kwargs):
    return RhinoBrep.from_box(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def from_cylinder(*args, **kwargs):
    return RhinoBrep.from_cylinder(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def from_sphere(*args, **kwargs):
    return RhinoBrep.from_sphere(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def from_mesh(*args, **kwargs):
    return RhinoBrep.from_mesh(*args, **kwargs)
