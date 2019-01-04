import numpy

import problem_manager

#todo: generowanie list

MAX_GENERATIONS = [5, 6]     #numpy.arange(5, 10, 1)    # Index of last generation
CONSTANT_MEMBERS = [0.3, 0.4]   #numpy.arange(0, 0.9, 0.1)
POPULATION_SIZE = [20, 30] #numpy.arange(20, 50, 10)   # Number of members in a generation
CROSSOVER_CHANCE = [0.3, 0.4] #numpy.arange(0.3, 0.7, 0.1)  # Chance for cross two members instead of just copy one of them to next generation
MUTATION_CHANCE = [0.3, 0.4] #numpy.arange(0.1, 0.4, 0.1)  # Chance for mutate child

# Mutation parameters
SWAP_ELEMENT_CHANCE = [0.1, 0.2] #numpy.arange(0.1, 0.3, 0.1)  # Chance to swap the job
CHANGE_R_CHANCE = [0.2, 0.3] #numpy.arange(0.2, 0.4, 0.1)  # Chance to change R position

ATTEMPTS = 10

#todo: wyniki muszą pochodzić z kilku pomiarów i być uśredniane
for s in [10]: #, 20, 50, 100, 200, 500, 1000]:
    for max_gen in MAX_GENERATIONS:
        for const_mem in CONSTANT_MEMBERS:
            for pop_size in POPULATION_SIZE:
                for cross_cha in CROSSOVER_CHANCE:
                    for mut_cha in MUTATION_CHANCE:
                        for swap_cha in SWAP_ELEMENT_CHANCE:
                            for change_cha in CHANGE_R_CHANCE:
                                instances_to_save = []
                                # todo: pasek postępu
                                for x in range(ATTEMPTS):
                                    instances = problem_manager.read(s)
                                    for i in range(len(instances)):
                                        instances[i] = problem_manager.custom_schedule(instances[i], True, max_gen, const_mem, pop_size, cross_cha, mut_cha, swap_cha, change_cha)
                                        instances_to_save.append(instances[i])
                                problem_manager.export_tuner(instances_to_save, ATTEMPTS, max_gen, const_mem, pop_size, cross_cha, mut_cha, swap_cha, change_cha)
