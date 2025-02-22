from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import sqrt
from math import fabs


def vector_average(vector):
    """Average of a vector.

    Parameters
    ----------
    vector : [float, float, float] | :class:`compas.geometry.Vector`
        List of values.

    Returns
    -------
    float
        The mean value.
    """
    return sum(vector) / float(len(vector))


def vector_variance(vector):
    """Variance of a vector.

    Parameters
    ----------
    vector : [float, float, float] | :class:`compas.geometry.Vector`
        List of values.

    Returns
    -------
    float
        The variance value.
    """
    m = vector_average(vector)
    return (sum([(i - m) ** 2 for i in vector]) / float(len(vector))) ** 0.5


def vector_standard_deviation(vector):
    """Standard deviation of a vector.

    Parameters
    ----------
    vector : [float, float, float] | :class:`compas.geometry.Vector`
        List of values.

    Returns
    -------
    float
        The standard deviation value.
    """
    return vector_variance(vector) ** 0.5


def close(value1, value2, tol=1e-05):
    """Returns True if two values are equal within a tolerance.

    Parameters
    ----------
    value1 : float or int
    value2 : float or int
    tol : float, optional
        The tolerance for comparing values.

    Returns
    -------
    bool
        True if the values are closer than the tolerance.
        False otherwise.

    Examples
    --------
    >>> close(1., 1.001)
    False
    >>> close(1., 1.001, tol=1e-2)
    True
    """
    return fabs(value1 - value2) < tol


def allclose(l1, l2, tol=1e-05):
    """Returns True if two lists are element-wise equal within a tolerance.

    Parameters
    ----------
    l1 : sequence[float]
        The first list of values.
    l2 : sequence[float]
        The second list of values.
    tol : float, optional
        The tolerance for comparing values.

    Returns
    -------
    bool
        True if all corresponding values of the two lists are closer than the tolerance.
        False otherwise.

    Notes
    -----
    The function is similar to NumPy's *allclose* function [1]_.

    References
    ----------
    .. [1] https://docs.scipy.org/doc/numpy/reference/generated/numpy.allclose.html

    Examples
    --------
    >>> allclose([0.1, 0.2, 0.3, 0.4], [0.1, 0.20001, 0.3, 0.4])
    True

    >>> allclose([0.1, 0.2, 0.3, 0.4], [0.1, 0.20001, 0.3, 0.4], tol=1e-6)
    False

    """

    if any(not allclose(a, b, tol) if hasattr(a, "__iter__") else fabs(a - b) > tol for a, b in zip(l1, l2)):
        return False
    return True


def argmax(values):
    """Returns the index of the first maximum value within an array.

    Parameters
    ----------
    values : sequence[float]
        A list of values.

    Returns
    -------
    int
        The index of the first maximum value within an array.

    Notes
    -----
    NumPy's *argmax* function [1]_ is different, it returns an array of indices.

    References
    ----------
    .. [1] https://numpy.org/doc/stable/reference/generated/numpy.argmax.html

    Examples
    --------
    >>> argmax([2, 4, 4, 3])
    1

    """
    return max(range(len(values)), key=lambda i: values[i])  # type: ignore


def argmin(values):
    """Returns the index of the first minimum value within an array.

    Parameters
    ----------
    values : sequence[float]
        A list of values.

    Returns
    -------
    int
        The index of the first minimum value within an array.

    Notes
    -----
    NumPy's *argmin* function [1]_ is different, it returns an array of indices.

    References
    ----------
    .. [1] https://numpy.org/doc/stable/reference/generated/numpy.argmin.html

    Examples
    --------
    >>> argmin([4, 2, 2, 3])
    1

    """
    return min(range(len(values)), key=lambda i: values[i])


# ==============================================================================
# these return something of smaller dimension/length/...
# something_(of)vector/s
# ==============================================================================


