#%%
import csv
import random
import ast

#%%
path = "Data/Digg/"
#path = "Data/Flixster/"
seeders_file = "random_seeders.csv"
#seeders_file = "top_seeders.csv"
suffix = "_random_diverse"
#advertisers_file = 'advertisers.csv'
advertisers_file = 'advertisers_diverse.csv'
ad_start = 0
seeder_start = 0
iterations = 10

#%%
tic_dict = {}
with open(path + 'edgesWithTIC.csv', 'r') as tic_file:
    tic_reader = csv.reader(tic_file, delimiter=',')
    next(tic_reader, None)  # skip the headers

    for row in tic_reader: 
        node1 = row[0]
        node2 = row[1]
        distribution = ast.literal_eval(row[2])
        if node1 in tic_dict:
            tic_dict[node1].append([node2, distribution])
        else:
            tic_dict[node1] = [[node2, distribution]]

print("Edges loaded.")

#%%
seeders_list = []
with open(path + seeders_file, 'r') as seeders_file:
    seeders_reader = csv.reader(seeders_file, delimiter=',')

    for row in seeders_reader: 
        seeders_list.append(row[0])

print("Nodes loaded.")

#%%
ad_list = []
with open(path + advertisers_file, 'r') as ad_file:
    ad_reader = csv.reader(ad_file, delimiter=',')

    for row in ad_reader:
        ad_list.append(row)

print("Ads loaded.")

#%%
def getInfluence(start_node, topic_dist):
    count = 0
    visited = set()
    visited.add(start_node)
    fringe = [start_node]

    while fringe:
        current_fringe = fringe
        fringe = []

        for node in current_fringe:

            if str(node) in tic_dict:

                for target_list in tic_dict[str(node)]:
                    target_node = target_list[0]
                    target_probabilities = target_list[1]

                    if target_node not in visited:
                        dice = random.random()
                        
                        probability = sum([float(topic_dist[i]) * float(target_probabilities[i]) for i in range(len(topic_dist))])

                        if dice <= probability:
                            fringe.append(target_node)
                            count += 1

                        visited.add(target_node)

    return count

#%%

with open(path + 'influence_' + str(iterations) + '_iterations' + suffix + '.csv', 'a', newline='') as influence_file:
    influence_writer = csv.writer(influence_file, delimiter=',')

    for index in range(ad_start, len(ad_list)):

        topic_dist = ad_list[index]
    
        for seeder in seeders_list[seeder_start:]:

            total = 0
            for i in range(iterations):
                total += getInfluence(seeder, topic_dist)

            count = total * 1.0 / iterations

            influence_writer.writerow([index, seeder, count])
            influence_file.flush()

        seeder_start = 0

print("Done.")
