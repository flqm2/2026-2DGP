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


    def update(self, elapsed):
        """Consume real elapsed time, including leftover time across transitions."""
        if not math.isfinite(elapsed) or elapsed < 0:
            raise ValueError("Elapsed time must be finite and nonnegative")
        while elapsed + 1e-12 >= self.remaining:
            elapsed = max(0.0, elapsed - self.remaining)
            if self.paused:
                self.action_index = (self.action_index + 1) % len(self.animations)
                self.frame_index = 0
                self.completed_loops = 0
                self.paused = False
                self.remaining = self.action.frame_seconds
            elif self.frame_index + 1 < len(self.action.frames):
                self.frame_index += 1
                self.remaining = self.action.frame_seconds
            else:
                self.completed_loops += 1
                if self.completed_loops == REPEAT_COUNT:
                    self.paused = True  # keep the final frame visible
                    self.remaining = PAUSE_SECONDS
                else:
                    self.frame_index = 0
                    self.remaining = self.action.frame_seconds
        self.remaining -= elapsed


def animation_scale(action):
    """One scale per action keeps pose changes from causing zoom flicker."""
    scale = MIN_CHARACTER_HEIGHT / min(frame.height for frame in action.frames)
    if (max(frame.height for frame in action.frames) * scale > CANVAS_HEIGHT - 70
            or max(frame.width for frame in action.frames) * scale > CANVAS_WIDTH - 40):
        raise ValueError(f"Cannot enlarge {action.name} without clipping")
    return scale