def sum_vectors(vectors, axis=0):
    """Calculate the sum of a series of vectors along the specified axis.

    Parameters
    ----------
    vectors : sequence[[float, float, float] | :class:`compas.geometry.Vector`]
        A list of vectors.
    axis : int, optional
        If ``axis == 0``, the sum is taken per column.
        If ``axis == 1``, the sum is taken per row.

    Returns
    -------
    list[float]
        The length of the list is ``len(vectors[0])``, if ``axis == 0``.
        The length is ``len(vectors)``, otherwise.

    Examples
    --------
    >>> vectors = [[1.0, 2.0, 3.0], [1.0, 2.0, 3.0], [1.0, 2.0, 3.0]]
    >>> sum_vectors(vectors)
    [3.0, 6.0, 9.0]
    >>> sum_vectors(vectors, axis=1)
    [6.0, 6.0, 6.0]

    """
    if axis == 0:
        vectors = zip(*vectors)
    return [sum(vector) for vector in vectors]


def norm_vector(vector):
    """Calculate the length of a vector.

    Parameters
    ----------
    vector : [float, float, float] | :class:`compas.geometry.Vector`
        XYZ components of the vector.

    Returns
    -------
    float
        The L2 norm, or *length* of the vector.

    Examples
    --------
    >>> norm_vector([2.0, 0.0, 0.0])
    2.0

    >>> norm_vector([1.0, 1.0, 0.0]) == sqrt(2.0)
    True

    """
    return sqrt(sum(axis**2 for axis in vector))


def norm_vectors(vectors):
    """
    Calculate the norm of each vector in a list of vectors.

    Parameters
    ----------
    vectors : sequence[[float, float, float] | :class:`compas.geometry.Vector`]
        A list of vectors

    Returns
    -------
    list[float]
        A list with the lengths of all vectors.

    Examples
    --------
    >>> norm_vectors([[1.0, 0.0, 0.0], [2.0, 0.0, 0.0], [3.0, 0.0, 0.0]])
    [1.0, 2.0, 3.0]

    """
    return [norm_vector(vector) for vector in vectors]


def length_vector(vector):
    """Calculate the length of the vector.

    Parameters
    ----------
    vector : [float, float, float] | :class:`compas.geometry.Vector`
        XYZ components of the vector.

    Returns
    -------
    float
        The length of the vector.

    Examples
    --------
    >>> length_vector([2.0, 0.0, 0.0])
    2.0

    >>> length_vector([1.0, 1.0, 0.0]) == sqrt(2.0)
    True

    """
    return sqrt(length_vector_sqrd(vector))


def length_vector_xy(vector):
    """Compute the length of a vector, assuming it lies in the XY plane.

    Parameters
    ----------
    vector : [float, float, float] | :class:`compas.geometry.Vector`
        XY(Z) components of the vector.

    Returns
    -------
    float
        The length of the XY component of the vector.

    Examples
    --------
    >>> length_vector_xy([2.0, 0.0])
    2.0

    >>> length_vector_xy([2.0, 0.0, 0.0])
    2.0

    >>> length_vector_xy([2.0, 0.0, 2.0])
    2.0

    """
    return sqrt(length_vector_sqrd_xy(vector))


def length_vector_sqrd(vector):
    """Compute the squared length of a vector.

    Parameters
    ----------
    vector : [float, float, float] | :class:`compas.geometry.Vector`
        XYZ components of the vector.

    Returns
    -------
    float
        The squared length.

    Examples
    --------
    >>> length_vector_sqrd([1.0, 1.0, 0.0])
    2.0

    """
    return vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2


def length_vector_sqrd_xy(vector):
    """Compute the squared length of a vector, assuming it lies in the XY plane.

    Parameters
    ----------
    vector : [float, float] or [float, float, float] | :class:`compas.geometry.Vector`
        XY(Z) components of the vector.

    Returns
    -------
    float
        The squared length.

    Examples
    --------
    >>> length_vector_sqrd_xy([1.0, 1.0])
    2.0

    >>> length_vector_sqrd_xy([1.0, 1.0, 0.0])
    2.0

    >>> length_vector_sqrd_xy([1.0, 1.0, 1.0])
    2.0

    """
    return vector[0] ** 2 + vector[1] ** 2


# ==============================================================================
# these perform an operation on a vector and return a modified vector
# -> elementwise operations on 1 vector
# should this not bet ...ed_vector
# ... or else modify the vector in-place
# ==============================================================================


