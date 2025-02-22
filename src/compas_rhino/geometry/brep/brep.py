from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino  # type: ignore

from compas.geometry import Frame
from compas.geometry import Brep
from compas.geometry import BrepTrimmingError
from compas.geometry import BrepError
from compas.geometry import Plane
from compas.geometry import Point

from compas_rhino.conversions import box_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from compas_rhino.conversions import frame_to_rhino
from compas_rhino.conversions import cylinder_to_rhino
from compas_rhino.conversions import sphere_to_rhino
from compas_rhino.conversions import mesh_to_compas
from compas_rhino.conversions import mesh_to_rhino
from compas_rhino.conversions import point_to_rhino

from .builder import _RhinoBrepBuilder
from .face import RhinoBrepFace
from .edge import RhinoBrepEdge
from .vertex import RhinoBrepVertex
from .loop import RhinoBrepLoop

TOLERANCE = 1e-6


class RhinoBrep(Brep):
    """Rhino Brep backend class.

    Wraps around and allows serialization and de-serialization of a :class:`Rhino.Geometry.Brep`.

    Attributes
    ----------
    native_brep : :class:`Rhino.Geometry.Brep`
        The underlying Rhino Brep instance.
    vertices : list[:class:`compas_rhino.geometry.RhinoBrepVertex`], read-only
        The list of vertices which comprise this Brep.
    points : list[:class:`compas.geometry.Point`], read-only
        The list of vertex geometries as points in 3D space.
    edges : list[:class:`compas_rhino.geometry.RhinoBrepEdge`], read-only
        The list of edges which comprise this brep.
    trims : list[:class:`compas_rhino.geometry.RhinoBrepTrim`], read-only
        The list of trims which comprise this brep.
    loops : list[:class:`compas_rhino.geometry.RhinoBrepLoop`], read-only
        The list of loops which comprise this brep.
    faces : list[:class:`compas_rhino.geometry.RhinoBrepFace`], read-only
        The list of faces which comprise this brep.
    frame : :class:`compas.geometry.Frame`, read-only
        The brep's origin (Frame.worldXY()).
    area : float, read-only
        The calculated area of this brep.
    volume : float, read-only
        The calculated volume of this brep.

    """

    def __init__(self):
        super(RhinoBrep, self).__init__()
        self._brep = Rhino.Geometry.Brep()

    def __deepcopy__(self, *args, **kwargs):
        return self.copy()

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def data(self):
        return {
            "vertices": [v.data for v in self.vertices],  # type: ignore
            "edges": [e.data for e in self.edges],  # type: ignore
            "faces": [f.data for f in self.faces],  # type: ignore
        }

    @classmethod
    def from_data(cls, data):
        """Construct a RhinoBrep from its data representation.

        Parameters
        ----------
        data : :obj:`dict`
            The data dictionary.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoBrep`

        """
        instance = cls()
        builder = _RhinoBrepBuilder()
        for v_data in data["vertices"]:
            RhinoBrepVertex.from_data(v_data, builder)
        for e_data in data["edges"]:
            RhinoBrepEdge.from_data(e_data, builder)
        for f_data in data["faces"]:
            RhinoBrepFace.from_data(f_data, builder)
        instance.native_brep = builder.result
        return instance

    def copy(self, cls=None):
        """Creates a deep-copy of this Brep using the native Rhino.Geometry.Brep copying mechanism.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoBrep`

        """
        # Avoid reconstruction when just copying. for sake of efficiency and stability
        return RhinoBrep.from_native(self._brep.DuplicateBrep())

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def is_manifold(self):
        return self._brep.IsManifold

    @property
    def is_solid(self):
        return self._brep.IsSolid

    @property
    def native_brep(self):
        return self._brep

    @native_brep.setter
    def native_brep(self, rhino_brep):
        self._brep = rhino_brep

    @property
    def vertices(self):
        return self.points

    @property
    def points(self):
        if self._brep:
            return [RhinoBrepVertex(vertex) for vertex in self._brep.Vertices]

    @property
    def edges(self):
        if self._brep:
            return [RhinoBrepEdge(edge) for edge in self._brep.Edges]

    @property
    def trims(self):
        if self._brep:
            return [RhinoBrepEdge(trim) for trim in self._brep.Trims]

    @property
    def loops(self):
        if self._brep:
            return [RhinoBrepLoop(loop) for loop in self._brep.Loops]

    @property
    def faces(self):
        if self._brep:
            return [RhinoBrepFace(face) for face in self._brep.Faces]

    @property
    def frame(self):
        return Frame.worldXY()

    @property
    def area(self):
        if self._brep:
            return self._brep.GetArea()

    @property
    def volume(self):
        if self._brep:
            return self._brep.GetVolume()

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_native(cls, rhino_brep):
        """Constructs a RhinoBrep from an instance of a Rhino.Geometry.Brep.

        Parameters
        ----------
        rhino_brep : :class:`Rhino.Geometry.Brep`
            The instance of Rhino brep to wrap.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoBrep`

        """
        brep = cls()
        brep._brep = rhino_brep
        return brep

    @classmethod
    def from_box(cls, box):
        """Create a RhinoBrep from a box.

        Parameters
        ----------
        box : :class:`compas.geometry.Box`
            The box geometry of the brep.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoBrep`

        """
        rhino_box = box_to_rhino(box)
        return cls.from_native(rhino_box.ToBrep())

    @classmethod
    def from_sphere(cls, sphere):
        """Create a RhinoBrep from a sphere.

        Parameters
        ----------
        sphere : :class:`compas.geometry.Sphere`
            The source sphere.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoBrep`

        """
        rhino_sphere = sphere_to_rhino(sphere)
        return cls.from_native(rhino_sphere.ToBrep())

    @classmethod
    def from_cylinder(cls, cylinder):
        """Create a RhinoBrep from a box.

        Parameters
        ----------
        box : :class:`compas.geometry.Box`
            The box geometry of the brep.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoBrep`

        """
        rhino_cylinder = cylinder_to_rhino(cylinder)
        return cls.from_native(rhino_cylinder.ToBrep(True, True))

    @classmethod
    def from_mesh(cls, mesh):
        """Create a RhinoBrep from a mesh.

        Parameters
        ----------
        mesh : :class:`compas.datastructures.Mesh`
            The source mesh.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoBrep`

        """
        rhino_mesh = mesh_to_rhino(mesh)
        return cls.from_native(Rhino.Geometry.Brep.CreateFromMesh(rhino_mesh, True))

    # ==============================================================================
    # Methods
    # ==============================================================================

    def contains(self, object):
        """Check if the Brep contains a given geometric primitive.

        Only closed and manifold breps can be checked for containment.

        Parameters
        ----------
        object : :class:`~compas.geometry.Point`, :class:`~compas.geometry.Curve`, :class:`~compas.geometry.Surface`
            The object to check for containment.

        Raises
        ------
        BrepError
            If the Brep is not solid.

        Returns
        -------
        bool
            True if the object is contained in the Brep, False otherwise.

        """
        if not self.is_solid:
            raise BrepError("Cannot check for containment if brep is not manifold or is not closed")

        if isinstance(object, Point):
            return self._brep.IsPointInside(point_to_rhino(object), TOLERANCE, False)
        else:
            raise NotImplementedError

    def to_meshes(self, u=16, v=16):
        """Convert the faces of this Brep shape to meshes.

        Parameters
        ----------
        u : int, optional
            The number of mesh faces in the U direction of the underlying surface geometry of every face of the Brep.
        v : int, optional
            The number of mesh faces in the V direction of the underlying surface geometry of every face of the Brep.

        Returns
        -------
        list[:class:`~compas.datastructures.Mesh`]

        """
        rg_meshes = Rhino.Geometry.Mesh.CreateFromBrep(self._brep, Rhino.Geometry.MeshingParamaters.Default)
        meshes = [mesh_to_compas(m) for m in rg_meshes]
        return meshes

    def transform(self, matrix):
        """Transform this Brep by given transformation matrix

        Parameters
        ----------
        matrix: :class:`compas.geometry.Transformation`
            The transformation matrix by which to transform this Brep.

        Returns
        -------
        None

        """
        self._brep.Transform(transformation_to_rhino(matrix))

    def trim(self, trimming_plane, tolerance=TOLERANCE):
        """Trim this brep by the given trimming plane

        Parameters
        ----------
        trimming_plane : :class:`compas.geometry.Frame` or :class:`compas.geometry.Plane`
            The frame or plane to use when trimming. The discarded bit is in the direction of the frame's normal.

        tolerance : float
            The precision to use for the trimming operation.

        Returns
        -------
        None

        """
        if isinstance(trimming_plane, Plane):
            trimming_plane = Frame.from_plane(trimming_plane)
        rhino_frame = frame_to_rhino(trimming_plane)
        results = self._brep.Trim(rhino_frame, tolerance)
        if not results:
            raise BrepTrimmingError("Trim operation ended with no result")

        self._brep = results[0].CapPlanarHoles(TOLERANCE)

    @classmethod
    def from_boolean_difference(cls, breps_a, breps_b):
        """Construct a Brep from the boolean difference of two groups of Breps.

        Parameters
        ----------
        breps_a : :class:`compas_rhino.geometry.RhinoBrep` or list(:class:`compas_rhino.geometry.RhinoBrep`)
            One or more Breps from which to substract.
        breps_b : :class:`compas_rhino.geometry.RhinoBrep` or list(:class:`compas_rhino.geometry.RhinoBrep`)
            One or more Breps to substract.

        Returns
        -------
        list(:class:`compas_rhino.geometry.RhinoBrep`)
            list of one or more resulting Breps.

        """
        if not isinstance(breps_a, list):
            breps_a = [breps_a]
        if not isinstance(breps_b, list):
            breps_b = [breps_b]
        resulting_breps = Rhino.Geometry.Brep.CreateBooleanDifference(
            [b.native_brep for b in breps_a],
            [b.native_brep for b in breps_b],
            TOLERANCE,
        )
        return [RhinoBrep.from_native(brep) for brep in resulting_breps]

    @classmethod
    def from_boolean_union(cls, breps_a, breps_b):
        """Construct a Brep from the boolean union of two groups of Breps.

        Parameters
        ----------
        breps_a : :class:`compas_rhino.geometry.RhinoBrep` or list(:class:`compas_rhino.geometry.RhinoBrep`)
            One of more breps to join.
        breps_b : :class:`compas_rhino.geometry.RhinoBrep` or list(:class:`compas_rhino.geometry.RhinoBrep`)
            Another one of more breps to join.

        Returns
        -------
        list(:class:`compas_rhino.geometry.RhinoBrep`)
            list of one or more resulting Breps.

        """
        if not isinstance(breps_a, list):
            breps_a = [breps_a]
        if not isinstance(breps_b, list):
            breps_b = [breps_b]

        resulting_breps = Rhino.Geometry.Brep.CreateBooleanUnion([b.native_brep for b in breps_a + breps_b], TOLERANCE)
        return [RhinoBrep.from_native(brep) for brep in resulting_breps]

    @classmethod
    def from_boolean_intersection(cls, breps_a, breps_b):
        """Construct a Brep from the boolean intersection of two groups of Breps.

        Parameters
        ----------
        breps_a : :class:`compas_rhino.geometry.RhinoBrep` or list(:class:`compas_rhino.geometry.RhinoBrep`)
            One or more Breps to instrsect.
        breps_b : :class:`compas_rhino.geometry.RhinoBrep` or list(:class:`compas_rhino.geometry.RhinoBrep`)
            Another one or more Breps to intersect.

        Returns
        -------
        list(:class:`compas_rhino.geometry.RhinoBrep`)
            list of one or more resulting Breps.

        """
        if not isinstance(breps_a, list):
            breps_a = [breps_a]
        if not isinstance(breps_b, list):
            breps_b = [breps_b]
        resulting_breps = Rhino.Geometry.Brep.CreateBooleanIntersection(
            [b.native_brep for b in breps_a],
            [b.native_brep for b in breps_b],
            TOLERANCE,
        )
        return [RhinoBrep.from_native(brep) for brep in resulting_breps]

    def split(self, cutter):
        """Splits a Brep into pieces using a Brep as a cutter.

        Parameters
        ----------
        cutter : :class:`compas_rhino.geometry.RhinoBrep`
            Another Brep to use as a cutter.

        Returns
        -------
        list(:class:`compas_rhino.geometry.RhinoBrep`)
            list of zero or more resulting Breps.

        """
        resulting_breps = self._brep.Split(cutter.native_brep, TOLERANCE)
        return [RhinoBrep.from_native(brep) for brep in resulting_breps]
