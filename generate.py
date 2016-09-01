# This file is responsible for generating the sample Data. generate_people returns a list of Persons,
# which is used for all of the graphing.

from datetime import datetime
from datetime import date
from random import choice
from random import randint

DEF = 4
MONTHS = range(1, 13)
DAYS = range(1, 28)
YEARS = range(2012, 2017)

class Person:
    def __init__(self, age: int, gender: str, duration, logs: [(datetime, str)]):
        # These first 4 attributes are data straight from the database.
        self.age = age
        self.gender = gender
        self.duration = duration
        self.logs = logs

        # Accessing elements from logs is tricky. These attributes abstract it and make the rest of the code cleaner
        self.date = date(self.logs[0][0].year, self.logs[0][0].month, self.logs[0][0].day)
        self.hour = self.logs[0][0].hour
        self.approx_time = self.hour + (self.logs[0][0].minute/60)

    def __repr__(self):
        ''' This method allows us to print a person object in a custom style. The returned string is what is shown
        when printed. '''
        log_string = ""
        for k, v in self.logs:
            log_string += str(k) + " " + v
            log_string += " || "
        return '''
Age: {age}
Gender: {gender}
duration: {duration}
logs: {logs}'''.format(age=self.age, gender=self.gender, duration=self.duration, logs=log_string)

# # # Helper methods to help in generating people # # #

age_chance = [25] * 5 + [35] * 30 + [45] * 40 + [55] * 25 # 100 elements. For example: 30% chance to select 35
def generate_age() -> int:
    ''' Use a weighted list to randomly pick (while favoring certain ages) an age. Vary ages slightly with randint '''
    return choice(age_chance) + randint(-4, 4)

def generate_gender() -> str:
    x = randint(0, 100)
    if x < 70:
        return "male"
    else:
        return "female"

def generate_duration() -> float:
    # It is important to NOT use elif here. If we did, we would have to check that x > 60 and x < 90...
    x = randint(0, 100)
    if x < 60: # 60% chance
        return 4
    if x < 90: # 30% chance
        return 8 + randint(-2, 4)
    else: # 10% chance
        return 15 + randint(0, 8)

def generate_logs(year: int, month: int, day: int) -> [(datetime, str)]:
    # Because we use elif, must do checks like so. generate_duration and generate_logs
    # just show 2 ways to do a similar thing. if's and one check, or elifs and 2 checks.
    x = randint(0, 100)
    if x < 80:
        logs = 1
    elif x >= 80 and x < 90:
        logs = 2
    elif x >= 90 and x < 97:
        logs = 3
    else:
        logs = 4
    log_collection = []
    for i in range(logs):
        log_collection.append((generate_date_time(year, month ,day), generate_emotion()))

    return log_collection

def generate_date_time(year: int, month: int, day: int) -> datetime:
    x = randint(0, 100)
    hour = 12 if x < 55 else 17
    hour += choice([0] * 30 + [1] * 20 + [-1] * 20 + [2] * 15 + [-2] * 15) # Pick randomly from weighted list.
    minute = randint(0, 59)
    second = randint(0, 59)
    return datetime(year, month, day, hour, minute, second)

def generate_emotion() -> str:
    x = randint(0, 100)
    if x < 80:
        return "neutral"
    if x < 90:
        return "sadness"
    else:
        return "happiness"

# # # End Helper methods # # #

def generate_people(people_per_day: int) -> [Person]:
    ''' Generate people across a span of time. The for loops loop through dates, and the helper methods handle the
    person creation. NOTE: DAYS only go up to 28. NOTE #2: Because the helpers do not account for date,
    there will probably not be trends across time.'''
    people = []
    for year in YEARS:
        for month in MONTHS:
            for day in DAYS:
                for _ in range(people_per_day + randint(-10,10)):
                    people.append(Person(generate_age(), generate_gender(),
                                         generate_duration(), generate_logs(year, month, day)))
    return people