def scale_vector(vector, factor):
    """Scale a vector by a given factor.

    Parameters
    ----------
    vector : [float, float, float] | :class:`compas.geometry.Vector`
        XYZ components of the vector.
    factor : float
        The scaling factor.

    Returns
    -------
    [float, float, float]
        The scaled vector.

    Examples
    --------
    >>> scale_vector([1.0, 2.0, 3.0], 2.0)
    [2.0, 4.0, 6.0]

    >>> v = [2.0, 0.0, 0.0]
    >>> scale_vector(v, 1 / length_vector(v))
    [1.0, 0.0, 0.0]

    """
    return [axis * factor for axis in vector]


def scale_vector_xy(vector, factor):
    """Scale a vector by a given factor, assuming it lies in the XY plane.

    Parameters
    ----------
    vector : [float, float] or [float, float, float] | :class:`compas.geometry.Vector`
        XY(Z) components of the vector.
    scale : float
        Scale factor.

    Returns
    -------
    [float, float, 0.0]
        The scaled vector in the XY-plane.

    Examples
    --------
    >>> scale_vector_xy([1.0, 2.0, 3.0], 2.0)
    [2.0, 4.0, 0.0]

    """
    return [vector[0] * factor, vector[1] * factor, 0.0]


def scale_vectors(vectors, factor):
    """Scale multiple vectors by a given factor.

    Parameters
    ----------
    vectors : sequence[[float, float, float] | :class:`compas.geometry.Vector`]
        A list of vectors.
    factor : float
        The scaling factor.

    Returns
    -------
    list[[float, float, float]]
        The scaled vectors.

    Examples
    --------
    >>>

    """
    return [scale_vector(vector, factor) for vector in vectors]


def scale_vectors_xy(vectors, factor):
    """Scale multiple vectors by a given factor, assuming they lie in the XY plane.

    Parameters
    ----------
    vectors : sequence[[float, float] or [float, float, float] | :class:`compas.geometry.Vector`]
        A list of vectors.
    factor : float
        The scaling factor.

    Returns
    -------
    list[[float, float, 0.0]]
        The scaled vectors in the XY plane.

    Examples
    --------
    >>>

    """
    return [scale_vector_xy(vector, factor) for vector in vectors]


def normalize_vector(vector):
    """Normalise a given vector.

    Parameters
    ----------
    vector : [float, float, float] | :class:`compas.geometry.Vector`
        XYZ components of the vector.

    Returns
    -------
    [float, float, float]
        The normalized vector.

    Examples
    --------
    >>>

    """
    length = length_vector(vector)
    if not length:
        return vector
    return [vector[0] / length, vector[1] / length, vector[2] / length]


def normalize_vector_xy(vector):
    """Normalize a vector, assuming it lies in the XY-plane.

    Parameters
    ----------
    vector : [float, float] or [float, float, float] | :class:`compas.geometry.Vector`
        XY(Z) components of the vector.

    Returns
    -------
    [float, float, 0.0]
        The normalized vector in the XY-plane.

    Examples
    --------
    >>>

    """
    length = length_vector_xy(vector)
    if not length:
        return vector
    return [vector[0] / length, vector[1] / length, 0.0]


def normalize_vectors(vectors):
    """Normalise multiple vectors.

    Parameters
    ----------
    vectors : sequence[[float, float, float] | :class:`compas.geometry.Vector`]
        A list of vectors.

    Returns
    -------
    list[[float, float, float]]
        The normalized vectors.

    Examples
    --------
    >>>

    """
    return [normalize_vector(vector) for vector in vectors]


def normalize_vectors_xy(vectors):
    """Normalise multiple vectors, assuming they lie in the XY plane.

    Parameters
    ----------
    vectors : sequence[[float, float] or [float, float, float] | :class:`compas.geometry.Vector`]
        A list of vectors.

    Returns
    -------
    list[[float, float, 0.0]]
        The normalized vectors in the XY plane.

    Examples
    --------
    >>>

    """
    return [normalize_vector_xy(vector) for vector in vectors]


def power_vector(vector, power):
    """Raise a vector to the given power.

    Parameters
    ----------
    vector : [float, float, float] | :class:`compas.geometry.Vector`
        XYZ components of the vector.
    power : int, float
        The power to which to raise the vector.

    Returns
    -------
    [float, float, float]
        The raised vector.

    Examples
    --------
    >>>

    """
    return [axis**power for axis in vector]


