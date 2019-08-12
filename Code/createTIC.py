#%%
import csv
import random

#%%
# parameters
number_of_topics = 10
path = 'Data/Flixster/'

#%%
#Get probability distribtion
distribution_list = []
with open(path + 'distribution.csv', 'r') as dist_file:
    dist_reader = csv.reader(dist_file, delimiter=',')
    next(dist_reader, None)  # skip the headers
    for row in dist_reader:
        if len(row) > 1:
            distribution_list.append([row[0], row[1]])

#%%
with open(path + 'edges.csv', 'r') as edges_file:
    with open(path + 'edgesWithTIC.csv', 'w', newline='') as tic_file:
        edges_reader = csv.reader(edges_file, delimiter=',')
        tic_writer = csv.writer(tic_file, delimiter=',')

        #header
        tic_writer.writerow(["node 1", "node 2", "topic probabilities"])

        for row in edges_reader:
            if len(row) > 1:

                probabilities = []

                for _ in range(number_of_topics):

                    #Get probability from distribution
                    probability = 0
                    random_number = random.random()
                    index = 0
                    while float(distribution_list[index][1]) < random_number:
                        index += 1
                    if index < len(distribution_list):
                        lower_bound = 0
                        if index > 0:
                            lower_bound = float(distribution_list[index-1][0])
                        upper_bound = float(distribution_list[index][0])
                        probability = lower_bound + random.random() * (upper_bound - lower_bound)

                    probabilities += [probability]

                tic_writer.writerow(row + [probabilities])


#%%
print(distribution_list)