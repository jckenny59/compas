from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_rhino import conversions

from compas.scene import GeometryObject
from .sceneobject import GHSceneObject


class BrepObject(GHSceneObject, GeometryObject):
    """A Scene object for drawing a brep in Grasshopper.

    Parameters
    ----------
    brep : :class:`compas_rhino.geometry.RhinoBrep`
        The brep to draw.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, brep, **kwargs):
        super(BrepObject, self).__init__(geometry=brep, **kwargs)

    def draw(self):
        """Draw the brep as a Grasshopper geometry.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Brep`]
            List of created Rhino breps.

        """
        brep = conversions.brep_to_rhino(self.geometry)

        if self.transformation:
            transformation = conversions.transformation_to_rhino(self.transformation)
            brep.Transform(transformation)

        self._guids = [brep]
        return self.guids