def power_vectors(vectors, power):
    """Raise a list of vectors to the given power.

    Parameters
    ----------
    vectors : sequence[[float, float, float] | :class:`compas.geometry.Vector`]
        A list of vectors.
    power : int, float
        The power to which to raise the vectors.

    Returns
    -------
    list[[float, float, float]]
        The raised vectors.

    Examples
    --------
    >>>

    """
    return [power_vector(vector, power) for vector in vectors]


def square_vector(vector):
    """Raise a vector to the power 2.

    Parameters
    ----------
    vector : [float, float, float] | :class:`compas.geometry.Vector`
        XYZ components of the vector.

    Returns
    -------
    [float, float, float]
        The squared vector.

    Examples
    --------
    >>>

    """
    return power_vector(vector, 2)


def square_vectors(vectors):
    """Raise a multiple vectors to the power 2.

    Parameters
    ----------
    vectors : sequence[[float, float, float] | :class:`compas.geometry.Vector`]
        A list of vectors.

    Returns
    -------
    [float, float, float]]
        The squared vectors.

    Examples
    --------
    >>>

    """
    return [square_vectors(vector) for vector in vectors]


# ==============================================================================
# these perform an operation with corresponding elements of the (2) input vectors as operands
# and return a vector with the results
# -> elementwise operations on two vectors
# ==============================================================================


def add_vectors(u, v):
    """Add two vectors.

    Parameters
    ----------
    u : [float, float, float] | :class:`compas.geometry.Vector`
        XYZ components of the first vector.
    v : [float, float, float] | :class:`compas.geometry.Vector`
        XYZ components of the second vector.

    Returns
    -------
    [float, float, float]
        The resulting vector.

    """
    return [a + b for (a, b) in zip(u, v)]


def add_vectors_xy(u, v):
    """Add two vectors, assuming they lie in the XY-plane.

    Parameters
    ----------
    u : [float, float] or [float, float, float] | :class:`compas.geometry.Vector`
        XY(Z) components of the first vector.
    v : [float, float] or [float, float, float] | :class:`compas.geometry.Vector`
        XY(Z) components of the second vector.

    Returns
    -------
    [float, float, 0.0]
        Resulting vector in the XY-plane.

    Examples
    --------
    >>>

    """
    return [u[0] + v[0], u[1] + v[1], 0.0]


def subtract_vectors(u, v):
    """Subtract one vector from another.

    Parameters
    ----------
    u : [float, float, float] | :class:`compas.geometry.Vector`
        XYZ components of the first vector.
    v : [float, float, float] | :class:`compas.geometry.Vector`
        XYZ components of the second vector.

    Returns
    -------
    [float, float, float]
        The resulting vector.

    Examples
    --------
    >>>

    """
    return [a - b for (a, b) in zip(u, v)]


def subtract_vectors_xy(u, v):
    """Subtract one vector from another, assuming they lie in the XY plane.

    Parameters
    ----------
    u : [float, float] or [float, float, float] | :class:`compas.geometry.Vector`
        The XY(Z) components of the first vector.
    v : [float, float] or [float, float, float] | :class:`compas.geometry.Vector`
        The XY(Z) components of the second vector.

    Returns
    -------
    [float, float, 0.0]
        Resulting vector in the XY-plane.

    Examples
    --------
    >>>

    """
    return [u[0] - v[0], u[1] - v[1], 0.0]


def multiply_vectors(u, v):
    """Element-wise multiplication of two vectors.

    Parameters
    ----------
    u : [float, float, float] | :class:`compas.geometry.Vector`
        The XYZ components of the first vector.
    v : l[float, float, float] | :class:`compas.geometry.Vector`
        The XYZ components of the second vector.

    Returns
    -------
    [float, float, float]
        Resulting vector.

    Examples
    --------
    >>>

    """
    return [a * b for (a, b) in zip(u, v)]


def multiply_vectors_xy(u, v):
    """Element-wise multiplication of two vectors assumed to lie in the XY plane.

    Parameters
    ----------
    u : [float, float] or [float, float, float] | :class:`compas.geometry.Vector`
        The XY(Z) components of the first vector.
    v : [float, float] or [float, float, float] | :class:`compas.geometry.Vector`
        The XY(Z) components of the second vector.

    Returns
    -------
    [float, float, 0.0]
        Resulting vector in the XY plane.

    Examples
    --------
    >>>

    """
    return [u[0] * v[0], u[1] * v[1], 0.0]


