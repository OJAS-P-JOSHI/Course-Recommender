import os
import pickle
import streamlit as st
import pandas as pd

# Error handling for pickle loading
try:
    courses_list = pickle.load(open('courses.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("Error: 'courses.pkl' and 'similarity.pkl' files not found. Please ensure they exist in the project directory.")
    exit(1)

# Recommendation function with improved clarity
def recommend(course_name):
    """Recommends courses similar to the provided course name.

    Args:
        course_name (str): Name of the course to base recommendations on.

    Returns:
        list: List of recommended course names.
    """
    try:
        index = courses_list[courses_list['course_name'] == course_name].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_course_names = [courses_list.iloc[i[0]].course_name for i in distances[1:7]]
        return recommended_course_names
    except IndexError:
        st.error(f"Error: Course '{course_name}' not found in the dataset.")
        return []

# Streamlit app layout and styling
st.set_page_config(page_title="Coursera Course Recommendation System", page_icon="")  # Set page title and icon

st.markdown("""
<h1 style='text-align: center; color: #0056b3;'>Coursera Course Recommendation System</h1>
""", unsafe_allow_html=True)

# Course selection dropdown with user-friendly message
selected_course = st.selectbox(
    "Select a course to find recommendations:",
    courses_list['course_name'],
    key="course_selection"
)

# Show recommended courses button
if st.button('Show Recommended Courses'):
    recommended_course_names = recommend(selected_course)
    if recommended_course_names:
        st.markdown("<h2 style='color: #0056b3;'>Recommended Courses for You:</h2>", unsafe_allow_html=True)
        for i, course in enumerate(recommended_course_names, start=1):
            st.write(f"**{i}.** {course}")
    else:
        st.info("No recommendations found for this course. Try a different one!")

# Footer with copyright information and centered alignment
st.markdown("<hr style='margin-top: 50px; margin-bottom: 10px; border: 0; border-top: 1px solid #ddd;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #777;'>© 2024 Coursera. All rights reserved.</p>", unsafe_allow_html=True)
