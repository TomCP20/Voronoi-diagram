"""A python program that generates Voronoi diagrams"""

from collections.abc import Callable
from colorsys import hsv_to_rgb
from functools import partial
from itertools import product
from math import atan2, pi
from random import random, randrange

from PIL import Image, ImageDraw

RES = 512
POINT_COUNT = 32
DOT_SIZE = 2
METRIC_SPACE = 0
"""0 = Euclidean, 1 = Manhattan"""

type Point = tuple[float, float]
"""A point in 2d space (X, Y) where 0 <= X, Y <= 1"""
type Pixel = tuple[int, int]
"""A point in 2d space (X, Y) where 0 <= X, Y <= 1"""
type Col = tuple[int, int, int]
"""A colour (R, G, B) where 0 <= R, G, B <= 255"""
type Mapping = Callable[[Point], Col]
"""A function that maps (X, Y) -> (R, G, B) """
type Grid = list[list[int]]
"""A grid of idexes for the closest point"""


def normalize(pixel: Pixel) -> Point:
    """Normalizes a pixel into a point"""
    return (pixel[0] / RES, pixel[1] / RES)


def denormalize(point: Point) -> Pixel:
    """Denormalizes a point into a pixel"""
    return (int(point[0] * RES), int(point[1] * RES))


def dist_sqr(p1: Point, p2: Point) -> float:
    """Returns the distance squared between p1 and p2"""
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


def man_dist(p1: Point, p2: Point) -> float:
    """Returns the manhattan distance between p1 and p2"""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def scale(c: tuple[float, float, float]) -> Col:
    """scale from float 0-1 to int 0-255"""
    return (int(c[0] * 255), int(c[1] * 255), int(c[2] * 255))


def xy_to_rg(p: Point) -> Col:
    """returns the color, (x, y, 0)"""
    return scale((p[0], p[1], 0))


def random_col(_: Point) -> Col:
    """returns a random color"""
    return (randrange(256), randrange(256), randrange(256))


def xy_to_hsv(p: Point) -> Col:
    """returs the color with hue x and lightness y"""
    return scale(hsv_to_rgb(p[0], 1, p[1]))


def polar_to_hsv(p: Point) -> Col:
    """returs the color with hue r and lightness angle"""
    r = ((p[0] - 0.5) ** 2 + (p[1] - 0.5) ** 2) ** 0.5
    angle = (atan2(p[1] - 0.5, p[0] - 0.5) % (2 * pi)) / (2 * pi)
    return scale(hsv_to_rgb(angle, 1, r))


def cpi(points: list[Point], p: Point) -> int:
    """returns the index of the point in points closest to p"""
    return points.index(min(points, key=partial([dist_sqr, man_dist][METRIC_SPACE], p)))


def gen_image(points: list[Point], grid: Grid, mapping: Mapping) -> Image.Image:
    """Generates an image of The Voronoi diagram using the given color mapping"""
    cols: dict[int, Col] = {points.index(p): mapping(p) for p in points}
    image = Image.new(mode="RGB", size=(RES, RES))
    for x, y in product(range(RES), repeat=2):
        image.putpixel((x, y), cols[grid[y][x]])
    if DOT_SIZE:
        draw = ImageDraw.Draw(image)
        for point in points:
            draw.circle(denormalize(point), DOT_SIZE, fill=(0, 0, 0))
    return image


def main():
    """The main function"""
    mappings: list[Mapping] = [random_col, xy_to_rg, xy_to_hsv, polar_to_hsv]

    points = [(random(), random()) for _ in range(POINT_COUNT)]
    grid = [[cpi(points, normalize((x, y))) for x in range(RES)] for y in range(RES)]
    for mapping in mappings:
        gen_image(points, grid, mapping).show()


if __name__ == "__main__":
    main()
