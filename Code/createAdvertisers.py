#%%
import csv
import random

#%%
# parameters
number_of_advertisers = 100
number_of_topics = 20
choose = 20
random_dampening_factor = True
advertiser_file_name = 'advertisers_diverse.csv'
path = 'Data/Digg/'

#%%
with open(path + advertiser_file_name, 'w', newline='') as advertiser_file:

    advertiser_writer = csv.writer(advertiser_file, delimiter=',')
    
    for i in range(number_of_advertisers):
        topic_dist = []
        total = 0

        shuffle_list = list(range(number_of_topics))
        random.shuffle(shuffle_list)
        chosen_topics = [shuffle_list[i] for i in range(choose)]

        for j in range(number_of_topics):

            if j in chosen_topics:

                random_value = random.random()
                topic_dist.append(random_value)
                total += random_value
            
            else:
                topic_dist.append(0)

        dampening_factor = 1.0
        if random_dampening_factor:
            dampening_factor = random.random()

        for j in range(number_of_topics):
            topic_dist[j] /= total/dampening_factor

        advertiser_writer.writerow(topic_dist)



