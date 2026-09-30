"""Drill #8: five pico2d animations, five loops each, one-second holds."""
from dataclasses import dataclass
import json
import math
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parent
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
REPEAT_COUNT = 5
PAUSE_SECONDS = 1.0
MIN_CHARACTER_HEIGHT = CANVAS_HEIGHT * 0.5


@dataclass(frozen=True)
class Frame:
    left: int
    bottom: int
    width: int
    height: int


@dataclass(frozen=True)
class Animation:
    name: str
    frames: tuple[Frame, ...]
    frame_seconds: float


def load_animations(path=ROOT / "animation_frames.json"):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    actions = tuple(Animation(
        item["name"],
        tuple(Frame(**{key: frame[key] for key in ("left", "bottom", "width", "height")})
              for frame in item["frames"]),
        item["frame_seconds"],
    ) for item in data["animations"])
    validate_animations(actions, data["size"])
    return ROOT / data["image"], actions

