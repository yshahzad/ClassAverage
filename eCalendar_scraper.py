import requests
import numpy as np
import re
from bs4 import BeautifulSoup

def scrape_instructor(url):
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.text
    else:
        print(f"Failed to fetch webpage. Status code: {response.status_code}")
        exit()

    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Scrapes instructor names
    instructor_tag = soup.find('p', class_='catalog-instructors')

    if instructor_tag:
        raw_text = instructor_tag.text.strip()
        # Remove the "Instructors:" prefix
        instructors = raw_text.removeprefix("Instructors: ").strip()
        #print(f"Instructors: {instructors}")
    else:
        print("Instructors' information not found.")
        #instructors = np.nan

    return instructors

def split_instructors_by_season(instructor_string):

    if "There are no instructors associated with" in instructor_string:
        return np.nan

    # Regex to match each season's data
    pattern = r'(.*?)\((Fall|Winter|Summer)\)'

    matches = re.findall(pattern, instructor_string)

    season_data = {}
    for i, (instructors, season) in enumerate(matches):
        instructors = instructors.strip("; ").strip()
        season_data[season] = instructors

        if i == len(matches) - 1:
            remaining = instructor_string.split(matches[i][0] + f"({season})")[-1].strip()
            if remaining:
                season_data[season] += "; " + remaining

    # Print the results
    #for season, instructors in season_data.items():
    #    print(f"{season}: {instructors}")

    return season_data