def divide_vectors(u, v):
    """Element-wise division of two vectors.

    Parameters
    ----------
    u : [float, float, float] | :class:`compas.geometry.Vector`
        The XYZ components of the first vector.
    v : [float, float, float] | :class:`compas.geometry.Vector`
        The XYZ components of the second vector.

    Returns
    -------
    [float, float, float]
        Resulting vector.

    Examples
    --------
    >>>

    """
    return [a / b for (a, b) in zip(u, v)]


def divide_vectors_xy(u, v):
    """Element-wise division of two vectors assumed to lie in the XY plane.

    Parameters
    ----------
    u : [float, float] or [float, float, float] | :class:`compas.geometry.Vector`
        The XY(Z) components of the first vector.
    v : [float, float] or [float, float, float] | :class:`compas.geometry.Vector`
        The XY(Z) components of the second vector.

    Returns
    -------
    [float, float, 0.0]
        Resulting vector in the XY plane.

    Examples
    --------
    >>>

    """
    return [u[0] / v[0], u[1] / v[1], 0.0]


# ==============================================================================
# ...
# ==============================================================================


def cross_vectors(u, v):
    r"""Compute the cross product of two vectors.

    Parameters
    ----------
    u : [float, float, float] | :class:`compas.geometry.Vector`
        XYZ components of the first vector.
    v : [float, float, float] | :class:`compas.geometry.Vector`
        XYZ components of the second vector.

    Returns
    -------
    [float, float, float]
        The cross product of the two vectors.

    Notes
    -----
    The xyz components of the cross product of two vectors :math:`\mathbf{u}`
    and :math:`\mathbf{v}` can be computed as the *minors* of the following matrix:

    .. math::
       :nowrap:

        \begin{bmatrix}
        x & y & z \\
        u_{x} & u_{y} & u_{z} \\
        v_{x} & v_{y} & v_{z}
        \end{bmatrix}

    Therefore, the cross product can be written as:

    .. math::
       :nowrap:

        \begin{eqnarray}
            \mathbf{u} \times \mathbf{v}
            & =
            \begin{bmatrix}
            u_{y} * v_{z} - u_{z} * v_{y} \\
            u_{z} * v_{x} - u_{x} * v_{z} \\
            u_{x} * v_{y} - u_{y} * v_{x}
            \end{bmatrix}
        \end{eqnarray}

    Examples
    --------
    >>> cross_vectors([1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
    [0.0, 0.0, 1.0]

    """
    return [
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    ]


def cross_vectors_xy(u, v):
    """Compute the cross product of two vectors, assuming they lie in the XY-plane.

    Parameters
    ----------
    u : [float, float] or [float, float, float] | :class:`compas.geometry.Vector`
        XY(Z) coordinates of the first vector.
    v : [float, float] or [float, float, float] | :class:`compas.geometry.Vector`
        XY(Z) coordinates of the second vector.

    Returns
    -------
    [float, float, float]
        The cross product of the two vectors.
        This vector will be perpendicular to the XY plane.

    Examples
    --------
    >>> cross_vectors_xy([1.0, 0.0], [0.0, 1.0])
    [0.0, 0.0, 1.0]

    >>> cross_vectors_xy([1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
    [0.0, 0.0, 1.0]

    >>> cross_vectors_xy([1.0, 0.0, 1.0], [0.0, 1.0, 1.0])
    [0.0, 0.0, 1.0]

    """
    return [0.0, 0.0, u[0] * v[1] - u[1] * v[0]]


def dot_vectors(u, v):
    """Compute the dot product of two vectors.

    Parameters
    ----------
    u : [float, float, float] | :class:`compas.geometry.Vector`
        XYZ components of the first vector.
    v : [float, float, float] | :class:`compas.geometry.Vector`
        XYZ components of the second vector.

    Returns
    -------
    float
        The dot product of the two vectors.

    Examples
    --------
    >>> dot_vectors([1.0, 0, 0], [2.0, 0, 0])
    2.0

    """
    return sum(a * b for a, b in zip(u, v))


