class Professor:
    def __init__(self, last_name, given_name, courses=[]):
        self.last_name = last_name
        self.first_name = given_name

        #List of Tuples, first entry being the name of a course the second being amount of times
        # one's having taught the course
        self.courses = courses



class Course:
    def __init__(self, age, freq, profs):
        self.age = age #years the course has been available
        self.frequency = freq #how often is the course offered
        self.professors = profs #List of tuples, first entry being the name of a prof the second being amount of times
        # they have taught the course


