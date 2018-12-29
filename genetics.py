# https://www.youtube.com/watch?v=XP8R0yzAbdo - example of genetic algorithm

import random
import copy

# Default parameters
POPULATION_SIZE = 10    # Number of members in a generation
CROSSOVER_CHANCE = 0.3  # Chance for cross two members instead of just copy one of them to next generation
MUTATION_CHANCE = 0.1   # Chance for mutate child


# Create child C from members A and B
def crossover():
    # todo: implement
    return None


def mutate(inst):
    if random.randrange(10) > 4:
        # swap two jobs
        swap1 = random.randint(0, inst.n - 1)
        swap2 = random.randint(0, inst.n - 1)
        inst.jobs[swap1], inst.jobs[swap2] = inst.jobs[swap2], inst.jobs[swap1]
    else:
        # move jobs block
        inst.r += random.randint(-inst.r, inst.d * inst.h)


# Select members for new population. It's random with higher chance for better members.
# Probability to pick member is 1 - place/size
def choose_next_generation():
    # todo implement
    return None


def generate_first_population(inst, count):
    population = []
    for i in range(count):
        population.append(mutate(copy.deepcopy(inst)))
    return population
