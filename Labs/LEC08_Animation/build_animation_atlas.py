"""Rebuild the transparent atlas from Pixel-Sprite-Sheet2.png (requires Pillow).

The viewer itself only needs pico2d and the generated PNG/JSON files.
"""
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "Pixel-Sprite-Sheet2.png"


def foreground_components(image):
    """Separate sprites and detached sword parts from the gray background."""
    pixels = image.load()
    background = pixels[0, 0]
    remaining = {
        (x, y)
        for y in range(image.height)
        for x in range(230, image.width)  # exclude the row labels
        if max(abs(pixels[x, y][c] - background[c]) for c in range(3)) > 30
    }
    components = []
    while remaining:
        start = remaining.pop()
        queue = deque([start])
        points = []
        while queue:
            x, y = queue.popleft()
            points.append((x, y))
            for neighbor in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if neighbor in remaining:
                    remaining.remove(neighbor)
                    queue.append(neighbor)
        if len(points) >= 3:
            xs, ys = zip(*points)
            bounds = (min(xs), min(ys), max(xs) + 1, max(ys) + 1)
            components.append((bounds, points))
    return sorted(components, key=lambda part: part[0])


# Top-left image coordinates, right/bottom exclusive. Rectangles include swords.
# Containment of whole connected components prevents neighboring-row bleed.
SOURCE_ROWS = [
    ("IDLE", [(275,67,385,207), (467,67,577,207), (659,67,769,207),
              (851,67,961,207), (1040,65,1150,207), (1232,65,1342,207)]),
    ("WALK", [(254,301,369,439), (445,300,560,439), (638,297,752,439),
              (828,297,943,439), (1021,297,1136,439), (1214,300,1335,439),
              (1402,301,1517,439), (1597,300,1711,438)]),
    ("RUN", [(252,517,367,659), (457,519,560,659), (657,519,764,645),
             (839,520,960,649), (1016,518,1129,661), (1204,516,1320,661),
             (1402,517,1518,658), (1606,520,1711,659)]),
    ("FIGHTING STANCE", [(254,732,401,871), (447,732,594,871),
                         (641,731,787,871), (832,730,979,871),
                         (1026,729,1172,871), (1219,732,1365,871)]),
    ("ATTACK 1", [(237,944,443,1082), (433,912,590,1083),
                  (670,856,799,1083), (859,859,1051,1082),
                  (1055,944,1258,1082)]),
]
