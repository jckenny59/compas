************************
Boundary Representations
************************

.. rst-class:: lead

Boundary representation (Brep) support is realized in COMPAS using its `plugin` system.
The expected interface for Brep related classes is defined in the :mod:`compas.geometry.brep` module
whereas the actual implementation is context dependent and implemented using plugins.

.. currentmodule:: compas.geometry

.. highlight:: python

Brep Basics
===========

Brep is a data structure used to describe a shape by means of recording topological and geometrical information of the shape's boundaries.
Some topological properties are associated with an underlying geometry, while others are purely topological.

A Brep is comprised of the following:

.. rst-class:: table table-bordered

.. list-table::
    :widths: auto
    :header-rows: 1

    * - Topology
      - Geometry
      - Description
    * - Vertex
      - 3D Point
      - The most basic element of a Brep, geometrically described as a point in 3D space.
    * - Edge
      - 3D Curve
      - An edge has a start vertex and an end vertex. The underlying 3D curve describes the geometry of the edge (Line, Circle etc.). Closed edges feature start_vertex == end_vertex.
    * - Loop
      - None
      - A collection of trims which define the inner or outer boundary of a face.
    * - Face
      - Surface
      - Defines the geometry of one of the shape's faces using a surface. Associated with at least one loop which describes the trimmed outer boundary of the surface. Inner loops are referred to as holes in the face.
    * - Trim
      - 2D Curve
      - A 2D curve which trims a face. Trims are associated with a corresponding edge.


Getting Started with COMPAS Brep
================================

To create an empty `Brep`

.. code-block::

    >>> from compas.geometry import Brep
    >>> brep = Brep()


Notice that the type of the actual instance created by `Brep()` will differ depending on the currently available backend.
For example, when in Rhino

.. code-block::

    >>> type(brep)
    compas_rhino.geometry.RhinoBrep

Every backend is expected to implement some alternative constructors

.. code-block::

    >>> from compas.geometry import Box
    >>> from compas.geometry import Brep
    >>> ...
    >>> box = Box.from_width_height_depth(5., 5., 5.)
    >>> brep_box = Brep.from_box(box)


`Brep` can also be instantiated from an instance of a backend native `Brep`

.. code-block::

    >>> import Rhino
    >>> from compas.geometry import Brep
    >>> ...
    >>> Brep.from_native(Rhino.Geometry.Brep())

Brep operations
===============

Trimming a Brep in Grasshopper

.. code-block::

    from compas.geometry import Frame
    from compas.geometry import Point
    from compas.geometry import Brep

    box = Box.from_width_height_depth(5, 5, 10)

    brep = Brep.from_box(box)
    cutting_plane = Frame(Point(0, 2.5, 0), [1, 0, 0], [0, 1, 1.5])

    brep.trim(cutting_plane)

|pic1| |pic2|

.. |pic1| image:: files/box_w_plane.png
   :width: 48%

.. |pic2| image:: files/trimmed_box.png
   :width: 48%

Splitting a Brep in Grasshopper

.. code-block::

    from compas.geometry import Brep, Box, Frame, Translation

    brep = Brep.from_box(Box.from_width_height_depth(5,5,5))
    cutter = Brep.from_box(Box.from_width_height_depth(1, 6, 6))

    a, b, c = brep.split(cutter)

    world_xy = Frame.worldXY()
    translated_frame = Frame((0, 0, 1.), world_xy.xaxis, world_xy.yaxis)
    t = Translation.from_frame_to_frame(world_xy, translated_frame)
    a.transform(t)
    b.transform(t)

    result = [x.native_brep for x in [a, b, c]]

.. image:: files/3_way_split.png
    :width: 50%
