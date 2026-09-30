"""Deterministic checks for timing boundaries and the real 33-frame manifest."""
import unittest
from animation_viewer import (
    CANVAS_HEIGHT, CANVAS_WIDTH, MIN_CHARACTER_HEIGHT, PAUSE_SECONDS,
    REPEAT_COUNT, Player, animation_scale, load_animations, validate_animations,
    Animation, Frame,
)


class AnimationTests(unittest.TestCase):
    def setUp(self):
        self.atlas, self.actions = load_animations()
        self.player = Player(self.actions)

    def test_real_asset_counts_and_variable_dimensions(self):
        self.assertTrue(self.atlas.is_file())
        self.assertEqual([len(a.frames) for a in self.actions], [6, 8, 8, 6, 5])
        self.assertGreater(len({(f.width, f.height) for a in self.actions for f in a.frames}), 10)

    def test_every_frame_has_full_duration_and_exactly_five_loops(self):
        for index, action in enumerate(self.actions):
            self.assertEqual(self.player.action_index, index)
            for loop in range(REPEAT_COUNT):
                for frame in range(len(action.frames)):
                    self.assertEqual(self.player.frame_index, frame)
                    self.assertEqual(self.player.completed_loops, loop)
                    self.assertFalse(self.player.paused)
                    self.player.update(action.frame_seconds - 0.001)
                    self.assertEqual(self.player.frame_index, frame)
                    self.assertFalse(self.player.paused)
                    self.player.update(0.001)
            self.assertTrue(self.player.paused)
            self.assertEqual(self.player.completed_loops, 5)
            self.assertEqual(self.player.frame_index, len(action.frames) - 1)
            self.player.update(0.999)
            self.assertTrue(self.player.paused)
            self.assertEqual(self.player.action_index, index)
            self.player.update(0.001)
            self.assertFalse(self.player.paused)
        self.assertEqual(self.player.action_index, 0)
        self.assertEqual(self.player.frame_index, 0)

    def test_large_elapsed_matches_small_steps(self):
        duration = sum(len(a.frames) * a.frame_seconds * 5 + 1 for a in self.actions)
        self.player.update(duration * 3 + 0.25)
        other = Player(self.actions)
        for _ in range(round(duration * 3 * 100)):
            other.update(0.01)
        other.update(0.25)
        self.assertEqual((self.player.action_index, self.player.frame_index, self.player.paused),
                         (other.action_index, other.frame_index, other.paused))
        self.assertAlmostEqual(self.player.remaining, other.remaining)

    def test_enlargement_preserves_ratio_and_fits_all_frames(self):
        for action in self.actions:
            scale = animation_scale(action)
            for frame in action.frames:
                self.assertGreaterEqual(frame.height * scale + 1e-9, MIN_CHARACTER_HEIGHT)
                self.assertLessEqual(frame.height * scale, CANVAS_HEIGHT - 70)
                self.assertLessEqual(frame.width * scale, CANVAS_WIDTH - 40)

    def test_reject_invalid_metadata_and_time(self):
        with self.assertRaises(ValueError):
            validate_animations((Animation("bad", (Frame(0, 0, 20, 20),), .1),), (10, 10))
        with self.assertRaises(ValueError):
            validate_animations((Animation("empty", (), .1),), (10, 10))
        for elapsed in (-1, float("inf"), float("nan")):
            with self.assertRaises(ValueError):
                self.player.update(elapsed)


if __name__ == "__main__":
    unittest.main()
