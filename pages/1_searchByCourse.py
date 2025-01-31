import pandas as pd
import streamlit as st
import plotly.express as px
import os


def academic_term_sort_key(term):
    season_order = {'F': 0, 'W': 1, 'S': 2}  # Define the order for seasons
    season, year = term[0], int(term[1:])  # Extract season and year
    # Adjust the year for sorting based on season
    adjusted_year = year if season == 'F' else year - 1
    return adjusted_year, season_order[season]

# def sort_df_by_term(df):
#     # Sort the DataFrame using the custom key
#     df['SortKey'] = df['TermName'].apply(academic_term_sort_key)
#     df = df.sort_values('SortKey').drop(columns=['SortKey'])
#
#     # Reset the index after sorting
#     df.reset_index(drop=True, inplace=True)
#     return df


# Dynamically resolve the CSV path
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "selected_classes_byProf.csv")

st.set_page_config(layout="wide")

st.title("McGill Professor Difficulty Dashboard")

# Read and display the CSV

data = pd.read_csv(DATA_FILE)

df = data.filter(items = ["Course", "TermName", "ClassAveLetter", "ClassAveNum", "Instructor_1", "Instructor_2",
                          "Instructor_3"])

course_name = st.text_input("Enter course code: (e.g. 'MATH558')")
course_name = "".join(course_name.split()).upper()
courseOverTime = df[df['Course'] == course_name]

courseCodes_count = data.groupby('SubjectCode').size().reset_index(name='Count')


#Landing Page
if course_name == "":
    st.header(f"Welcome to the dashboard!")
    st.write("Enter a course code above to get started!")

    st.divider()

    col1, col2 = st.columns([0.5, 0.5])

    with col1:
        # DEPARTMENTS PIE CHART
        fig = px.pie(courseCodes_count, values='Count', names='SubjectCode', title=
            f"Departments Represented:")
        #color_discrete_sequence=px.colors.sequential.amp_r

        st.plotly_chart(fig, theme=None, use_container_width=False)

    with col2:
        col11, col12 = st.columns([0.5, 0.5])

        with col11:
            st.metric(label="Courses Represented:",
                  value=data.groupby('Course').size().reset_index(name='Count').shape[0])

        with col12:
            st.metric(label="Terms Represented:",
                  value=data.groupby('TermName').size().reset_index(name='Count').shape[0])

        summary = data.groupby(['SubjectCode', 'TermName'])['ClassAveNum'].mean().reset_index()

        # Rename columns for clarity if needed
        summary.rename(columns={'ClassAveNum': 'MeanGPA'}, inplace=True)

        summary['TermName'] = pd.Categorical(
            summary['TermName'],
            categories=sorted(data['TermName'].unique(), key=academic_term_sort_key),
            ordered=True
        )

        sorted_summary = summary.sort_values('TermName')

        # Display or use the summarized DataFrame
        grades_by_time_bar = px.line(sorted_summary, x="TermName", y="MeanGPA", color="SubjectCode",
                                     color_discrete_sequence=px.colors.sequential.amp_r)

        st.write(sorted_summary)
        st.plotly_chart(grades_by_time_bar)


#Mis-input
elif courseOverTime.shape[0] == 0:
    st.write(f"We have no historical data about {course_name}. It is possible that it does not "
             f"exist as a course at McGill.")

#Statistics by Class
else:
    st.header(f"Statistics for {course_name}")
    col1, col2 = st.columns([0.45, 0.55])

    sorted_courseOverTime = courseOverTime.sort_values(by="ClassAveNum")
    median_grade = sorted_courseOverTime["ClassAveLetter"].iloc[sorted_courseOverTime.shape[0] // 2]

    #prof_name = st.text_input("Enter Professor name: (e.g. 'Asgharian, Masoud')")

    # PIE CHART
    first_term = courseOverTime["TermName"].iloc[0]
    pie_df = courseOverTime.groupby('Instructor_1').size().reset_index(name='Count')

    fig = px.pie(pie_df, values='Count', names='Instructor_1', title=f"{course_name} Professor Distribution "
                                f"since {first_term}", color_discrete_sequence=px.colors.sequential.Agsunset)


    #Computing the median grade of a course


    with col1:

        col11, col12 = st.columns(2)

        with col11:

            st.metric(label = "Median Grade", value=median_grade)

        st.plotly_chart(fig, theme=None, use_container_width=True)

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
        # st.write("Course Average by Professor")
        # st.bar_chart(sortedCourseAveByProf, x="Instructor_1", y="ClassAveNum", x_label="Professor",
        #              y_label="Average GPA Points", color="Count")

        #df = px.data.gapminder().query("continent == 'Oceania'")
        fig = px.bar(sortedCourseAveByProf, x='Instructor_1', y='ClassAveNum',
                     hover_data=['Instructor_1', 'ClassAveNum'], color='Count',
                     labels={'Instructor_1': 'Professor'}, height=400,
                     color_continuous_scale=['#8B0000', '#A23232', '#B86464', '#CF9696', '#E5C8C8']
)

        #fig.show()

        st.plotly_chart(fig)



        st.divider()

        st.write("Course Average over Time")
        st.bar_chart(courseOverTime, x="TermName", y="ClassAveNum", x_label="Term", y_label="Average GPA Points",
                     color="#8B0000")

    #Build out courses page first




