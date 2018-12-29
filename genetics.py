# https://www.youtube.com/watch?v=XP8R0yzAbdo - example of genetic algorithm

import random
import copy
from Instance import Instance

# Default parameters
from problem_manager import calc_result

MAX_GENERATIONS = 50    # Index of last generation
CONSTANT_MEMBERS = 0.1  # Percentage of members copied directly to new generation (no crossover)
POPULATION_SIZE = 50  # Number of members in a generation
CROSSOVER_CHANCE = 0.5  # Chance for cross two members instead of just copy one of them to next generation
MUTATION_CHANCE = 0.2  # Chance for mutate child

# Mutation parameters
SWAP_ELEMENT_CHANCE = 0.1  # Chance to swap the job
CHANGE_R_CHANCE = 0.2  # Chance to change R position

# Crossover parameters


def start(inst):
    population = generate_first_population(inst, POPULATION_SIZE)

    # first population is not sorted and calculated. Same thing is in next_generation function.
    for inst in population:
        calc_result(inst)
    population.sort(key=lambda instance: instance.f, reverse=False)

    for i in range(MAX_GENERATIONS):
        population = next_generation(population)

    best_member = population[0]
    return best_member


# Create child C from members A and B
def crossover(inst_a, inst_b):
    start_index = random.randint(0, int(inst_a.n / 2))  # Start coping from this element of A
    end_index = random.randint(int(inst_a.n / 2), inst_a.n - 1)  # End coping on this element of A

    # todo: tak to powinno być inicjalizowane, zamiast kopiowania z A, ale trzeba obliczyć parametry (p, r itd.)
    # inst_c = Instance()
    inst_c = copy.deepcopy(inst_a)

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
                for j in range(len(inst_c.jobs)):   # todo: optimize
                    if inst_c.jobs[j] is None:
                        inst_c.jobs[j] = job  # Put element from B to the first available position of C
                        not_assigned_jobs.remove(job.id)
                        break
    return inst_c


# Swap jobs and move R position with preset probability
def mutate(inst, swap_chance=SWAP_ELEMENT_CHANCE, change_r_chance=CHANGE_R_CHANCE):
    # Swap elements
    fist_job_idx = None  # one of the jobs to swap
    for i in range(0, len(inst.jobs)):
        if random.uniform(0, 1) <= swap_chance:
            # swap two jobs
            if fist_job_idx is None:
                fist_job_idx = i
            else:
                inst.jobs[fist_job_idx], inst.jobs[i] = inst.jobs[i], inst.jobs[fist_job_idx]
                fist_job_idx = None

    # Change R position
    if random.uniform(0, 1) <= change_r_chance:
        # move jobs block
        inst.r += random.randint(-inst.r, int(inst.d * inst.h))
    return inst


# Select members for new population. It's random with higher chance for better members.
# Probability to pick member is 1 - place/size
def next_generation(population):
    population.sort(key=lambda instance: instance.f, reverse=False)
    next_gen = []
    inst_a = None

    for i in range(int(len(population)*CONSTANT_MEMBERS)):
        next_gen.append(copy.deepcopy(population[i]))
    while len(next_gen) < POPULATION_SIZE:
        for inst in population:
            if random.uniform(0, 1) <= CROSSOVER_CHANCE:
                if inst_a is None:
                    inst_a = inst
                else:
                    inst_c = crossover(inst_a, inst)
                    next_gen.append(inst_c)
                    inst_a = None
                    if len(next_gen) == POPULATION_SIZE:
                        break

    for inst in next_gen:
        if inst is None:
            print("a")
        calc_result(inst)
    next_gen.sort(key=lambda instance: instance.f, reverse=False)
    return next_gen


def generate_first_population(inst, count):
    population = []
    for i in range(count):
        instance = copy.deepcopy(inst)
        population.append(mutate(instance, 0.7, 0.3))
    return population
