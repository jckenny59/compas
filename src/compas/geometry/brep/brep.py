from compas.geometry import Geometry

from . import new_brep
from . import from_brepfaces
from . import from_box
from . import from_cylinder
from . import from_sphere
from . import from_mesh
from . import from_cone
from . import from_surface
from . import from_torus
from . import from_extrusion
from . import from_boolean_difference
from . import from_boolean_intersection
from . import from_boolean_union
from . import from_curves
from . import from_polygons
from . import from_step
from . import from_sweep
from . import from_native


LINEAR_DEFLECTION = 1e-3


class BrepType(object):
    """Possible types of a Brep

    Attributes
    ----------
    COMPOUND
    COMPSOLID
    SHELL
    FACE
    WIRE
    EDGE
    VERTEX
    SHAPE

    """

    COMPOUND = 0
    COMPSOLID = 1
    SHELL = 2
    FACE = 3
    WIRE = 4
    EDGE = 5
    VERTEX = 6
    SHAPE = 7


class BrepOrientation(object):
    """Possible orientations of a Brep

    Attributes
    ----------
    FORWARD
    REVERSED
    INTERNAL
    EXTERNAL

    """

    FORWARD = 0
    REVERSED = 1
    INTERNAL = 2
    EXTERNAL = 3


class Brep(Geometry):
    """Contains the topological and geometrical information of a Brep shape.

    This class serves as an interface for a Brep and allows instantiating a Brep object depending on the available Backend.
    Note: this is not a full implementation of Brep and rather relies on COMPAS's plugin system for actual implementation.

    Attributes
    ----------
    vertices : list[:class:`compas.geometry.BrepVertex`], read-only
        The vertices of the Brep.
    edges : list[:class:`compas.geometry.BrepEdge`], read-only
        The edges of the Brep.
    trims : list[:class:`compas.geometry.BrepTrim`], read-only
        The trims of the Brep.
    loops : list[:class:`compas.geometry.BrepLoop`], read-only
        The loops of the Brep.
    faces : list[:class:`compas.geometry.BrepFace`], read-only
        The faces of the Brep.
    frame : :class:`compas.geometry.Frame`, read-only
        The local coordinate system of the Brep.
    area : float, read-only
        The surface area of the Brep.
    volume : float, read-only
        The volume of the regions contained by the Brep.
    solids : list[:class:`compas.geometry.Brep`], read-only
        The solids of this brep.
    shells : list[:class:`compas.geometry.Brep`], read-only
        The shells of this brep.
    points : list[:class:`compas.geometry.Point`], read-only
        The points of this brep.
    centroid : :class:`compas.geometry.Point`, read-only
        The centroid of this brep.
    is_valid : bool, read-only
        True if this brep is valid, False otherwise
    is_solid : bool, read-only
        True if this brep is a solid, False otherwise.
    is_compound : bool, read-only
        True if this brep's type is a compound, False otherwise.
    is_compoundsolid : bool, read-only
        True if this brep's type is a compoundsolid, False otherwise.
    is_orientable : bool, read-only
        True if this brep is orientable, False otherwise.
    is_closed : bool, read-only
        True if this brep is closed, False otherwise.
    is_infinite : bool, read-only
        True if this brep is infinite, False otherwise.
    is_convex : bool, read-only
        True if this brep is convex, False otherwise.
    is_manifold : bool, read-only
        True if this brep is a manifold, False otherwise.
    is_surface : bool, read-only
        True if this brep is a surface, False otherwise.

    """

    def __new__(cls, *args, **kwargs):
        return new_brep(cls, *args, **kwargs)

    def __init__(self, name=None):
        super(Brep, self).__init__(name=name)

    def __str__(self):
        lines = [
            "Brep",
            "-----",
            "Vertices: {}".format(len(self.vertices)),
            "Edges: {}".format(len(self.edges)),
            "Loops: {}".format(len(self.loops)),
            "Faces: {}".format(len(self.faces)),
            "Frame: {}".format(self.frame),
            "Area: {}".format(self.area),
            "Volume: {}".format(self.volume),
        ]
        return "\n".join(lines)

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def dtype(self):
        return "compas.geometry/Brep"

    @property
    def data(self):
        faces = []
        for face in self.faces:
            faces.append(face.data)
        return {"faces": faces}

    @classmethod
    def from_data(cls, data):
        # faces = []
        # for face in data["faces"]:
        #     faces.append(BrepFace.from_data(face))
        # return cls.from_brepfaces(faces)
        pass

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def native_brep(self):
        raise NotImplementedError

    @property
    def orientation(self):
        raise NotImplementedError

    @property
    def type(self):
        raise NotImplementedError

    @property
    def is_valid(self):
        raise NotImplementedError

    @property
    def is_shell(self):
        raise NotImplementedError

    @property
    def is_solid(self):
        raise NotImplementedError

    @property
    def is_compound(self):
        raise NotImplementedError

    @property
    def is_compoundsolid(self):
        raise NotImplementedError

    @property
    def is_orientable(self):
        raise NotImplementedError

    @property
    def is_closed(self):
        raise NotImplementedError

    @property
    def is_infinite(self):
        raise NotImplementedError

    @property
    def is_convex(self):
        raise NotImplementedError

    @property
    def is_manifold(self):
        raise NotImplementedError

    @property
    def is_surface(self):
        raise NotImplementedError

    # ==============================================================================
    # Geometric Components
    # ==============================================================================

    @property
    def points(self):
        raise NotImplementedError

    @property
    def curves(self):
        raise NotImplementedError

    @property
    def surfaces(self):
        raise NotImplementedError

    # ==============================================================================
    # Topological Components
    # ==============================================================================

    @property
    def vertices(self):
        raise NotImplementedError

    @property
    def edges(self):
        raise NotImplementedError

    @property
    def trims(self):
        raise NotImplementedError

    @property
    def loops(self):
        raise NotImplementedError

    @property
    def faces(self):
        raise NotImplementedError

    @property
    def shells(self):
        raise NotImplementedError

    @property
    def solids(self):
        raise NotImplementedError

    # ==============================================================================
    # Geometric Properties
    # ==============================================================================

    @property
    def frame(self):
        raise NotImplementedError

    @property
    def area(self):
        raise NotImplementedError

    @property
    def volume(self):
        raise NotImplementedError

    @property
    def centroid(self):
        raise NotImplementedError

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_box(cls, box):
        """Construct a Brep from a COMPAS box.

        Parameters
        ----------
        box : :class:`compas.geometry.Box`

        Returns
        -------
        :class:`compas.geometry.Brep`

        """
        return from_box(box)

    @classmethod
    def from_brepfaces(cls, faces):
        """Make a Brep from a list of Brep faces forming an open or closed shell.

        Parameters
        ----------
        faces : list[:class:`compas.geometry.BrepFace`]

        Returns
        -------
        :class:`compas.geometry.Brep`

        """
        return from_brepfaces(faces)

    @classmethod
    def from_cone(cls, cone):
        """Construct a Brep from a COMPAS cone.

        Parameters
        ----------
        cone : :class:`compas.geometry.Cone`

        Returns
        -------
        :class:`compas.geometry.Brep`

        """
        return from_cone(cone)

    @classmethod
    def from_curves(cls, curves):
        """Construct a Brep from a set of curves.

        Parameters
        ----------
        curves : list[:class:`compas.geometry.NurbsCurve`]

        Returns
        -------
        :class:`compas.geometry.Brep`

        """
        return from_curves(curves)

    @classmethod
    def from_cylinder(cls, cylinder):
        """Construct a Brep from a COMPAS cylinder.

        Parameters
        ----------
        cylinder : :class:`compas.geometry.Cylinder`

        Returns
        -------
        :class:`compas.geometry.Brep`

        """
        return from_cylinder(cylinder)

    @classmethod
    def from_extrusion(cls, curve, vector):
        """Construct a Brep by extruding a closed curve along a direction vector.

        Parameters
        ----------
        curve : :class:`compas.geometry.Curve`
            The curve to extrude
        vector : :class:`compas.geometry.Vector`
            The vector to extrude the curve by

        Returns
        -------
        :class:`compas.geometry.Brep`

        """
        return from_extrusion(curve, vector)

    @classmethod
    def from_iges(cls, filename):
        """Construct a Brep from the data contained in an IGES file.

        Parameters
        ----------
        filename : str

        Returns
        -------
        :class:`compas.geometry.Brep`

        """
        return from_iges(filename)

    @classmethod
    def from_loft(cls, curves):
        """Construct a Brep by lofting a set of curves.

        Parameters
        ----------
        curves : list[:class:`compas.geometry.Curve`]

        Returns
        -------
        :class:`compas.geometry.Brep`

        """
        return from_loft(curves)

    @classmethod
    def from_mesh(cls, mesh):
        """Construct a Brep from a COMPAS mesh.

        Parameters
        ----------
        mesh : :class:`compas.datastructures.Mesh`

        Returns
        -------
        :class:`compas.geometry.Brep`

        """
        return from_mesh(mesh)

    @classmethod
    def from_native(cls, native_brep):
        """Creates a Brep from an instance of a native backend Brep type.

        Parameters
        ----------
        brep : an instance of a Brep from a supported Brep backend
            e.g. Rhino.Geometry.Brep

        Returns
        -------
        :class:`compas.geometry.Brep`
        """
        return from_native(native_brep)

    @classmethod
    def from_pipe(cls, curve, radius, thickness=None):
        """Construct a Brep by extruding a closed curve along a path curve.

        Parameters
        ----------
        curve : :class:`compas.geometry.Curve`
            The curve to extrude
        radius : float
            The radius of the pipe.
        thickness : float, optional
            The thickness of the pipe.
            The thickness should be smaller than the radius.

        Returns
        -------
        :class:`compas.geometry.Brep`

        """
        return from_pipe(curve, radius, thickness=thickness)

    @classmethod
    def from_polygons(cls, polygons):
        """Construct a Brep from a set of polygons.

        Parameters
        ----------
        polygons : list[:class:`compas.geometry.Polygon`]

        Returns
        -------
        :class:`compas.geometry.Brep`

        """
        return from_polygons(polygons)

    @classmethod
    def from_sphere(cls, sphere):
        """Construct a Brep from a COMPAS sphere.

        Parameters
        ----------
        sphere : :class:`compas.geometry.Sphere`

        Returns
        -------
        :class:`compas.geometry.Brep`

        """
        return from_sphere(sphere)

    @classmethod
    def from_step(cls, filename):
        """Conctruct a Brep from the data contained in a STEP file.

        Parameters
        ----------
        filename : str

        Returns
        -------
        :class:`compas.geometry.Brep`

        """
        return from_step(filename)

    @classmethod
    def from_sweep(cls, profile, path):
        """Construct a BRep by sweeping a profile along a path.

        Parameters
        ----------
        profile : :class:`compas.geometry.BrepEdge` or :class:`compas.geometry.BrepFace`
            the profile to sweep. Either an edge or a face.
        path : :class:`compas.geometry.BrepLoop`
            the path to sweep along

        Returns
        -------
        :class:`compas.geometry.Brep`

        """
        return from_sweep(profile, path)

    @classmethod
    def from_torus(cls, torus):
        """Construct a Brep from a COMPAS torus.

        Parameters
        ----------
        torus : :class:`compas.geometry.Torus`

        Returns
        -------
        :class:`compas.geometry.BRep`

        """
        return from_torus(torus)

    # ==============================================================================
    # Boolean Constructors
    # ==============================================================================

    @classmethod
    def from_boolean_difference(cls, brep_a, brep_b):
        """Construct a Brep from the boolean difference of two other Breps.

        Parameters
        ----------
        brep_a : :class:`compas.geometry.Brep`
        brep_b : :class:`compas.geometry.Brep`

        Returns
        -------
        :class:`compas.geometry.Brep`

        """
        return from_boolean_difference(brep_a, brep_b)

    @classmethod
    def from_boolean_intersection(cls, brep_a, brep_b):
        """Construct a BRep from the boolean intersection of two other Breps.

        Parameters
        ----------
        brep_a : :class:`compas.geometry.Brep`
        brep_b : :class:`compas.geometry.Brep`

        Returns
        -------
        :class:`compas.geometry.Brep`

        """
        return from_boolean_intersection(brep_a, brep_b)

    @classmethod
    def from_boolean_union(cls, brep_a, brep_b):
        """Construct a Brep from the boolean union of two other Breps.

        Parameters
        ----------
        brep_a : :class:`compas.geometry.Brep`
        brep_b : :class:`compas.geometry.Brep`

        Returns
        -------
        :class:`compas.geometry.Brep`

        """
        return from_boolean_union(brep_a, brep_b)

    def __sub__(self, other):
        """Compute the boolean difference using the "-" operator of this shape and another.

        Parameters
        ----------
        other : :class:`compas.geometry.Brep`
            The other Brep to create a union with.

        Returns
        -------
        :class:`compas.geometry.Brep`
            The Brep resulting from the difference operation.

        """
        results = type(self).from_boolean_difference(self, other)
        if isinstance(results, list):
            results = results[0]
        return results

    def __and__(self, other):
        """Compute the boolean intersection using the "&" operator of this shape and another.

        Parameters
        ----------
        other : :class:`compas.geometry.Brep`
            The other Brep to create a union with.

        Returns
        -------
        :class:`compas.geometry.Brep`
            The Brep resulting from the intersection operation.

        """
        results = type(self).from_boolean_intersection(self, other)
        if isinstance(results, list):
            results = results[0]
        return results

    def __add__(self, other):
        """Compute the boolean union using the "+" operator of this Brep and another.

        Parameters
        ----------
        other : :class:`compas.geometry.Brep`
            The other Brep to create a union with.

        Returns
        -------
        :class:`compas.geometry.Brep`
            The Brep resulting from the union operation.

        """
        results = type(self).from_boolean_union(self, other)
        if isinstance(results, list):
            results = results[0]
        return results

    # ==============================================================================
    # Converters
    # ==============================================================================

    def to_json(self, filepath):
        """Export the BRep to a JSON file.

        Parameters
        ----------
        filepath : str
            Location of the file.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def to_step(self, filepath):
        """Write the BRep shape to a STEP file.

        Parameters
        ----------
        filepath : str
            Location of the file.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def to_tesselation(self, linear_deflection=LINEAR_DEFLECTION):
        """Create a tesselation of the shape for visualisation.

        Parameters
        ----------
        linear_deflection : float, optional
            Allowable deviation between curved geometry and mesh discretisation.

        Returns
        -------
        :class:`compas.datastructures.Mesh`

        """
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
        list[:class:`compas.datastructures.Mesh`]

        """
        raise NotImplementedError

    def to_viewmesh(self, precision):
        """Convert this Brep to a view mesh.

        Parameters
        ----------
        precision : float
            The presicion by which the mesh is estimated

        Returns
        -------
        :class:`compas.datastructure.Mesh`

        """
        raise NotImplementedError

    # ==============================================================================
    # Relationships
    # ==============================================================================

    def vertex_neighbors(self, vertex):
        """Identify the neighbouring vertices of a given vertex.

        Parameters
        ----------
        vertex : :class:`compas.geometry.BrepVertex`

        Returns
        -------
        list[:class:`compas.geometry.BrepVertex`]

        """
        raise NotImplementedError

    def vertex_edges(self, vertex):
        """Identify the edges connected to a given vertex.

        Parameters
        ----------
        vertex : :class:`compas.geometry.BrepVertex`

        Returns
        -------
        list[:class:`compas.geometry.BrepEdge`]

        """
        raise NotImplementedError

    def vertex_faces(self, vertex):
        """Identify the faces connected to a vertex.

        Parameters
        ----------
        vertex : :class:`compas.geometry.BrepVertex`

        Returns
        -------
        list[:class:`compas.geometry.BrepFace`]

        """
        raise NotImplementedError

    # ==============================================================================
    # Other Methods
    # ==============================================================================

    def trim(self, trimming_plane, tolerance):
        """Trim this Brep using the given trimming plane.

        Parameters
        ----------
        trimming_plane : :class:`compas.geometry.Frame`
            defines the trimming plane
        tolerance: float
            the tolerance to use when trimming

        Returns
        -------
        None

        """
        raise NotImplementedError

    def make_solid(self):
        """Convert the current shape to a solid if it is a shell.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def sew(self):
        """Sew together the individual parts of the shape.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def fix(self):
        """Fix the shell.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def cull_unused_vertices(self):
        """Remove all unused vertices.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def cull_unused_edges(self):
        """Remove all unused edges.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def cull_unused_loops(self):
        """Remove all unused loops.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def cull_unused_faces(self):
        """Remove all unused faces.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def contours(self, planes):
        """Generate contour lines by slicing the Brep shape with a series of planes.

        Parameters
        ----------
        planes : list[:class:`compas.geometry.Plane`]
            The slicing planes.

        Returns
        -------
        list[list[:class:`compas.geometry.Polyline`]]
            A list of polylines per plane.

        """
        raise NotImplementedError

    def slice(self, plane):
        """Slice through the BRep with a plane.

        Parameters
        ----------
        plane : :class:`compas.geometry.Plane`

        Returns
        -------
        :class:`compas.geometry.BrepFace`

        """

    def split(self, cutter):
        """Slice through the BRep with a plane.

        Parameters
        ----------
        cutter : :class:`compas.geomtery.Brep`
            Another Brep to use as a cutter.

        Returns
        -------
        list[:class:`compas.geometry.Brep`]

        """
        raise NotImplementedError

    def overlap(self, other, deflection=LINEAR_DEFLECTION, tolerance=0.0):
        """Compute the overlap between this BRep and another.

        Parameters
        ----------
        other : :class:`compas.geometry.Brep`
            The other Brep.
        deflection : float, optional
            Allowable deflection for mesh generation used for proximity detection.
        tolerance : float, optional
            Tolerance for overlap calculation.

        Returns
        -------
        tuple[list[:class:`compas.geometry.BrepFace`]]

        """
        raise NotImplementedError
