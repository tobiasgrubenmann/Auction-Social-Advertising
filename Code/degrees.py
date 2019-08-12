#%%
import csv

#%%
path = "Data/Digg/"
k = 50

#%%
def second(elem):
    return elem[1]

seeder_dict = {}
with open(path + 'edgesWithTiC.csv', 'r') as tic_file:
    tic_reader = csv.reader(tic_file, delimiter=',')

    for row in tic_reader: 
        node1 = row[0]

        if node1 in seeder_dict:
            seeder_dict[node1] += 1
        else:
            seeder_dict[node1] = 1

seeder_degree_list = []
for key, value in seeder_dict.items():
    seeder_degree_list.append([key,value])

seeder_degree_list.sort(key=second, reverse=True)

#%%

with open(path + 'degrees.csv', 'a') as seeders_file:
    
    for pair in seeder_degree_list:

        seeders_file.write(pair[0] + ',' + str(pair[1]) + '\n')

