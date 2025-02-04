import pandas as pd
import streamlit as st
import plotly.express as px
import os

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "selected_classes_byProf.csv")

st.set_page_config(layout="wide", 
                   page_icon="🦉",
                   initial_sidebar_state="collapsed",
                   menu_items={"Report a bug": "mailto:yavuz.shahzad@mail.mcgill.ca"})


st.title("ProfSight McGill: Instructor Dashboard")

data = pd.read_csv(DATA_FILE)

df = data.filter(items = ["Course", "TermName", "ClassAveLetter", "ClassAveNum", "Instructor_1", "Instructor_2",
                          "Instructor_3"])

prof_name = st.text_input("Enter an instructor's name: (eg. Jakobson, Dmitry)")

#GET ALL CLASSES A PROF HAS TAUGHT
prof_courses = df[df['Instructor_1'] == prof_name]

st.divider()

#Initial State
if prof_name == "":
    st.write('''Enter an instructors name above to get started! Please make sure you enter the name in the form 
             "Last, First Middle".''')

#Misinput

elif prof_courses.shape[0] == 0:
    st.write('''We could not find a McGill instructor of the provided name. Please make sure you enter the name in the form 
             "Last, First Middle"''')


#Correct Input
else:
    summary = prof_courses.groupby(['Course'])['ClassAveNum'].mean().reset_index()
    summary_pie = prof_courses.groupby('Course').size().reset_index(name="Count")


    #METRICS

    total_means = df[df["Course"].isin(summary["Course"])].groupby(['Course'])['ClassAveNum'].mean().reset_index()
    summary["AllProfMeanNum"] = total_means["ClassAveNum"]
    summary["Diff"] = summary["ClassAveNum"] - summary["AllProfMeanNum"]

    #columns 1 and 5 remain empty, for spacing.
    col1, col2, col3, col4, col5 = st.columns(5)

    with col2:
        st.metric(label="Difference from Mean", value=round(summary["Diff"].mean(), 2), delta=None, delta_color="normal", help=None, 
            label_visibility="visible", border=False)
        
    with col3:
        z_score = (prof_courses["ClassAveNum"].mean() - total_means["ClassAveNum"].mean()) / total_means["ClassAveNum"].std()
        st.metric(label="Z-Score", value=round(z_score, 2), delta=None, delta_color="normal", help=None, 
                label_visibility="visible", border=False)
        
    with col4:
        st.metric(label="No. Courses Taught", value=prof_courses.shape[0])

    st.divider()

    col1, col2 = st.columns([0.5, 0.5])

    with col1:
        #COURSES PIE CHART
        st.write(f"**Courses Taught**")
        fig = px.pie(summary_pie, values='Count', names='Course')
        #color_discrete_sequence=px.colors.sequential.amp_r
        st.plotly_chart(fig)

    with col2:
        #MEAN GPA BY COURSE BAR
        st.write(f"**Mean GPA by Course**")
        fig_bar = px.bar(summary, x='Course', y='ClassAveNum',
                            hover_data=['Course', 'ClassAveNum'], height=400,
                            color_continuous_scale=['#8B0000', '#A23232', '#B86464', '#CF9696', '#E5C8C8'])

        st.plotly_chart(fig_bar)




