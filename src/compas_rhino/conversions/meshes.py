from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest  # type: ignore

from System.Drawing import Color as SystemColor  # type: ignore
from System.Array import CreateInstance  # type: ignore
from Rhino.Geometry import Mesh as RhinoMesh  # type: ignore

try:
    # MeshNgon is not available in older versions of Rhino
    from Rhino.Geometry import MeshNgon  # type: ignore
except ImportError:
    MeshNgon = None

from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import centroid_polygon
from compas.utilities import pairwise
from .geometry import vector_to_compas


def average_color(colors):
    c = len(colors)
    r, g, b = zip(*colors)
    r = sum(r) / c
    g = sum(g) / c
    b = sum(b) / c
    return int(r), int(g), int(b)


def connected_ngon(face, vertices, rmesh):
    points = [vertices[index] for index in face]
    centroid = centroid_polygon(points)

    c = rmesh.Vertices.Add(*centroid)

    facets = []
    for i, j in pairwise(face + face[:1]):
        facets.append(rmesh.Faces.AddFace(i, j, c))

    ngon = MeshNgon.Create(face, facets)  # type: ignore
    rmesh.Ngons.AddNgon(ngon)


def disjoint_ngon(face, vertices, rmesh):
    points = [vertices[vertex] for vertex in face]
    centroid = centroid_polygon(points)

    indices = []
    for point in points:
        x, y, z = point
        indices.append(rmesh.Vertices.Add(x, y, z))

    c = rmesh.Vertices.Add(*centroid)

    facets = []
    for i, j in pairwise(indices + indices[:1]):
        facets.append(rmesh.Faces.AddFace(i, j, c))

    ngon = MeshNgon.Create(indices, facets)  # type: ignore
    rmesh.Ngons.AddNgon(ngon)


def disjoint_face(face, vertices, rmesh):
    indices = []
    for index in face:
        x, y, z = vertices[index]
        indices.append(rmesh.Vertices.Add(x, y, z))
    rmesh.Faces.AddFace(*indices)


# =============================================================================
# To Rhino
# =============================================================================


def mesh_to_rhino(
    mesh,
    color=None,
    vertexcolors=None,
    facecolors=None,
    disjoint=True,
    face_callback=None,
):
    """Convert a COMPAS Mesh or a Polyhedron to a Rhino mesh object.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh` | :class:`compas.geometry.Polyhedron`
        A COMPAS Mesh or a Polyhedron.
    disjoint : bool, optional
        If ``True``, each face of the resulting mesh will be independently defined (have a copy of its own vertices).
    face_callback : callable, optional
        Called after each face is created with the face as an agrument, useful for custom post-processing.

    Returns
    -------
    :class:`Rhino.Geometry.Mesh`
        A Rhino mesh object.

    """
    vertices, faces = mesh.to_vertices_and_faces()
    return vertices_and_faces_to_rhino(
        vertices,
        faces,
        color=color,
        vertexcolors=vertexcolors,
        facecolors=facecolors,
        disjoint=disjoint,
        face_callback=face_callback,
    )


polyhedron_to_rhino = mesh_to_rhino


