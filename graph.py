'''
This file is responsible for handling the input given from server.py to create a graph and save on the output.png file.
4 plotting functions, a helper, and then the update_png


'''

import pandas
import seaborn
from generate import Person
from generate import generate_people
from generate import MONTHS
from generate import YEARS

# # # Begin plotting methods # # #
'''
All plotting functions follow a similar pattern.
    1. Make a container(s)
    2. Do some counting with loops and if statements to fill container with graphing data
    3. Pass the container to seaborn for graphing

All plotting functions have the line "if not constraints or constraints(p) appears in all of the plotters.
   This evaluates to True if either:
      1. constraints is None or False. This happens when the user types nothing into the text field.
      2. constraints was constructed correctly and the person passes the test.

All plotting functions EXCEPT FOR HEATMAP pass data to seaborn in the same way:
    the x and y parameters specify where to look in the data parameters.
    Example: pass in a DataFrame (i.e. data=df). Saying "x=Age" will end up using df["Age"]

    For heatmaps, just pass in the DataFrame. All of the data is used in it's existin format so
    no specifying is necessary.
'''

def barplot(sample: [Person], hours: range, axis, constraints: callable) -> None:
    try:
        counts = {hour : 0 for hour in hours}

        sorted_sample = sorted(sample[:100], key=lambda x: x.hour) # Will error if len(sample) < 100

        for hour in hours:
            for p in sorted_sample:
                if p.hour == hour:
                    if not constraints or constraints(p):
                        counts[hour] += 1
                elif p.hour > hour:
                    break # Avoid unnecessary computation because we sorted.

        df = pandas.DataFrame({"Counts": counts})
        seaborn.barplot(x=df.index, y="Counts", data=df, ax=axis)
    except Exception as ex:
        print(ex)
        print("Invalid syntax")

def comparative_bar_plot(sample: [Person], hours: range, axis, constraints: callable) -> None:
    ''' Comparative barplot of males vs. females at times of day '''
    try:

        male_hour_counts = {i : 0 for i in hours}
        female_hour_counts = {i : 0 for i in hours}

        for i in hours:
            for p in sample[:100]: # Just take first 100
                if p.hour == i:
                    if not constraints or constraints(p):
                        if p.gender == "male":
                            male_hour_counts[i] += 1
                        elif p.gender == "female":
                            female_hour_counts[i] += 1

        df = pandas.DataFrame({"Male": male_hour_counts, "Female" : female_hour_counts})

        # Reformat DataFrame
        df = df.stack().reset_index()
        df.columns = ["x", "hue", "y"]

        # the hue column and keyword lets seaborn color code the graph, allowing for side by side comparison
        seaborn.barplot(x="x", y="y", hue="hue", data=df, ax=axis)
    except Exception as ex:
        print(ex)
        print("Invalid syntax")

def heatmap_visits(people: [Person], years: range, axis, constraints: callable) -> None:
    ''' Generates a DataFrame containing number of visits per month for the years'''
    try:
        table = pandas.DataFrame()
        month_str = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
                     7: "July", 8: "August", 9: "September", 10: "October", 11: "November",  12: "December"}

        sorted_people = pandas.Series(sorted(people, key=lambda x: (x.date.year, x.date.month)))

        for year in years:
            counts = {}
            for month in MONTHS:
                for p in sorted_people:
                    if p.date.year == year:
                        if p.date.month == month:
                            if not constraints or constraints(p):
                                if month_str[month] in counts:
                                    counts[month_str[month]] += 1
                                else:
                                    counts[month_str[month]] = 1
                    elif p.date.year > year:  # People are sorted by year. Save computations by not checking everyone
                        break

            table[year] = pandas.Series(counts)

        seaborn.heatmap(data=table, annot=True, fmt="d", ax=axis)
    except Exception as ex:
        print(ex)
        print("Invalid syntax")

def duration_scatterplot(people: [Person], axis, constraints: callable) -> None:
    # Age vs. duration
    try:
        people = people[:150]
        ages = []
        duration = []
        for p in people:
            if not constraints or constraints(p):
                ages.append(p.age)
                duration.append(p.duration)

        table = pandas.DataFrame()
        table["Age"] = pandas.Series(ages)
        table["Duration"] = pandas.Series(duration)
        seaborn.regplot(x="Age", y="Duration", data=table, ax=axis)
    except Exception as ex:
        print(ex)
        print("Invalid syntax")

# # # End plotting methods # # #

def make_constraints(user_input: str, sample_person: Person) -> callable:
    # Attempt to turn user input from text field into a function.
    # This function is used to filter people in the plotting method.
    try:
        test = lambda x: eval("x." + user_input)
        test(sample_person) # If this doesn't raise an error, the function is valid.
        return test
    except:
        return None

def update_png(type_of_graph, constraints):
    # Ideally, don't remake the sample every time. This is a waste of computation.
    # To solve, wrap everything in this file in a class and make the sample an object attribute.
    # Did not do this because I wanted to keep the code minimal.
    sample = generate_people(people_per_day=10)

    constraints = make_constraints(constraints, sample[0])

    # Creates window/axis on which to plot on
    fig, ax = seaborn.plt.subplots()

    if type_of_graph is not None:

        if type_of_graph == "barplot":
            barplot(sample, range(10, 20), ax, constraints)

        elif type_of_graph == "comparative_barplot":
            comparative_bar_plot(sample, range(10, 20), ax, constraints)

        elif type_of_graph == "heatmap_visits":
            heatmap_visits(sample, YEARS, ax, constraints)

        elif type_of_graph == "regplot_duration":
            duration_scatterplot(sample, ax, constraints) # jointplot automatically brings up its own window/chart?

        # Overwrite the existing file. On next webpage refresh, the new chart should show.
        fig.savefig("static/output.png")

        print(" \n Update output complete! \n")