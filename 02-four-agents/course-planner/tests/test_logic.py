"""Tests for logic.py. Sample data, made for this workshop.

Run: python -m unittest
"""
import unittest

from logic import Course, gpa, total_credits


def make(credits, grade):
    return Course(code="TST 100", name="Test", credits=credits, grade=grade, day="Sun")


class TestLogic(unittest.TestCase):
    def test_total_credits(self):
        courses = [make(3, "A"), make(4, "B"), make(1, "F")]
        self.assertEqual(total_credits(courses), 8)

    def test_gpa_known_set(self):
        # A+ (4.00) and B (3.00), both 3 credits: (12 + 9) / 6 = 3.50
        courses = [make(3, "A+"), make(3, "B")]
        self.assertAlmostEqual(gpa(courses), 3.50)

    def test_gpa_empty_list(self):
        self.assertEqual(gpa([]), 0.0)


if __name__ == "__main__":
    unittest.main()
