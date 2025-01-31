import pandas as pd
import streamlit as st
import plotly.express as px
import os

st.header("Welcome to ProfSight!")
st.write('''ProfSight: McGill is an interactive dashboard to help you build an informed degree plan and semester schedule. 
         Gone are the days of endlessly scrolling Reddit and RateMyProf to estimate how difficult a class/professor will be.
         Our **Search by Course** page offers a breakdown of your course's historical class averages by professor and time 
         period. Our **Search by Prof** page offers a unique insight into each professor's teaching history, including their mean 
         class averages, comparisons to other professors teaching similar courses, and more.
         ''')

st.write("Select a dashboard below:")


col1, col2 = st.columns([0.5, 0.5])

with col1:

    st.page_link("pages/1_searchByCourse.py", label="Search By Course")

with col2:

    st.page_link("app.py", label="Search By Prof (currently under construction)")




