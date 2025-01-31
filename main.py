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

def split_instructors_list(df, n_instructors):
    for i in range(n_instructors):
        df[f"Instructor_{i + 1}"] = None

    for i, row in df.iterrows():

        if not pd.isna(row["Instructor"]):
            instructors = row["Instructor"].split("; ")

            # Records first 3 instructors per term
            for j in range(n_instructors):
                if j < len(instructors):
                    df.loc[i, f"Instructor_{j + 1}"] = instructors[j]

    return df

data = pd.read_csv("data/classAvgs_W2024.csv").drop(0)

#IMPORTANT: DEFINE SUBJECT CODE BELOW

depts_to_scrape = ["MATH", "PSYC", "COMP", "PHYS", "ECON", "SOCI", "ENGL", "BIOL"]
subject = "selected"

subjectCodes = []
for course in data["Course"]:
    subject_code = course[:4]
    subjectCodes.append(subject_code)

data["SubjectCode"] = subjectCodes

classAvgs = data.filter(items = ["Course", "TermName", "ClassAveLetter", "ClassAveNum", "SubjectCode"])

#Filters classes for certain subjects. REMOVE BEFORE FINAL ANALYSIS!
#classAvgs = classAvgs.loc[classAvgs["SubjectCode"].isin([subject])]
classAvgs = classAvgs.loc[classAvgs["SubjectCode"].isin(depts_to_scrape)]

print(classAvgs.head(15))

classes = classAvgs["Course"].unique()

classAvgs["URL"] = getURLs(classAvgs)

instructors = []

scrape_progress_counter = 0
for i, row in classAvgs.iterrows():

    print(f"Progress: {scrape_progress_counter} / {classAvgs.shape[0]} - "
          f"{scrape_progress_counter * 100/ classAvgs.shape[0]} %")

    scrape_progress_counter += 1

    term_name = row["TermName"]
    course_name = row["Course"]

    print(row["URL"])

    prof = scrape_instructor(row["URL"])

    if prof is None:
        instructor = None

    else:
        seasonal_dict = split_instructors_by_season(prof)

        if term_name[0] == "F":
            instructor = check_term_season("Fall", seasonal_dict)
        elif term_name[0] == "W":
            instructor = check_term_season("Winter", seasonal_dict)
        else:
            instructor = check_term_season("Summer", seasonal_dict)

    instructors.append(instructor)

    print(instructor)
    #print(seasonal_dict)

classAvgs["Instructor"] = instructors

classAvgByProf = split_instructors_list(classAvgs, n_instructors=3)

classAvgByProf.to_csv(f"{subject.lower()}_classes_byProf.csv")
