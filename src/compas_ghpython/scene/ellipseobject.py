from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino import conversions

from compas.scene import GeometryObject
from .sceneobject import GHSceneObject


class EllipseObject(GHSceneObject, GeometryObject):
    """Scene object for drawing ellipses.

    Parameters
    ----------
    ellipse : :class:`compas.geometry.Ellipse`
        A COMPAS ellipse.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, ellipse, **kwargs):
        super(EllipseObject, self).__init__(geometry=ellipse, **kwargs)

    def draw(self):
        """Draw the ellipse.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Ellipse`]
            List of created Rhino ellipse.

        """
        ellipse = conversions.ellipse_to_rhino(self.geometry)
        ellipse = ellipse.ToNurbsCurve()

        if self.transformation:
            ellipse.Transform(conversions.transformation_to_rhino(self.transformation))

        self._guids = [ellipse]
        return self.guids
