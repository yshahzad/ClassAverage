import pandas as pd
import streamlit as st
import plotly.express as px
import os

# Dynamically resolve the CSV path
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "math_classes_byProf.csv")

st.set_page_config(layout="wide")

st.title("McGill Professor Difficulty Dashboard")

# Read and display the CSV

data = pd.read_csv(DATA_FILE)
df = data.filter(items = ["Course", "TermName", "ClassAveLetter", "ClassAveNum", "Instructor_1", "Instructor_2",
                          "Instructor_3", "Instructor 4"])

course_name = st.text_input("Enter course code: (e.g. 'MATH558')")
course_name = "".join(course_name.split()).upper()
courseOverTime = df[df['Course'] == course_name]

st.header(f"Statistics for {course_name}")
col1, col2 = st.columns([0.45, 0.55])

sorted_courseOverTime = courseOverTime.sort_values(by="ClassAveNum")
median_grade = sorted_courseOverTime["ClassAveLetter"].iloc[sorted_courseOverTime.shape[0] // 2]

#prof_name = st.text_input("Enter Professor name: (e.g. 'Asgharian, Masoud')")


# PIE CHART
first_term = courseOverTime["TermName"].iloc[0]
pie_df = courseOverTime.groupby('Instructor_1').size().reset_index(name='Count')

fig = px.pie(pie_df, values='Count', names='Instructor_1', title=f"{course_name} Professor Distribution "
                                                               f"since {first_term}")


#Computing the median grade of a course


with col1:

    col11, col12 = st.columns(2)

    with col11:

        st.metric(label = "Median Grade", value=median_grade)

    st.plotly_chart(fig, theme=None)

# COURSE AVERAGE OVER TIME
# st.write("Course Average over Time")
# st.bar_chart(courseOverTime, x="TermName", y="ClassAveNum", x_label="Term", y_label="Average GPA Points")

# COURSE AVERAGE BY PROF
courseAveByProf = courseOverTime.groupby('Instructor_1')['ClassAveNum'].mean().reset_index()
courseAveByProf.columns = ['Instructor_1', 'ClassAveNum']
courseAveByProf["Count"] = pie_df["Count"]

# st.write("Course Average by Professor")
#TODO: Fix the sort feature of the grades by prof chart
sortedCourseAveByProf = courseAveByProf.sort_values(by="ClassAveNum", ascending=False)

# st.bar_chart(sortedCourseAveByProf, x="Instructor_1", y="ClassAveNum", x_label="Professor",
#              y_label="Average GPA Points", color="Count")

#st.bar_chart(sortedCourseAveByProf.set_index('Instructor_1')['ClassAveNum'])

st.write(sortedCourseAveByProf)

with col2:
    st.write("Course Average by Professor")
    st.bar_chart(sortedCourseAveByProf, x="Instructor_1", y="ClassAveNum", x_label="Professor",
                 y_label="Average GPA Points", color="Count")

    st.divider()

    st.write("Course Average over Time")
    st.bar_chart(courseOverTime, x="TermName", y="ClassAveNum", x_label="Term", y_label="Average GPA Points")







#Build out courses page first




