import matplotlib.pyplot as plt
from random import *
from numpy import *
import numpy as np
import sys

# zombies can not die of natural causes
# zombies can die only if they are killed by humans
# humans start at 1000
# zombies start at 1



h_birthrate =0.001 # human birth rate
initial_interaction = 0.001; # predator-prey interaction
interaction = initial_interaction
# z_reproduction = 0.5; # zombie reproduction rate
# z_deathrate = 0.0 # zombie death rate
z_conversion = 0.8 # conversion rate of humans to zombies
chaos_at_start = 10 # zombies dont die first 10 days
dt = 0.01; # time step
max_time = 3600 # number of days

# initial time and populations
t = 0; 
human_pop = 1000; # humans x
zombie_pop = 1;  # zombies y

# empty lists in which to store time and populations
t_list = []; x_list = []; y_list = []

# initialize lists
t_list.append(t); x_list.append(human_pop); y_list.append(zombie_pop)

# Function to determine survivability based on the ratio of humans to zombies
# def calculate_survivability(human_pop, zombie_pop):
#     if human_pop >= zombie_pop:
#         return 0.5  # No increased survivability when humans outnumber zombies
    
#     ratio = human_pop / zombie_pop
#     percentage = ratio * 100

#     # Survivability increases as the ratio decreases (less humans compared to zombies)
#     if percentage >= 90:
#         return 0.52
#     elif percentage >= 80:
#         return 0.54
#     if percentage >= 70:
#         return 0.56
#     elif percentage >= 60:
#         return 0.58
#     elif percentage >= 50:
#         return 0.60
#     elif percentage >= 40:
#         return 0.62
#     elif percentage >= 30:
#         return 0.64
#     elif percentage >= 20:
#         return 0.66
#     elif percentage >= 10:
#         return 0.68
#     else:
#         return 1.0  # Max survivability when there are very few humans compared to zombies

def calculate_survivability(human_pop, zombie_pop):
    if zombie_pop == 0:
        return 0  # No zombies, no increased survivability needed

    ratio = human_pop / zombie_pop

    # Survivability increases when humans are outnumbered, and decreases when they outnumber zombies
    # If the ratio is less than 1 (more zombies), survivability increases as it gets smaller
    if ratio < 1:
        survivability = 1 - ratio  # The smaller the ratio, the higher the survivability
    else:
        survivability =  1 - (ratio - 1) / 10  # If humans outnumber zombies, survivability goes down gradually

    return survivability  # Clamp between 0 and 1

# func for human-zombie interaction
# takes in human and zombie population
# 
def hzInteraction(human_pop, interaction, zombie_pop, survivabitlity):
    
    h_popInc = h_birthrate*human_pop
    zombieHumaninteractions = interaction*human_pop*zombie_pop
    
    h_popDec = zombieHumaninteractions * (1 - survivability); # 40 percent of interactions result in survival
    z_popInc = h_popDec * z_conversion; # 50 percent of interactions result in conversion, 10 % die
    
    
    dHpop = h_popInc - h_popDec
    dZpop = z_popInc - zombieHumaninteractions*0.01 # mult by chance of conversion later.. +- zombies killed
    
        
    return [dHpop, dZpop]
    # increase zombie death rate for every iteration
    
 

while t < max_time:
    
    # Reduce interaction rate further if chaos period is reached
    if t < chaos_at_start:
        interaction = np.minimum(interaction, 0.01)  # Interaction rate is capped during the chaos period
    
    
    # # Adjust the interaction rate dynamically based on the current population sizes
    # if human_pop < zombie_pop:
    #     interaction = interaction * 0.1  # If zombies outnumber humans, decrease the interaction rate
    # else:
    #     interaction = initial_interaction * 1.1  # Otherwise, use the initial interaction rate
    
    # Calculate survivability based on human-zombie ratio
    survivability = calculate_survivability(human_pop, zombie_pop)
    
    
    calculatedPop = hzInteraction(human_pop, interaction, zombie_pop, survivability)
    human_pop = human_pop + (calculatedPop[0])*dt
    zombie_pop = zombie_pop + (calculatedPop[1])*dt
    
    
    # Ensure populations don't go negative
    human_pop = max(human_pop, 0)
    zombie_pop = max(zombie_pop, 0)
    
    # calc new values for t, x, y
    t = t + dt

    # store new values in lists
    t_list.append(t)
    x_list.append(human_pop)
    y_list.append(zombie_pop)
       
    
plt.plot(t_list, x_list, 'g', label='Humans', linewidth=2)
plt.plot(t_list, y_list, 'r', label='Zombies', linewidth=2)
plt.xlabel('Days')
plt.ylabel('Population')
plt.legend()
plt.title('Human vs. Zombie Population Dynamics')
plt.show()