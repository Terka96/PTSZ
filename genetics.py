# https://www.youtube.com/watch?v=XP8R0yzAbdo - example of genetic algorithm

import random
import copy
from Instance import Instance

# Default parameters
POPULATION_SIZE = 10  # Number of members in a generation
CROSSOVER_CHANCE = 0.3  # Chance for cross two members instead of just copy one of them to next generation
MUTATION_CHANCE = 0.1  # Chance for mutate child

# Mutation parameters
MUTATE_ELEMENT_CHANCE = 0.05  # Chance to mutate the element


# Crossover parameters


# Create child C from members A and B
def crossover(inst_a, inst_b):
    start_index = random.randint(0, int(inst_a.n / 2))  # Start coping from this element of A
    end_index = random.randint(int(inst_a.n / 2), inst_a.n - 1)  # End coping on this element of A

    inst_c = Instance()

    not_assigned_jobs = list(range(inst_a.n))  # Jobs not assigned to C

    # 1. Copy from A
    inst_c.jobs = copy.deepcopy(inst_a.jobs)

    for i in range(0, start_index):
        inst_c.jobs[i] = None
    for i in range(end_index, inst_a.n):
        inst_c.jobs[i] = None

    # inst_c.jobs[:start_index] = None * start_index    # error
    # inst_c.jobs[end_index:] = None * (inst_a.n - end_index)   error

    # Remember assigned jobs (remove them from not_assigned list)
    for i in range(start_index, end_index):
        not_assigned_jobs.remove(inst_c.jobs[i].id)

    # 2. Fill with B
    for i in range(0, inst_b.n):
        job = copy.deepcopy(inst_b.jobs[i])
        if job.id in not_assigned_jobs:
            if inst_c.jobs[i] is None:  # Put element from B at the same place to C
                inst_c.jobs[i] = job
                not_assigned_jobs.remove(job.id)
            else:
                inst_c.jobs[not_assigned_jobs[0]] = job     # Put element from B to the first available position of C
                not_assigned_jobs.pop(0)

    return inst_c


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
