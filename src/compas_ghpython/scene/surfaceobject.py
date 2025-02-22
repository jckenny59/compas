from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino import conversions

from compas.scene import GeometryObject
from .sceneobject import GHSceneObject


class SurfaceObject(GHSceneObject, GeometryObject):
    """Scene object for drawing surfaces.

    Parameters
    ----------
    surface : :class:`compas.geometry.Surface`
        A COMPAS surface.

    Other Parameters
    ----------------
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, surface, **kwargs):
        super(SurfaceObject, self).__init__(geometry=surface, **kwargs)

    def draw(self):
        """Draw the surface.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Surface`]
            The created Rhino surfaces.

        """
        geometry = conversions.surface_to_rhino(self.geometry)

        if self.transformation:
            geometry.Transform(conversions.transformation_to_rhino(self.transformation))

        self._guids = [geometry]
        return self.guids
