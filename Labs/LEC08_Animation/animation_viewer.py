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


def draw_frame(pico, atlas, player, font=None):
    pico.clear_canvas()
    frame = player.frame
    scale = animation_scale(player.action)
    atlas.clip_draw(frame.left, frame.bottom, frame.width, frame.height,
                    CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2,
                    frame.width * scale, frame.height * scale)
    if font:
        phase = (f"HOLD {player.remaining:.1f}s" if player.paused
                 else f"LOOP {player.completed_loops + 1}/{REPEAT_COUNT}")
        font.draw(20, CANVAS_HEIGHT - 28,
                  f"{player.action_index + 1}/{len(player.animations)}  "
                  f"{player.action.name} | FRAME {player.frame_index + 1}/"
                  f"{len(player.action.frames)} | {phase}", (25, 25, 25))
        font.draw(20, 22, "ESC: quit | 5 loops > 1 second hold > next animation", (25, 25, 25))
    pico.update_canvas()


def load_status_font(pico):
    """Status text is optional; animation also works without a system font."""
    import os
    fonts = [Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts/arial.ttf",
             Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")]
    for path in fonts:
        if path.is_file():
            return pico.load_font(str(path), 18)
    return None


def quit_requested(pico):
    return any(event.type == pico.SDL_QUIT
               or (event.type == pico.SDL_KEYDOWN and event.key == pico.SDLK_ESCAPE)
               for event in pico.get_events())


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate assets without opening a window")
    parser.add_argument("--smoke-test", action="store_true", help="render every frame once, then close")
    args = parser.parse_args()
    atlas_path, actions = load_animations()
    if not atlas_path.is_file():
        raise FileNotFoundError(atlas_path)
    for action in actions:
        animation_scale(action)
    if args.check:
        print("Validated: " + ", ".join(f"{a.name}={len(a.frames)}" for a in actions))
        return

    import pico2d as pico
    pico.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        pico.hide_lattice()
        atlas = pico.load_image(str(atlas_path))
        font = load_status_font(pico)
        player = Player(actions)
        if args.smoke_test:
            for action_index, action in enumerate(actions):
                player.action_index = action_index
                for frame_index in range(len(action.frames)):
                    if quit_requested(pico):
                        return
                    player.frame_index = frame_index
                    draw_frame(pico, atlas, player, font)
            print("Rendered all 33 frames using pico2d")
            return
        previous = time.perf_counter()
        while not quit_requested(pico):
            now = time.perf_counter()
            player.update(now - previous)
            previous = now
            draw_frame(pico, atlas, player, font)
            pico.delay(0.01)  # events stay responsive even in the one-second hold
    finally:
        pico.close_canvas()


if __name__ == "__main__":
    main()
