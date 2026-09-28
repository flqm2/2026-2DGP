from pico2d import *
import math


WIDTH, HEIGHT = 800, 600
CENTER_X, CENTER_Y = 400, 300
RADIUS = 200
SPEED = 180
FRAME_TIME = 0.01


def move_on_segment(start, end, distance):
	"""Return a point distance pixels from start, clamped to this segment."""
	dx = end[0] - start[0]
	dy = end[1] - start[1]
	length = math.hypot(dx, dy)
	if length == 0:
		return end, 0

	traveled = min(distance, length)
	ratio = traveled / length
	return (start[0] + dx * ratio, start[1] + dy * ratio), length - traveled


def move_on_path(path, distance):
	"""Move along a closed path and return (position, remaining, completed)."""
	traveled = distance
	for start, end in zip(path, path[1:]):
		segment_length = math.hypot(end[0] - start[0], end[1] - start[1])
		if distance <= segment_length:
			position, _ = move_on_segment(start, end, distance)
			return position, traveled, False
		distance -= segment_length
	return path[-1], 0.0, True


open_canvas(WIDTH, HEIGHT)
character = load_image('character.png')

circle_start_angle = 0.0
circle_angle = circle_start_angle
circle_end = (CENTER_X + RADIUS, CENTER_Y)

# Each path starts where the previous path finishes.
square_path = [
	circle_end,
	(circle_end[0], circle_end[1] + 120),
	(circle_end[0] - 120, circle_end[1] + 120),
	(circle_end[0] - 120, circle_end[1]),
	circle_end,
]

# An equilateral triangle: all interior angles are 60 degrees.
triangle_start = square_path[-1]
triangle_height = 120 * math.sqrt(3) / 2
triangle_path = [
	triangle_start,
	(triangle_start[0] - 120, triangle_start[1]),
	(triangle_start[0] - 60, triangle_start[1] + triangle_height),
	triangle_start,
]

paths = ('circle', 'square', 'triangle')
phase = 0
path_distance = 0.0
running = True

while running:
	for event in get_events():
		if event.type == SDL_QUIT:
			running = False
		elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
			running = False

	current_path = paths[phase]
	if current_path == 'circle':
		circle_angle += SPEED * FRAME_TIME / RADIUS
		if circle_angle >= circle_start_angle + 2 * math.pi:
			circle_angle = circle_start_angle + 2 * math.pi
			phase = 1
			path_distance = 0.0
		x = CENTER_X + RADIUS * math.cos(circle_angle)
		y = CENTER_Y + RADIUS * math.sin(circle_angle)
	else:
		path = square_path if current_path == 'square' else triangle_path
		position, path_distance, completed = move_on_path(
			path, path_distance + SPEED * FRAME_TIME
		)
		x, y = position
		if completed:
			phase = (phase + 1) % len(paths)
			path_distance = 0.0
			if phase == 0:
				circle_angle = circle_start_angle

	clear_canvas()
	character.draw(x, y)
	update_canvas()
	delay(FRAME_TIME)

close_canvas()
