from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino import conversions

from compas.scene import GeometryObject
from .sceneobject import GHSceneObject
from compas.geometry import Frame


class PlaneObject(GHSceneObject, GeometryObject):
    """Scene object for drawing planes.

    Parameters
    ----------
    plane : :class:`compas.geometry.Plane`
        A COMPAS plane.
    scale : float, optional
        Scale factor that controls the visualisation size of the plane.
        Default is ``1.0``.
    **kwargs : dict, optional
        Additional keyword arguments.

    Attributes
    ----------
    scale : float
        Scale factor that controls the visualisation size of the plane.

    """

    def __init__(self, plane, scale=1.0, **kwargs):
        super(PlaneObject, self).__init__(geometry=plane, **kwargs)
        self.scale = scale

    def draw(self):
        """Draw the frame.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Line`, :rhino:`Rhino.Geometry.Mesh`]
            List of created Rhino geometries.
        """
        frame = Frame.from_plane(self._item)
        normal = conversions.line_to_rhino(
            [frame.to_world_coordinates([0, 0, 0]), frame.to_world_coordinates([0, 0, self.scale])]
        )

        vertices = [
            frame.to_world_coordinates([-self.scale, -self.scale, 0]),
            frame.to_world_coordinates([self.scale, -self.scale, 0]),
            frame.to_world_coordinates([self.scale, self.scale, 0]),
            frame.to_world_coordinates([-self.scale, self.scale, 0]),
        ]
        faces = [[0, 1, 2, 3]]
        mesh = conversions.vertices_and_faces_to_rhino(vertices, faces)

        geometries = [normal, mesh]

        if self.transformation:
            for geometry in geometries:
                geometry.Transform(conversions.transformation_to_rhino(self.transformation))

        self._guids = geometries
        return self.guids
