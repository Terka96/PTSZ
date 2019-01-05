import numpy

import problem_manager

#todo: generowanie list

MAX_GENERATIONS = [3]    #numpy.arange(5, 10, 1)    # Index of last generation
POPULATION_SIZE = [50]  #numpy.arange(20, 50, 10)   # Number of members in a generation

CONSTANT_MEMBERS = numpy.arange(0.1, 0.9, 0.3)
CROSSOVER_CHANCE = numpy.arange(0.1, 0.9, 0.3)  # Chance for cross two members instead of just copy one of them to next generation
MUTATION_CHANCE = numpy.arange(0.1, 0.9, 0.3)  # Chance for mutate child

# Mutation parameters
SWAP_ELEMENT_CHANCE = numpy.arange(0.1, 0.9, 0.3)  # Chance to swap the job
CHANGE_R_CHANCE = numpy.arange(0.1, 0.9, 0.3)  # Chance to change R position

iterations = len(MAX_GENERATIONS) * len(CONSTANT_MEMBERS) * len(POPULATION_SIZE) * len(CROSSOVER_CHANCE) * len(MUTATION_CHANCE) * len(SWAP_ELEMENT_CHANCE) * len(CHANGE_R_CHANCE)

ATTEMPTS = 5

iter = 0
#todo: wyniki muszą pochodzić z kilku pomiarów i być uśredniane
for s in [10, 50, 100, 200]: #, 20, 50, 100, 200, 500, 1000]:
    for max_gen in MAX_GENERATIONS:
        for pop_size in POPULATION_SIZE:
            for const_mem in CONSTANT_MEMBERS:
                for cross_cha in CROSSOVER_CHANCE:
                    for mut_cha in MUTATION_CHANCE:
                        for swap_cha in SWAP_ELEMENT_CHANCE:
                            for change_cha in CHANGE_R_CHANCE:
                                instances_to_save = []
                                iter += 1
                                print("{0}/{1}".format(iter, iterations))
                                # todo: pasek postępu
                                for x in range(ATTEMPTS):
                                    instances = problem_manager.read(s)
                                    for i in range(len(instances)):
                                        instances[i] = problem_manager.custom_schedule(instances[i], True, max_gen, const_mem, pop_size, cross_cha, mut_cha, swap_cha, change_cha)
                                        instances_to_save.append(instances[i])
                                problem_manager.export_tuner(instances_to_save, ATTEMPTS, max_gen, const_mem, pop_size, cross_cha, mut_cha, swap_cha, change_cha)
