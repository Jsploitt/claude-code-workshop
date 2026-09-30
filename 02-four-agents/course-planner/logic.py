"""Course planner logic. Sample data, made for this workshop.

Keep all calculations here so they can be tested without the Streamlit page.
"""
import csv
from dataclasses import dataclass

# KFUPM 4.00 scale
GRADE_POINTS = {
    "A+": 4.00,
    "A": 3.75,
    "B+": 3.50,
    "B": 3.00,
    "C+": 2.50,
    "C": 2.00,
    "D+": 1.50,
    "D": 1.00,
    "F": 0.00,
}


@dataclass
class Course:
    code: str
    name: str
    credits: int
    grade: str
    day: str


def load_courses(path):
    """Read courses from a CSV file with columns code,name,credits,grade,day."""
    courses = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            courses.append(
                Course(
                    code=row["code"].strip(),
                    name=row["name"].strip(),
                    credits=int(row["credits"]),
                    grade=row["grade"].strip(),
                    day=row["day"].strip(),
                )
            )
    return courses


def total_credits(courses):
    """Sum of credit hours."""
    return sum(c.credits for c in courses)


def gpa(courses):
    """Credit-weighted GPA on the KFUPM 4.00 scale. Returns 0.0 for an empty list."""
    credits = total_credits(courses)
    if credits == 0:
        return 0.0
    points = sum(GRADE_POINTS[c.grade] * c.credits for c in courses)
    return points / credits