def dot_vectors_xy(u, v):
    """Compute the dot product of two vectors, assuming they lie in the XY-plane.

    Parameters
    ----------
    u : [float, float] or [float, float, float] | :class:`compas.geometry.Vector`
        XY(Z) coordinates of the first vector.
    v : [float, float] or [float, float, float] | :class:`compas.geometry.Vector`
        XY(Z) coordinates of the second vector.

    Returns
    -------
    float
        The dot product of the XY components of the two vectors.

    Examples
    --------
    >>> dot_vectors_xy([1.0, 0], [2.0, 0])
    2.0

    >>> dot_vectors_xy([1.0, 0, 0], [2.0, 0, 0])
    2.0

    >>> dot_vectors_xy([1.0, 0, 1], [2.0, 0, 1])
    2.0

    """
    return u[0] * v[0] + u[1] * v[1]


def vector_component(u, v):
    """Compute the component of u in the direction of v.

    Parameters
    ----------
    u : [float, float, float] | :class:`compas.geometry.Vector`
        XYZ components of the vector.
    v : [float, float, float] | :class:`compas.geometry.Vector`
        XYZ components of the direction.

    Returns
    -------
    [float, float, float]
        The component of u in the direction of v.

    Notes
    -----
    This is similar to computing direction cosines, or to the projection of
    a vector onto another vector. See the respective Wikipedia pages ([1]_, [2]_)
    for more info.

    References
    ----------
    .. [1] *Direction cosine*. Available at https://en.wikipedia.org/wiki/Direction_cosine.
    .. [2] *Vector projection*. Available at https://en.wikipedia.org/wiki/Vector_projection.

    Examples
    --------
    >>> vector_component([1.0, 2.0, 3.0], [1.0, 0.0, 0.0])
    [1.0, 0.0, 0.0]

    """
    l2 = length_vector_sqrd(v)
    if not l2:
        return [0, 0, 0]
    x = dot_vectors(u, v) / l2
    return scale_vector(v, x)


def vector_component_xy(u, v):
    """Compute the component of u in the direction of v, assuming they lie in the XY-plane.

    Parameters
    ----------
    u : [float, float] or [float, float, float] | :class:`compas.geometry.Vector`
        XYZ components of the vector.
    v : [float, float] or [float, float, float] | :class:`compas.geometry.Vector`
        XYZ components of the direction.

    Returns
    -------
    [float, float, 0.0]
        The component of u in the XY plane, in the direction of v.

    Notes
    -----
    This is similar to computing direction cosines, or to the projection of
    a vector onto another vector. See the respective Wikipedia pages ([1]_, [2]_)
    for more info.

    References
    ----------
    .. [1] *Direction cosine*. Available at https://en.wikipedia.org/wiki/Direction_cosine.
    .. [2] *Vector projection*. Available at https://en.wikipedia.org/wiki/Vector_projection.

    Examples
    --------
    >>> vector_component_xy([1, 2, 0], [1, 0, 0])
    [1.0, 0.0, 0.0]

    """
    l2 = length_vector_sqrd_xy(v)
    if not l2:
        return [0, 0, 0]
    x = dot_vectors_xy(u, v) / l2
    return scale_vector_xy(v, x)


# ==============================================================================
# these involve vectors interpreted as matrices (lists of lists)
# -> matrix multiplication
# ==============================================================================


def transpose_matrix(M):
    """Transpose a matrix.

    Parameters
    ----------
    M : list[list[float]] | :class:`compas.geometry.Transformation`
        The matrix to be transposed.

    Returns
    -------
    list[list[float]]
        The result matrix.

    """
    return list(map(list, zip(*list(M))))


