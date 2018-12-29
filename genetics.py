import random
import copy


def mutate(inst):
    if random.randrange(10) > 4:
        # swap two jobs
        swap1 = random.randint(0, inst.n - 1)
        swap2 = random.randint(0, inst.n - 1)
        inst.jobs[swap1], inst.jobs[swap2] = inst.jobs[swap2], inst.jobs[swap1]
    else:
        # move jobs block
        inst.r += random.randint(-inst.r, inst.d * inst.h)


def generate_first_population(inst, count):
    population = []
    for i in range(count):
        population.append(mutate(copy.deepcopy(inst)))
    return population
