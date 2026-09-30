"""Course Planner page. Sample data, made for this workshop.

Run: streamlit run app.py
"""
import streamlit as st

from logic import gpa, load_courses, total_credits

st.set_page_config(page_title="Course Planner")
st.title("Course Planner")
st.caption("Sample data, made for this workshop.")

courses = load_courses("courses.csv")

col1, col2 = st.columns(2)
col1.metric("Total credits", total_credits(courses))
col2.metric("GPA", f"{gpa(courses):.2f}")

st.subheader("Courses")
st.dataframe(
    [
        {"Code": c.code, "Name": c.name, "Credits": c.credits, "Grade": c.grade, "Day": c.day}
        for c in courses
    ],
    hide_index=True,
)

st.subheader("Credits per course")
st.bar_chart({c.code: c.credits for c in courses})