def multiply_matrices(A, B):
    r"""Mutliply a matrix with a matrix.

    Parameters
    ----------
    A : list[list[float]] | :class:`compas.geometry.Transformation`
        The first matrix.
    B : list[list[float]] | :class:`compas.geometry.Transformation`
        The second matrix.

    Returns
    -------
    list[list[float]]
        The result matrix.

    Raises
    ------
    Exception
        If the shapes of the matrices are not compatible.
        If the row length of B is inconsistent.

    Notes
    -----
    This is a pure Python version of the following linear algebra procedure:

    .. math::

        \mathbf{A} \cdot \mathbf{B} = \mathbf{C}

    with :math:`\mathbf{A}` [m x n], :math:`\mathbf{B}` [n x o], and :math:`\mathbf{C}` [m x o].

    Examples
    --------
    >>> A = [[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]
    >>> B = [[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]
    >>> multiply_matrices(A, B)
    [[4.0, 0.0, 0.0], [0.0, 4.0, 0.0], [0.0, 0.0, 4.0]]

    """
    A = list(A)
    B = list(B)
    n = len(B)  # number of rows in B
    o = len(B[0])  # number of cols in B
    if not all(len(row) == o for row in B):
        raise Exception("Row length in matrix B is inconsistent.")
    if not all([len(row) == n for row in A]):
        raise Exception("Matrix shapes are not compatible.")
    B = list(zip(*list(B)))
    return [[dot_vectors(row, col) for col in B] for row in A]


def multiply_matrix_vector(A, b):
    r"""Multiply a matrix with a vector.

    Parameters
    ----------
    A : list[list[float]] | :class:`compas.geometry.Transformation`
        The matrix.
    b : [float, float, float] | :class:`compas.geometry.Vector`
        The vector.

    Returns
    -------
    [float, float, float]
        The resulting vector.

    Raises
    ------
    Exception
        If not all rows of the matrix have the same length as the vector.

    Notes
    -----
    This is a Python version of the following linear algebra procedure:

    .. math::

        \mathbf{A} \cdot \mathbf{x} = \mathbf{b}

    with :math:`\mathbf{A}` a *m* by *n* matrix, :math:`\mathbf{x}` a vector of
    length *n*, and :math:`\mathbf{b}` a vector of length *m*.

    Examples
    --------
    >>> matrix = [[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]
    >>> vector = [1.0, 2.0, 3.0]
    >>> multiply_matrix_vector(matrix, vector)
    [2.0, 4.0, 6.0]

    """
    n = len(b)
    if not all([len(row) == n for row in A]):
        raise Exception("Matrix shape is not compatible with vector length.")
    return [dot_vectors(row, b) for row in A]


# ==============================================================================
# linalg
# ==============================================================================


def homogenize_vectors(vectors, w=1.0):
    """Homogenise a list of vectors.

    Parameters
    ----------
    vectors : sequence[[float, float, float] | :class:`compas.geometry.Vector`]
        A list of vectors.
    w : float, optional
        Homogenisation parameter.

    Returns
    -------
    list[[float, float, float]]
        Homogenised vectors.

    Notes
    -----
    Vectors described by XYZ components are homogenised by appending a homogenisation
    parameter to the components, and by dividing each component by that parameter.
    Homogenisatioon of vectors is often used in relation to transformations.

    Examples
    --------
    >>> vectors = [[1.0, 0.0, 0.0]]
    >>> homogenize_vectors(vectors)
    [[1.0, 0.0, 0.0, 1.0]]

    """
    return [[x / w, y / w, z / w, w] for x, y, z in vectors]


def dehomogenize_vectors(vectors):
    """Dehomogenise a list of vectors.

    Parameters
    ----------
    vectors : sequence[[float, float, float] | :class:`compas.geometry.Vector`]
        A list of vectors.

    Returns
    -------
    list[float, float, float]
        Dehomogenised vectors.

    Examples
    --------
    >>>

    """
    return [[x * w, y * w, z * w] for x, y, z, w in vectors]


def orthonormalize_vectors(vectors):
    """Orthonormalize a set of vectors.

    Parameters
    ----------
    vectors : sequence[[float, float, float] | :class:`compas.geometry.Vector`]
        The set of vectors to othonormalize.

    Returns
    -------
    list[[float, float, float]]
        An othonormal basis for the input vectors.

    Notes
    -----
    This creates a basis for the range (column space) of the matrix A.T,
    with A = vectors.

    Orthonormalisation is according to the Gram-Schmidt process.

    Examples
    --------
    >>> orthonormalize_vectors([[1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]

    """
    basis = []
    for v in vectors:
        if basis:
            e = subtract_vectors(v, sum_vectors([vector_component(v, b) for b in basis]))
        else:
            e = v
        if any(axis > 1e-10 for axis in e):
            basis.append(normalize_vector(e))
    return basis
