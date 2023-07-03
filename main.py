import json
import numpy as np
import random
import math
import re
from dataclasses import dataclass
from argparse import ArgumentParser, Namespace as Arguments
from PIL import ImageFont, ImageDraw, Image
from sympy.abc import t
from sympy.polys.polyfuncs import interpolate

DEFAULT_FONT = "courier.ttf"
ALPHABET = "abcdefghijklmnopqrstuvwxyz"
BASE64 = ALPHABET + ALPHABET.upper() + "".join([str(n) for n in range(10)]) + "+/"

Character = str 

@dataclass
class Point: x: float; y: float

def generate_character_mappings(k: int, text: str, addr: str) -> dict[Character, np.ndarray]:
    mappings = {}
    unique_chars = set(text)
    font = ImageFont.truetype(addr, int(k))
    for char in unique_chars:
        temp_image = Image.new('RGB', (k, k))
        draw = ImageDraw.Draw(temp_image)
        draw.text((0, 0), char, font=font, color=0)
        mappings[char] = np.array(temp_image.convert('1'))
    return mappings

def generate_points(mappings: dict[Character, np.ndarray], k: int, text: str, n: int) -> list[list[Point]]:
    """
    Generates the paths that the points must take
    """
    total_points = []
    for char in text:
        points = []
        char_map = mappings[char]
        while len(points) < n:
            x, y = [k*random.random() for _ in range(2)]
            if char_map[math.floor(y)][math.floor(x)]:
                points.append(Point(x, -y))
        total_points.append(points)
    return total_points

def interpolate_poly(points: list[list[Point]], n: int) -> None:
    """
    Determines the polynomial interpolation for n points that pass through their predetermined paths
    """
    polys = []
    for point_id in range(n):
        interpolation_data = [points[i][point_id] for i in range(len(points))]
        get_poly = lambda v: str(interpolate([*map(lambda p: eval(f"p.{v}"), interpolation_data)], t)).replace("**", "^")
        polys.append((get_poly('x'), get_poly('y')))
    with open('points.txt', 'w') as f:
        f.write(f"t = 1\n") 
        for x_poly, y_poly in polys:
            f.write(f"({x_poly}, {y_poly})\n")

def interpolate_linear(points: list[list[Point]], n: int) -> None:
    """
    Connects points linearly rather than using a polynomial
    """
    point_strings = []
    for point_id in range(n):
        connecting_points = [points[i][point_id] for i in range(len(points))]
        x_conditions, y_conditions = [], []
        for (i, (p1, p2)) in enumerate(zip(connecting_points, connecting_points[1:]), start=1):
            base = rf"{i} \le t < {i+1}"
            x_conditions.append(f"{base}:{p1.x}+{p2.x-p1.x}*(t-{i})")
            y_conditions.append(f"{base}:{p1.y}+{p2.y-p1.y}*(t-{i})")
        point_strings.append(fr"(\left\{{{','.join(x_conditions)}\right\}}, \left\{{{','.join(y_conditions)}\right\}})")
    with open('points.txt', 'w') as f:
        f.write('t = 1\n')
        for point in point_strings:
            f.write(f"{point}\n")

def get_args() -> Arguments:
    """ 
    Returns the arguments to customize generation. 
      - side_length: The side length
      - text: The text to be displayed
      - point_count: The number of points being displayed
      - font_family: The font that is used
      - polynomial: Determines if polynomial interpolation will be used
    """
    parser = ArgumentParser()
    parser.add_argument("side_length", help="The side length of the square which text is rendered in", type=int)
    parser.add_argument("text", help="The text that will be rendered by the program")
    parser.add_argument("point_count", help="The number of points that will be rendered", type=int)
    parser.add_argument("--font_family", help="The path to the font file that will be used to render your text")
    parser.add_argument("--polynomial", help="Determines if polynomial behaviour is used", action="store_true")
    return parser.parse_args()

def main():
    args = get_args()

    # unpacks arguments
    k = args.side_length
    n = args.point_count
    text = re.sub(r'\s', '', args.text)
    font_family = args.font_family
    if font_family is None:
        font_family = DEFAULT_FONT
    
    mappings = generate_character_mappings(k, text, font_family)
    points = generate_points(mappings, k, text, n)
    if args.polynomial:
        interpolate_poly(points, n)
    else:
        interpolate_linear(points, n)

if __name__ == "__main__":
    main()