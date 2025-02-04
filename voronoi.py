"""A python program that generates Voronoi diagrams"""
from colorsys import hsv_to_rgb
from math import atan2, pi
from random import random, randrange
from collections.abc import Callable
from itertools import product
from PIL import Image, ImageDraw

type Point = tuple[float, float]
type Col = tuple[int, int, int]

def scale(c: tuple[float, float, float]) -> Col:
    """scale from float 0-1 to int 0-255"""
    return (int(c[0]*255), int(c[1]*255), int(c[2]*255))

def xy_to_rg(p: Point) -> Col:
    """returns the color, (x, y, 0)"""
    return scale((p[0], p[1], 0))

def random_col(_: Point) -> Col:
    """returns a random color"""
    return (randrange(256), randrange(256), randrange(256))

def xy_to_hsv(p: Point) -> Col:
    """returs the color with hue x and lightness y"""
    return scale(hsv_to_rgb(p[0], 1, p[1]))

def r_angle_to_hsv(p: Point) -> Col:
    """returs the color with hue r and lightness angle"""
    r = ((p[0] - 0.5)**2 + (p[1] - 0.5)**2)**0.5
    angle = (atan2(p[1]-0.5, p[0]-0.5) % (2*pi))/(2*pi)
    return scale(hsv_to_rgb(angle, 1, r))

def gen_voronoi(res: int, n: int, col_func: Callable[[Point], Col], radius: int) -> Image.Image:
    """Generates a Voronoi diagrams"""
    points: set[Point] = {(random(), random()) for _ in range(n)}
    cols: dict[Point, Col] = {p: col_func(p) for p in points}
    image = Image.new(mode="RGB", size=(res, res))
    for (x, y) in product(range(res), range(res)):
        def dist_key(p1: Point) -> Callable[[Point], float]:
            return lambda p2 : (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2
        image.putpixel((x, y), cols[min(points, key=dist_key((x/res, y/res)))])

    if radius:
        draw = ImageDraw.Draw(image)
        for point in points:
            draw.circle((int(point[0]*res), int(point[1]*res)), radius, fill=(0, 0, 0))

    return image

gen_voronoi(512, 32, random_col, 4).show()
