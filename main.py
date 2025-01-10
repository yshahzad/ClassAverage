#Get a list of courses to scrape
import pandas as pd
import numpy as np
from eCalendar_scraper import *

def getURLs(df):
    weblinks = []

    for i, row in df.iterrows():
        term_name = row["TermName"]
        course_name = row["Course"]

        # Works for D1/D2 courses
        course_code = f"{course_name[0:4]}-{course_name[4:]}".lower()

        if term_name[0] == "F":
            year = int(term_name[1:])
        else:
            year = int(term_name[1:]) - 1

        weblink = f"https://www.mcgill.ca/study/{year}-{year + 1}/courses/{course_code}"
        weblinks.append(weblink)

    return weblinks

def check_term_season(season, seasonal_dict):
    '''
    Returns the instructor(s) associated with a specific season of an academic year. Also verifies that
    the eCalendar contains information on the term/season in question.
    '''
    if not season in seasonal_dict.keys():
        instructor = "None"
    else:
        instructor = seasonal_dict[season]

    return instructor


data = pd.read_csv("data/classAvgs_W2024.csv").drop(0)

subjectCodes = []
for course in data["Course"]:
    subject_code = course[:4]
    subjectCodes.append(subject_code)

data["SubjectCode"] = subjectCodes

#print(subjectCodes)

classAvgs = data.filter(items = ["Course", "TermName", "ClassAveLetter", "SubjectCode"])

#Filters classes for certain subjects. REMOVE BEFORE FINAL ANALYSIS!
classAvgs = classAvgs.loc[classAvgs["SubjectCode"].isin(["MATH"])]

print(classAvgs.head(15))

classes = classAvgs["Course"].unique()

classAvgs["URL"] = getURLs(classAvgs)

instructors = []

for i, row in classAvgs.iterrows():
    term_name = row["TermName"]
    course_name = row["Course"]

    print(row["URL"])

    prof = scrape_instructor(row["URL"])
    seasonal_dict = split_instructors_by_season(prof)

    if term_name[0] == "F":
        instructor = check_term_season("Fall", seasonal_dict)
    elif term_name[0] == "W":
        instructor = check_term_season("Winter", seasonal_dict)
    else:
        instructor = check_term_season("Summer", seasonal_dict)

    instructors.append(instructor)

    print(instructor)
    print(seasonal_dict)

classAvgs["Instructor"] = instructors

classAvgs.to_csv("MATH_classes.csv")





