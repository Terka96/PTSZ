# https://www.youtube.com/watch?v=XP8R0yzAbdo - example of genetic algorithm

import random
import copy
import time
import itertools

# Default parameters
from calculator import calc_result

MAX_GENERATIONS = 100000    # Index of last generation
CONSTANT_MEMBERS = 0.3  # Percentage of members copied directly to new generation (no crossover)
POPULATION_SIZE = 50  # Number of members in a generation
CROSSOVER_CHANCE = 0.2  # Chance for cross two members instead of just copy one of them to next generation
MUTATION_CHANCE = 0.9  # Chance for mutate child

# Mutation parameters
SWAP_ELEMENT_CHANCE = 0.3  # Chance to swap the job
CHANGE_R_CHANCE = 0.1  # Chance to change R position

DEBUG = False

# Crossover parameters


class Genetics:
    def __init__(self, max_gen=MAX_GENERATIONS, const_memb=CONSTANT_MEMBERS, pop_size=POPULATION_SIZE, cross_chance=CROSSOVER_CHANCE, mut_chance=MUTATION_CHANCE,
                 swap_el_chance=SWAP_ELEMENT_CHANCE, change_r_chance=CHANGE_R_CHANCE):
        self.MAX_GENERATIONS = max_gen
        self.CONSTANT_MEMBERS = const_memb
        self.POPULATION_SIZE = pop_size
        self.CROSSOVER_CHANCE = cross_chance
        self.MUTATION_CHANCE = mut_chance
        self.SWAP_ELEMENT_CHANCE = swap_el_chance
        self.CHANGE_R_CHANCE = change_r_chance

    def start(self, inst, max_proc_time=0):
        start_time = time.time()

        population = self.generate_first_population(inst, self.POPULATION_SIZE)

        # first population is not sorted and calculated. Same thing is in next_generation function.
        for inst in population:
            calc_result(inst)
        population.sort(key=lambda instance: instance.f, reverse=False)

        self.debug("Init time: {0}".format(time.time() - start_time))

        for i in range(self.MAX_GENERATIONS):
            population = self.next_generation(population)
            if time.time() - start_time > max_proc_time > 0:
                print("GEN.{1}: Wykorzystano czas dla przetwarzania danej instancji ({0:.2f}s)".format(max_proc_time, i))
                break
        best_member = population[0]
        return best_member

    # Create child C from members A and B
    def crossover(self, inst_a, inst_b):
        # start_time = time.time()
        start_index = random.randint(0, int(inst_a.n / 2))  # Start coping from this element of A
        end_index = random.randint(int(inst_a.n / 2), inst_a.n - 1)  # End coping on this element of A

        # todo: tak to powinno być inicjalizowane, zamiast kopiowania z A, ale trzeba obliczyć parametry (p, r itd.)
        # inst_c = Instance()
        inst_c = copy.deepcopy(inst_a)
        # self.debug(":::PART1: {0}".format(time.time() - start_time))
        # start_time = time.time()

        not_assigned_jobs = list(range(inst_a.n))  # Jobs not assigned to C

        # 1. Copy from A
        inst_c.jobs = copy.deepcopy(inst_a.jobs)

        inst_c.jobs[0:start_index] = itertools.repeat(None, start_index)
        # for i in range(0, start_index):
        #     inst_c.jobs[:start_index] = None
        # for i in range(end_index, inst_a.n):
        #     inst_c.jobs[i] = None
        inst_c.jobs[end_index:len(inst_c.jobs)] = itertools.repeat(None, (len(inst_c.jobs) - end_index))

        # self.debug(":::PART2: {0}".format(time.time() - start_time))
        # start_time = time.time()
        # inst_c.jobs[:start_index] = None * start_index    # error
        # inst_c.jobs[end_index:] = None * (inst_a.n - end_index)   error

        # Remember assigned jobs (remove them from not_assigned list)
        for i in range(start_index, end_index):
            not_assigned_jobs.remove(inst_c.jobs[i].id)

        # self.debug(":::PART3: {0}".format(time.time() - start_time))
        # start_time = time.time()
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
        # self.debug(":::PART4: {0}".format(time.time() - start_time))
        # start_time = time.time()
        return inst_c

    # Swap jobs and move R position with preset probability
    def mutate(self, inst, swap_chance=None, change_r_chance=None):
        swap_chance = self.SWAP_ELEMENT_CHANCE if swap_chance is None else swap_chance
        change_r_chance = self.CHANGE_R_CHANCE if change_r_chance is None else change_r_chance
        # Swap elements
        fist_job_idx = None  # one of the jobs to swap
        start_int = (random.randint(0, len(inst.jobs)-2))
        end_int = (random.randint(start_int, len(inst.jobs)))
        for i in range(start_int, end_int):
            if random.uniform(0, 1) <= swap_chance:
                # swap two jobs
                if fist_job_idx is None:
                    fist_job_idx = i
                else:
                    # if (inst.jobs[fist_job_idx].a < inst.jobs[fist_job_idx].b) == (inst.jobs[i].a < inst.jobs[i].b):
                    inst.jobs[fist_job_idx], inst.jobs[i] = inst.jobs[i], inst.jobs[fist_job_idx]
                    fist_job_idx = None

        # Change R position
        if random.uniform(0, 1) <= change_r_chance:
            # move jobs block
            inst.r += random.randint(-inst.r, int((inst.d * inst.h)/10))
        return inst

    # Select members for new population. It's random with higher chance for better members.
    # Probability to pick member is 1 - place/size
    def next_generation(self, population):
        population.sort(key=lambda instance: instance.f, reverse=False)
        next_gen = []
        inst_a = None

        start_time = time.time()
        for i in range(int(len(population)*self.CONSTANT_MEMBERS)):
            next_gen.append(copy.deepcopy(population[i]))
        while len(next_gen) < self.POPULATION_SIZE:
            for inst in population:
                if random.uniform(0, 1) <= self.CROSSOVER_CHANCE:
                    if inst_a is None:
                        inst_a = inst
                    else:
                        inst_c = self.crossover(inst_a, inst)
                        next_gen.append(inst_c)
                        inst_a = None
                        if len(next_gen) == self.POPULATION_SIZE:
                            break
                else:
                    next_gen.append(inst)
        self.debug("Filling population: {0}".format(time.time() - start_time))

        # Mutate
        start_time = time.time()
        for i in range(len(next_gen)):
            if random.uniform(0, 1) <= self.MUTATION_CHANCE:
                next_gen[i] = self.mutate(next_gen[i], self.SWAP_ELEMENT_CHANCE,  self.CHANGE_R_CHANCE)

        for inst in next_gen:
            calc_result(inst)
        next_gen.sort(key=lambda instance: instance.f, reverse=False)
        self.debug("Mutationse: {0}\n".format(time.time() - start_time))

        return next_gen

    def generate_first_population(self, inst, count):
        population = []
        for i in range(count):
            instance = copy.deepcopy(inst)
            population.append(self.mutate(instance, 1, 0.3))
        return population

    def debug(self, msg):
        if DEBUG == True:
            print(msg)
