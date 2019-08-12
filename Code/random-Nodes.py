#%%
import csv
import random

#%%
path = "Data/Digg/"
k = 50


seeder_set = set()
with open(path + 'edgesWithTiC.csv', 'r') as tic_file:
    tic_reader = csv.reader(tic_file, delimiter=',')

    for row in tic_reader: 
        node = row[0]

        seeder_set.add(node)

all_seeders_list = list(seeder_set)

seeders_list = []
while len(seeders_list) < 50:
    seeder = random.choice(all_seeders_list)
    seeders_list.append(seeder)

#%%

with open(path + 'random_seeders.csv', 'a') as seeders_file:
    
    for seeder in seeders_list:

        seeders_file.write(seeder + '\n')

