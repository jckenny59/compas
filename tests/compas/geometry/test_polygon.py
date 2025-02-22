import pytest
import json
import compas
from random import random
from compas.geometry import Point
from compas.geometry import Polygon
from compas.utilities import pairwise


@pytest.mark.parametrize(
    "points",
    [
        [[0, 0, 0], [1, 0, 0]],
        [[0, 0, 0], [1, 0, 0], [1, 1, 0]],
        [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]],
        [[0, 0, x] for x in range(5)],
        [[random(), random(), random()] for i in range(10)],
    ],
)
def test_polygon(points):
    polygon = Polygon(points)
    assert polygon.points == points
    assert polygon.lines == [(a, b) for a, b in pairwise(points + points[:1])]
    assert polygon.points[-1] != polygon.points[0]
    assert polygon.lines[0][0] == polygon.points[0]
    assert polygon.lines[-1][1] == polygon.points[0]
    assert polygon.lines[-1][0] == polygon.points[-1]

    if not compas.IPY:
        assert polygon == eval(repr(polygon))


def test_polygon_constructor_does_not_modify_input_params():
    pts = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 0]]

    polygon = Polygon(pts)
    assert len(pts) == 5
    assert len(polygon.points) == 4, "The last point (matching the first) should have been removed"


def test_polygon_data():
    points = [[random(), random(), random()] for i in range(10)]
    polygon = Polygon(points)
    other = Polygon.from_data(json.loads(json.dumps(polygon.to_data())))

    assert polygon == other
    assert polygon.points == other.points
    assert polygon.data == other.data

    if not compas.IPY:
        assert Polygon.validate_data(polygon.data)
        assert Polygon.validate_data(other.data)


def test_polygon__eq__():
    points1 = [[0, 0, x] for x in range(5)]
    polygon1 = Polygon(points1)
    points2 = [[0, 0, x] for x in range(6)]
    polygon2 = Polygon(points2)
    points3 = [[0, 0, x] for x in range(5)] + [[0, 0, 0]]
    polygon3 = Polygon(points3)
    assert polygon1 == polygon1
    assert polygon1 == points1
    assert points1 == polygon1
    assert polygon1 != polygon2
    assert polygon2 != polygon1
    assert polygon1 != points2
    assert points2 != polygon1
    assert polygon1 != 1
    assert polygon1 == polygon3


def test_polygon__getitem__():
    points = [[0, 0, x] for x in range(5)]
    polygon = Polygon(points)
    for x in range(5):
        assert polygon[x] == [0, 0, x]
    with pytest.raises(IndexError):
        polygon[6] = [0, 0, 6]


def test_polygon__setitem__():
    points = [[0, 0, x] for x in range(5)]
    polygon = Polygon(points)
    point = [1, 1, 4]
    polygon[4] = point
    assert polygon[4] == point
    assert isinstance(polygon[4], Point)
    assert polygon.lines[-2].end == point
