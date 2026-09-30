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


def validate_animations(actions, size):
    if not actions or len(size) != 2 or any(v <= 0 for v in size):
        raise ValueError("An atlas needs dimensions and at least one animation")
    for action in actions:
        if not action.frames or not math.isfinite(action.frame_seconds) or action.frame_seconds <= 0:
            raise ValueError(f"Invalid frame count or duration: {action.name}")
        for frame in action.frames:
            values = (frame.left, frame.bottom, frame.width, frame.height)
            if any(type(value) is not int for value in values):
                raise ValueError("Frame coordinates must be integers")
            if (frame.left < 0 or frame.bottom < 0 or frame.width <= 0 or frame.height <= 0
                    or frame.left + frame.width > size[0]
                    or frame.bottom + frame.height > size[1]):
                raise ValueError(f"Frame outside atlas: {action.name}, {frame}")


class Player:
    def __init__(self, animations):
        if not animations:
            raise ValueError("No animations to play")
        self.animations = animations
        self.action_index = 0
        self.frame_index = 0
        self.completed_loops = 0
        self.paused = False
        self.remaining = self.action.frame_seconds

    @property
    def action(self):
        return self.animations[self.action_index]

    @property
    def frame(self):
        return self.action.frames[self.frame_index]

