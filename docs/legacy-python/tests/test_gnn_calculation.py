"""Check the teaching example against hand-expanded arithmetic."""
import math
from pathlib import Path
import sys
import unittest

SOURCE = Path(__file__).resolve().parents[1] / 'source'
sys.path.insert(0, str(SOURCE))
from gnn_figures import gat_values, FEATURES

class GATCalculationTests(unittest.TestCase):
    def test_full_head_matches_expanded_example(self):
        z, raw, scores, exps, alpha, parts, out = gat_values()
        self.assertEqual(z, [(1, 1), (-2, 2), (1, 3), (0, 2)])
        self.assertEqual(raw, [.5, -2, 1.5, 0])
        self.assertEqual(scores, [.5, -.4, 1.5, 0])
        denominator = math.exp(.5) + math.exp(-.4) + math.exp(1.5) + 1
        self.assertAlmostEqual(sum(alpha), 1)
        self.assertGreater(alpha[1], 0)
        self.assertAlmostEqual(out[0], (math.exp(.5)-2*math.exp(-.4)+math.exp(1.5))/denominator)
        self.assertAlmostEqual(out[1], (math.exp(.5)+2*math.exp(-.4)+3*math.exp(1.5)+2)/denominator)

    def test_reordering_neighbors_preserves_output(self):
        expected = gat_values()[-1]
        reordered = gat_values([FEATURES[i] for i in [0, 3, 1, 2]])[-1]
        for actual, wanted in zip(reordered, expected):
            self.assertAlmostEqual(actual, wanted)

    def test_second_head_has_own_projection_and_coefficients(self):
        values = gat_values(w=[(1, 0), (0, 1)], a=[0, 1, -1, .5])
        self.assertEqual(values[1], [-1, 1, -1.5, -.5])
        self.assertNotEqual(values[4], gat_values()[4])
        self.assertEqual(len(gat_values()[-1] + values[-1]), 4)
