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
