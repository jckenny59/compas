from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry.objects import Vector

from compas.geometry import distance_point_point
from compas.geometry import distance_point_line
from compas.geometry import distance_point_plane

from compas.geometry import is_point_on_line
from compas.geometry import is_point_on_line_xy
from compas.geometry import is_point_on_segment
from compas.geometry import is_point_on_segment_xy
from compas.geometry import is_point_on_polyline
from compas.geometry import is_point_on_polyline_xy

# from compas.geometry import is_point_on_circle

from compas.geometry import is_point_in_triangle
from compas.geometry import is_point_in_triangle_xy
from compas.geometry import is_point_in_circle
from compas.geometry import is_point_in_circle_xy

from compas.geometry import is_polygon_convex_xy

from compas.geometry import is_point_in_polygon_xy
from compas.geometry import is_point_in_convex_polygon_xy

from compas.geometry import transform_points

from compas.geometry import translate_points
from compas.geometry import scale_points
from compas.geometry import rotate_points
from compas.geometry import project_points_plane
from compas.geometry import project_points_line


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'GNU - General Public License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['Point', ]


class Point(object):
    """A location in three-dimensional space.

    Parameters
    ----------
    x : float
        The X coordinate of the point.
    y : float
        The Y coordinate of the point.
    z : float, optional
        The Z coordinate of the point.
        Default is ``0.0``.
    precision : integer, optional
        The number of fractional digits used in the representation of the coordinates of the point.
        Default is ``3``.

    Examples
    --------
    >>> p1 = Point(1, 2, 3)
    >>> p2 = Point(4, 5, 6)

    >>> p1.x
    1.0
    >>> p1[0]
    1.0
    >>> p1[5]
    1.0
    >>> p1[-3]
    1.0
    >>> p1[-6]
    1.0

    >>> p1 + p2
    [5.0, 7.0, 9.0]
    >>> p1 + [4, 5, 6]
    [5.0, 7.0, 9.0]
    >>> p1 * 2
    [2.0, 4.0, 6.0]
    >>> p1 ** 2
    [1.0, 4.0, 9.0]
    >>> p1
    [1.0, 2.0, 3.0]

    >>> p1 += p2
    >>> p1 *= 2
    >>> p1 **= 2
    >>> p1
    [100.0, 196.0, 324.0]

    Notes
    -----
    A ``Point`` object supports direct access to its xyz coordinates through
    the dot notation, as well list-style access using indices. Indexed
    access is implemented such that the ``Point`` behaves like a circular
    list.

    For more info, see [1]_.

    References
    ----------
    .. [1] Stack Overflow. *Pythonic Circular List*.
           Available at: https://stackoverflow.com/questions/8951020/pythonic-circular-list.

    """

    __slots__ = ['_x', '_y', '_z', '_precision']

    def __init__(self, x, y, z=0.0, precision=None):
        self._x = 0.0
        self._y = 0.0
        self._z = 0.0
        self._precision = 3
        self.x = x
        self.y = y
        self.z = z
        self.precision = precision

    # ==========================================================================
    # factory
    # ==========================================================================

    # ==========================================================================
    # descriptors
    # ==========================================================================

    @property
    def x(self):
        """:obj:`float`: The X coordinate of the point."""
        return self._x

    @x.setter
    def x(self, x):
        self._x = float(x)

    @property
    def y(self):
        """:obj:`float`: The Y coordinate of the point."""
        return self._y

    @y.setter
    def y(self, y):
        self._y = float(y)

    @property
    def z(self):
        """:obj:`float`: The Z coordinate of the point."""
        return self._z

    @z.setter
    def z(self, z):
        self._z = float(z)

    @property
    def precision(self):
        """:obj:`int`: The number of fractional digits used in the representation of the coordinates of the point."""
        return self._precision

    @precision.setter
    def precision(self, value):
        if isinstance(value, int) and value > 0:
            self._precision = value

    # ==========================================================================
    # representation
    # ==========================================================================

    def __repr__(self):
        return 'Point({0:.{3}f}, {1:.{3}f}, {2:.{3}f})'.format(self.x, self.y, self.z, self.precision)

    def __len__(self):
        return 3

    # ==========================================================================
    # access
    # ==========================================================================

    def __getitem__(self, key):
        if isinstance(key, slice):
            return [self[i] for i in range(*key.indices(len(self)))]
        i = key % 3
        if i == 0:
            return self.x
        if i == 1:
            return self.y
        if i == 2:
            return self.z
        raise KeyError

    def __setitem__(self, key, value):
        i = key % 3
        if i == 0:
            self.x = value
            return
        if i == 1:
            self.y = value
            return
        if i == 2:
            self.z = value
            return
        raise KeyError

    def __iter__(self):
        return iter([self.x, self.y, self.z])

    # ==========================================================================
    # comparison
    # ==========================================================================

    def __eq__(self, other):
        """Is this point equal to the other point? Two points are considered
        equal if their XYZ coordinates are identical.

        Parameters
        ----------
        other : point
            The point to compare.

        Returns
        -------
        bool
            True if the points are equal.
            False otherwise.

        """
        return self.x == other[0] and self.y == other[1] and self.z == other[2]

    # ==========================================================================
    # operators
    # ==========================================================================

    def __add__(self, other):
        """Return a ``Point`` that is the sum of this ``Point`` and another point.

        Parameters
        ----------
        other : point
            The point to add.

        Returns
        -------
        Point
            The resulting new point.

        """
        return Point(self.x + other[0], self.y + other[1], self.z + other[2])

    def __sub__(self, other):
        """Return a ``Vector`` that is the the difference between this ``Point``
        and another point.

        Parameters
        ----------
        other : point
            The point to subtract.

        Returns
        -------
        Vector
            A vector from other to self.

        """
        x = self.x - other[0]
        y = self.y - other[1]
        z = self.z - other[2]
        return Vector(x, y, z)

    def __mul__(self, n):
        """Create a ``Point`` from the coordinates of the current ``Point`` multiplied
        by the given factor.

        Parameters
        ----------
        n : float
            The multiplication factor.

        Returns
        -------
        Point
            The resulting new ``Point``.

        """
        return Point(n * self.x, n * self.y, n * self.z)

    def __pow__(self, n):
        """Create a ``Point`` from the coordinates of the current ``Point`` raised
        to the given power.

        Parameters
        ----------
        n : float
            The power.

        Returns
        -------
        Point
            A new point with raised coordinates.

        """
        return Point(self.x ** n, self.y ** n, self.z ** n)

    # ==========================================================================
    # in-place operators
    # ==========================================================================

    def __iadd__(self, other):
        """Add the coordinates of the other point to this ``Point``.

        Parameters
        ----------
        other : point
            The point to add.

        """
        self.x += other[0]
        self.y += other[1]
        self.z += other[2]

    def __isub__(self, other):
        """Subtract the coordinates of the other point from this ``Point``.

        Parameters
        ----------
        other : point
            The point to subtract.

        """
        self.x -= other[0]
        self.y -= other[1]
        self.z -= other[2]

    def __imul__(self, n):
        """Multiply the coordinates of this ``Point`` by the given factor.

        Parameters
        ----------
        n : float
            The multiplication factor.

        """
        self.x *= n
        self.y *= n
        self.z *= n

    def __ipow__(self, n):
        """Raise the coordinates of this ``Point`` to the given power.

        Parameters
        ----------
        n : float
            The power.

        """
        self.x **= n
        self.y **= n
        self.z **= n

    # ==========================================================================
    # helpers
    # ==========================================================================

    def copy(self):
        """Make a copy of this ``Point``.

        Returns
        -------
        Point
            The copy.

        """
        cls = type(self)
        return cls(self.x, self.y, self.z, self.precision)

    # ==========================================================================
    # methods
    # ==========================================================================

    def distance_to_point(self, point):
        """Compute the distance to another point.

        Parameters
        ----------
        point : point
            The other point.

        Returns
        -------
        float
            The distance.

        """
        return distance_point_point(self, point)

    def distance_to_line(self, line):
        """Compute the distance to a line.

        Parameters
        ----------
        line : line
            The line.

        Returns
        -------
        float
            The distance.

        """
        return distance_point_line(self, line)

    def distance_to_plane(self, plane):
        """Compute the distance to a plane.

        Parameters
        ----------
        plane : plane
            The plane.

        Returns
        -------
        float
            The distance.

        """
        return distance_point_plane(self, plane)

    def on_line(self, line, xy=False):
        """Determine if the point lies on the given line.

        Parameters
        ----------
        line : line
            The line.
        xy : bool, optional
            Assume the test is performed in the XY plane.
            Default is False.

        Returns
        -------
        bool
            True, if the point lies on the line.
            False, otherwise.

        """
        if xy:
            is_point_on_line_xy(self, line)
        return is_point_on_line(self, line)

    def on_segment(self, segment, xy=False):
        """Determine if the point lies on the given segment.

        Parameters
        ----------
        segment : segment
            The segment.
        xy : bool, optional
            Assume the test is performed in the XY plane.
            Default is False.

        Returns
        -------
        bool
            True, if the point lies on the segment.
            False, otherwise.

        """
        if xy:
            return is_point_on_segment_xy(self, segment)
        return is_point_on_segment(self, segment)

    def on_polyline(self, polyline, xy=False):
        """Determine if the point lies on the given polyline.

        Parameters
        ----------
        polyline : polyline
            The polyline.
        xy : bool, optional
            Assume the test is performed in the XY plane.
            Default is False.

        Returns
        -------
        bool
            True, if the point lies on the polyline.
            False, otherwise.

        """
        if xy:
            return is_point_on_polyline_xy(self, polyline)
        return is_point_on_polyline(self, polyline)

    def on_circle(self, circle, xy=False):
        """Determine if the point lies on the given circle.

        Parameters
        ----------
        circle : circle
            The circle.
        xy : bool, optional
            Assume the test is performed in the XY plane.
            Default is False.

        Returns
        -------
        bool
            True, if the point lies on the circle.
            False, otherwise.

        """
        raise NotImplementedError

    def in_triangle(self, triangle, xy=False):
        """Determine if the point lies in the given triangle.

        Parameters
        ----------
        triangle : triangle
            The triangle.
        xy : bool, optional
            Assume the test is performed in the XY plane.
            Default is False.

        Returns
        -------
        bool
            True, if the point lies in the triangle.
            False, otherwise.

        """
        if xy:
            return is_point_in_triangle_xy(self, triangle)
        return is_point_in_triangle(self, triangle)        

    def in_polygon(self, polygon):
        """Determine if the point lies in the given polygon.

        Parameters
        ----------
        polyline : polyline
            The polyline.

        Returns
        -------
        bool
            True, if the point lies on the polyline.
            False, otherwise.

        """
        if is_polygon_convex_xy(polygon):
            return is_point_in_convex_polygon_xy(self, polygon)
        return is_point_in_polygon_xy(self, polygon)


    def in_circle(self, circle, xy=False):
        """Determine if the point lies on the given polyline.

        Parameters
        ----------
        polyline : polyline
            The polyline.
        xy : bool, optional
            Assume the test is performed in the XY plane.
            Default is False.

        Returns
        -------
        bool
            True, if the point lies on the polyline.
            False, otherwise.

        """
        if xy:
            return is_point_in_circle_xy(self, circle)
        return is_point_in_circle(self, circle)

    def in_polyhedron(self, polyhedron):
        """Determine if the point lies on the given polyline.

        Parameters
        ----------
        polyline : polyline
            The polyline.

        Returns
        -------
        bool
            True, if the point lies on the polyline.
            False, otherwise.

        """
        raise NotImplementedError

    # ==========================================================================
    # tranformations
    # ==========================================================================

    def transform(self, matrix):
        """Transform this ``Point`` using a given transformation matrix.

        Parameters
        ----------
        matrix : list of list
            The transformation matrix.

        """
        point = transform_points([self, ], matrix)[0]
        self.x = point[0]
        self.y = point[1]
        self.z = point[2]

    def translate(self, vector):
        """Translate this ``Point`` by a vector.

        Parameters
        ----------
        vector : vector
            The translation vector.

        """
        point = translate_points([self, ], vector)[0]
        self.x = point[0]
        self.y = point[1]
        self.z = point[2]

    def scale(self, factor):
        """Scale the coordinates of this ``Point`` by a given factor.

        Parameters
        ----------
        factor : float
            The scale factor.

        """
        point = scale_points([self, ], factor)[0]
        self.x = point[0]
        self.y = point[1]
        self.z = point[2]

    def rotate(self, angle, axis=None, origin=None):
        """Rotate this ``Vector`` over the given angle around the specified axis
        and origin.

        Parameters
        ----------
        angle : float
            The rotation angle in radians.
        axis : vector, optional
            The rotation axis.
            Default is the Z axis (``[0.0, 0.0, 1.0]``).
        origin : point, optional
            The origin of the rotation axis.
            Default is ``[0.0, 0.0, 0.0]``.

        """
        if axis is None:
            axis = [0.0, 0.0, 1.0]
        if origin is None:
            origin = [0.0, 0.0, 0.0]

        point = rotate_points([self, ], angle, axis, origin)[0]
        self.x = point[0]
        self.y = point[1]
        self.z = point[2]

    def project_to_line(self, line):
        point = project_points_line([self, ], line)[0]
        self.x = point[0]
        self.y = point[1]
        self.z = point[2]

    def project_to_plane(self, plane):
        point = project_points_plane([self, ], plane)[0]
        self.x = point[0]
        self.y = point[1]
        self.z = point[2]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.geometry import Point
    from compas.geometry import Vector
    from compas.geometry import Plane
    from compas.geometry import Line
    from compas.geometry import Polygon


    point    = Point(0.0, 0.0, 0.0)
    normal   = Vector(0.0, 0.0, 1.0)
    plane    = Plane(point, normal)
    line     = Line([0.0, 0.0, 0.0], [1.0, 0.0, 0.0])
    triangle = Polygon([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0]])
    polygon  = Polygon([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]])

    p = Point(1.0, 1.0, 1.0)

    print(*p)

    print(repr(p))

    print(p.distance_to_point(point))
    print(p.distance_to_line(line))
    print(p.distance_to_plane(plane))
    print(p.in_triangle(triangle))

