==========
Pluggables
==========

.. rst-class:: lead

COMPAS has an extensible architecture based on pluggables and plugins that allows to
customize and extend the functionality of the core framework.

Categories
==========

The following *extension points* are currently defined.

``booleans``
------------

.. currentmodule:: compas.geometry

* :func:`boolean_union_mesh_mesh`
* :func:`boolean_difference_mesh_mesh`
* :func:`boolean_intersection_mesh_mesh`

``install``
-----------

.. currentmodule:: compas_rhino.uninstall

* :func:`installable_rhino_packages`
* :func:`after_rhino_install`
* :func:`after_rhino_uninstall`


``intersections``
-----------------

.. currentmodule:: compas.geometry

* :func:`intersection_mesh_mesh`
* :func:`intersection_ray_mesh`


``quadmesh``
------------

.. currentmodule:: compas.geometry

* :func:`quadmesh_planarize`


``triangulation``
-----------------

.. currentmodule:: compas.geometry

* :func:`delaunay_triangulation`
* :func:`constrained_delaunay_triangulation`
* :func:`conforming_delaunay_triangulation`


``trimesh``
-----------

.. currentmodule:: compas.geometry

* :func:`trimesh_gaussian_curvature`
* :func:`trimesh_principal_curvature`
* :func:`trimesh_geodistance`
* :func:`trimesh_isolines`
* :func:`trimesh_massmatrix`
* :func:`trimesh_harmonic`
* :func:`trimesh_lscm`
* :func:`trimesh_remesh`
* :func:`trimesh_remesh_constrained`
* :func:`trimesh_slice`
