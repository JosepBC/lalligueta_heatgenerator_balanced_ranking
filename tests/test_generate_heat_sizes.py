import unittest
from heat_sizes import generate_heat_sizes


class TestGenerateHeatSizes(unittest.TestCase):

    def test_small_groups(self):
        self.assertEqual(generate_heat_sizes(1), [1])
        self.assertEqual(generate_heat_sizes(2), [2])
        self.assertEqual(generate_heat_sizes(3), [3])
        self.assertEqual(generate_heat_sizes(4), [4])
        self.assertEqual(generate_heat_sizes(5), [5])

    def test_multiple_of_five(self):
        self.assertEqual(generate_heat_sizes(10), [5, 5])
        self.assertEqual(generate_heat_sizes(20), [5, 5, 5, 5])
        self.assertEqual(generate_heat_sizes(25), [5, 5, 5, 5, 5])

    def test_minus_one(self):
        self.assertEqual(generate_heat_sizes(21), [3, 3, 5, 5, 5])

    def test_minus_two(self):
        self.assertEqual(generate_heat_sizes(22), [3, 4, 5, 5, 5])

    def test_minus_three(self):
        self.assertEqual(generate_heat_sizes(23), [4, 4, 5, 5, 5])

    def test_minus_four(self):
        self.assertEqual(generate_heat_sizes(24), [4, 5, 5, 5, 5])

    def test_total_pilots_preserved(self):
        for pilots in range(10, 30):
            heats = generate_heat_sizes(pilots)
            self.assertEqual(sum(heats), pilots)

    def test_max_heat_size(self):
        heats = generate_heat_sizes(50)
        for h in heats:
            self.assertLessEqual(h, 5)

    def test_min_heat_size(self):
        heats = generate_heat_sizes(50)
        for h in heats:
            self.assertGreaterEqual(h, 3)


if __name__ == "__main__":
    unittest.main()