def vertices_and_faces_to_rhino(
    vertices,
    faces,
    color=None,
    vertexcolors=None,
    facecolors=None,
    disjoint=True,
    face_callback=None,
):
    """Convert COMPAS vertices and faces to a Rhino mesh object.

    Parameters
    ----------
    vertices : list[[float, float, float] | :class:`compas.geometry.Point`]
        A list of point locations.
    faces : list[list[int]]
        A list of faces as lists of indices into `vertices`.
    disjoint : bool, optional
        If ``True``, each face of the resulting mesh will be independently defined (have a copy of its own vertices).
    face_callback : callable, optional
        Called after each face is created with the face as an agrument, useful for custom post-processing.

    Returns
    -------
    :class:`Rhino.Geometry.Mesh`
        A Rhino mesh object.

    """
    if disjoint and facecolors:
        if len(faces) != len(facecolors):
            raise ValueError("The number of face colors does not match the number of faces.")

    if not disjoint and vertexcolors:
        if len(vertices) != len(vertexcolors):
            raise ValueError("The number of vertex colors does not match the number of vertices.")

    face_callback = face_callback or (lambda _: None)
    mesh = RhinoMesh()

    if disjoint:
        vertexcolors = []

        for face, facecolor in zip_longest(faces, facecolors or []):
            f = len(face)

            if f < 3:
                continue

            if f > 4:
                if MeshNgon is None:
                    raise NotImplementedError("MeshNgons are not supported in this version of Rhino.")

                disjoint_ngon(face, vertices, mesh)
                if facecolor:
                    for _ in range(f + 1):
                        vertexcolors.append(facecolor)

            else:
                disjoint_face(face, vertices, mesh)
                if facecolor:
                    for _ in range(f):
                        vertexcolors.append(facecolor)

            face_callback(face)

    else:
        for x, y, z in vertices:
            mesh.Vertices.Add(x, y, z)

        for face in faces:
            f = len(face)

            if f < 3:
                continue

            if f > 4:
                if MeshNgon is None:
                    raise NotImplementedError("MeshNgons are not supported in this version of Rhino.")

                connected_ngon(face, vertices, mesh)
                if vertexcolors:
                    vertexcolors.append(average_color([vertexcolors[index] for index in face]))

            else:
                mesh.Faces.AddFace(*face)

            face_callback(face)

    # if color:
    #     mesh.VertexColors.CreateMonotoneMesh(SystemColor.FromArgb(*color.rgb255))

    # else:
    if not color:
        if vertexcolors:
            if len(mesh.Vertices) != len(vertexcolors):
                raise ValueError("The number of vertex colors does not match the number of vertices.")

            colors = CreateInstance(SystemColor, len(vertexcolors))
            for index, color in enumerate(vertexcolors):
                colors[index] = SystemColor.FromArgb(*color.rgb255)

            mesh.VertexColors.SetColors(colors)

    # mesh.UnifyNormals()
    mesh.Normals.ComputeNormals()
    mesh.Compact()

    return mesh


# =============================================================================
# To COMPAS
# =============================================================================


def mesh_to_compas(rhinomesh, cls=None):
    """Convert a Rhino mesh object to a COMPAS mesh.

    Parameters
    ----------
    rhinomesh : :class:`Rhino.Geometry.Mesh`
        A Rhino mesh object.
    cls: :class:`compas.datastructures.Mesh`, optional
        The mesh type.

    Returns
    -------
    :class:`compas.datastructures.Mesh`
        A COMPAS mesh.

    """
    cls = cls or Mesh
    mesh = cls()
    mesh.default_vertex_attributes.update(normal=None, color=None)
    mesh.default_face_attributes.update(normal=None)

    vertexcolors = rhinomesh.VertexColors
    if not vertexcolors:
        vertexcolors = [None] * rhinomesh.Vertices.Count

    for vertex, normal, color in zip(rhinomesh.Vertices, rhinomesh.Normals, vertexcolors):
        mesh.add_vertex(
            x=vertex.X,
            y=vertex.Y,
            z=vertex.Z,
            normal=vector_to_compas(normal),
            color=Color(color.R, color.G, color.B) if color else None,
        )

    facenormals = rhinomesh.FaceNormals
    if not facenormals:
        facenormals = [None] * rhinomesh.Faces.Count

    for face, normal in zip(rhinomesh.Faces, facenormals):
        if face.IsTriangle:
            vertices = [face.A, face.B, face.C]
        else:
            vertices = [face.A, face.B, face.C, face.D]
        mesh.add_face(vertices, normal=vector_to_compas(normal) if normal else None)

    for key in rhinomesh.UserDictionary:
        mesh.attributes[key] = rhinomesh.UserDictionary[key]

    return mesh
