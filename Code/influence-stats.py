#%%
import csv
import sys

#%%
filenames = ["Data/Flixster/influence_10_iterations_top.csv",
             "Data/Flixster/influence_10_iterations_top_diverse.csv",
             "Data/Flixster/influence_10_iterations_random.csv",
             "Data/Flixster/influence_10_iterations_random_diverse.csv",
             "Data/Digg/influence_10_iterations_top.csv",
             "Data/Digg/influence_10_iterations_top_diverse.csv",
             "Data/Digg/influence_10_iterations_random.csv",
             "Data/Digg/influence_10_iterations_random_diverse.csv"]

#%%
for filename in filenames:
    with open(filename) as input_file:
        input_reader = csv.reader(input_file, delimiter=',')

        sum = 0
        count = 0
        min = sys.float_info.max
        max = 0

        for row in input_reader:
            spread = float(row[2])
            sum += spread
            count += 1
            if spread < min:
                min = spread
            if spread > max:
                max = spread

        print(filename)
        print("average: " + str(sum/count))
        print("min: " + str(min))
        print("max: " + str(max))