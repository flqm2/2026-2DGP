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

