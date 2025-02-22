"""
This package provides scene object plugins for visualising COMPAS objects in Blender.
When working in Blender, :class:`compas.scene.SceneObject` will automatically use the corresponding Blender object for each COMPAS object type.
"""

import compas_blender

from compas.plugins import plugin
from compas.scene import register

from compas.geometry import Box
from compas.geometry import Capsule
from compas.geometry import Circle
from compas.geometry import Cone
from compas.geometry import Curve
from compas.geometry import Cylinder
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Pointcloud
from compas.geometry import Polygon
from compas.geometry import Polyhedron
from compas.geometry import Polyline
from compas.geometry import Sphere
from compas.geometry import Surface
from compas.geometry import Torus
from compas.geometry import Vector
from compas.datastructures import Mesh
from compas.datastructures import Network
from compas.datastructures import VolMesh

from .sceneobject import BlenderSceneObject
from .boxobject import BoxObject
from .capsuleobject import CapsuleObject
from .circleobject import CircleObject
from .coneobject import ConeObject
from .curveobject import CurveObject
from .cylinderobject import CylinderObject
from .frameobject import FrameObject
from .lineobject import LineObject
from .meshobject import MeshObject
from .networkobject import NetworkObject
from .planeobject import PlaneObject
from .pointobject import PointObject
from .pointcloudobject import PointcloudObject
from .polygonobject import PolygonObject
from .polyhedronobject import PolyhedronObject
from .polylineobject import PolylineObject
from .sphereobject import SphereObject
from .surfaceobject import SurfaceObject
from .torusobject import TorusObject
from .vectorobject import VectorObject
from .volmeshobject import VolMeshObject


@plugin(category="drawing-utils", pluggable_name="clear", requires=["bpy"])
def clear_blender(guids=None):
    compas_blender.clear(guids=guids)


@plugin(category="drawing-utils", pluggable_name="redraw", requires=["bpy"])
def redraw_blender():
    compas_blender.redraw()


@plugin(category="factories", requires=["bpy"])
def register_scene_objects():
    register(Box, BoxObject, context="Blender")
    register(Capsule, CapsuleObject, context="Blender")
    register(Circle, CircleObject, context="Blender")
    register(Cone, ConeObject, context="Blender")
    register(Curve, CurveObject, context="Blender")
    register(Cylinder, CylinderObject, context="Blender")
    register(Frame, FrameObject, context="Blender")
    register(Line, LineObject, context="Blender")
    register(Mesh, MeshObject, context="Blender")
    register(Network, NetworkObject, context="Blender")
    register(Plane, PlaneObject, context="Blender")
    register(Point, PointObject, context="Blender")
    register(Pointcloud, PointcloudObject, context="Blender")
    register(Polygon, PolygonObject, context="Blender")
    register(Polyhedron, PolyhedronObject, context="Blender")
    register(Polyline, PolylineObject, context="Blender")
    register(Sphere, SphereObject, context="Blender")
    register(Surface, SurfaceObject, context="Blender")
    register(Torus, TorusObject, context="Blender")
    register(Vector, VectorObject, context="Blender")
    register(VolMesh, VolMeshObject, context="Blender")
    print("Blender Objects registered.")


__all__ = [
    "BlenderSceneObject",
    "BoxObject",
    "CapsuleObject",
    "CircleObject",
    "ConeObject",
    "CurveObject",
    "CylinderObject",
    "FrameObject",
    "LineObject",
    "MeshObject",
    "NetworkObject",
    "PlaneObject",
    "PointObject",
    "PointcloudObject",
    "PolygonObject",
    "PolyhedronObject",
    "PolylineObject",
    "SphereObject",
    "SurfaceObject",
    "TorusObject",
    "VectorObject",
    "VolMeshObject",
]
