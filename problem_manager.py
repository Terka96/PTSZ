import os
import sys
from timeit import default_timer as timer

import genetics
from Instance import Instance
from Job import Job
from calculator import calc_result


def read(size):
    problem_id = 0
    jobs_n = 0
    jobs_left = 0
    instances = []
    inst = 0

    handle = open("data/sch" + str(size) + ".txt", "r")
    for line in handle.readlines():
        if inst == 0:
            inst = Instance(0, 0, 0, 0, 0, 0, [])
        elif jobs_left == 0:
            inst = Instance(0, 0, 0, 0, 0, 0, [])
            inst.jobs = []
            inst.k = problem_id + 1
            inst.n = size
            jobs_n = int(line)
            jobs_left = jobs_n
        else:
            line = [int(s) for s in line.split()]
            j = Job()
            j.id = jobs_n - jobs_left
            j.p = line[0]  # czas
            j.a = line[1]  # kara za szybko
            j.b = line[2]  # kara za późno
            inst.d += j.p
            inst.jobs.append(j)
            jobs_left -= 1
            if jobs_left == 0:
                for h in [0.2, 0.4, 0.6, 0.8]:
                    instances.append(Instance(inst.n, inst.k, h, inst.d, inst.r, inst.f, inst.jobs))
                problem_id += 1
    handle.close()
    return instances


def custom_schedule(inst, custom_params=True, max_proc_time=0, max_gen=None, const_memb=None, pop_size=None, cross_chance=None,
                    mut_chance=None, swap_el_chance=None, change_r_chance=None):
    start = timer()
    for j in inst.jobs:
        j.w = (-j.a + j.b) * j.p
    inst.jobs = sorted(inst.jobs, key=lambda j: j.w, reverse=True)
    dd = int(inst.d * inst.h)
    t = 0
    center = 0
    weights = 0
    for j in inst.jobs:
        t += j.p
        w = abs(j.w)
        weights += w
        center += t * w
    center = int(center / weights)
    inst.r = max(0, dd - center)
    # liczenie kary
    calc_result(inst)

    # Use genetic algorithm
    genetic = genetics.Genetics(max_gen, const_memb, pop_size, cross_chance, mut_chance, swap_el_chance,
                                change_r_chance) if custom_params else genetics.Genetics()
    inst = genetic.start(inst, max_proc_time)

    inst.t = timer() - start
    sys.stdout.write('.')
    sys.stdout.flush()
    return inst


def schedule(inst, max_proc_time=0):
    return custom_schedule(inst, False, max_proc_time)


def export(inst):
    path = "results"
    if not os.path.exists(path):
        os.makedirs(path)

    filename = path + "/n" + str(inst.n) + "k" + str(inst.k) + "h" + str(int(inst.h * 10))
    file = open(filename, "w+")
    if (inst.h == 0.2 and inst.n == 10) or (inst.h == 0.4 and inst.n == 20) or (inst.h == 0.6 and inst.n == 50) or (
            inst.h == 0.8 and inst.n == 100) or (inst.h == 0.2 and inst.n == 200) or (
            inst.h == 0.4 and inst.n == 500) or (inst.h == 0.6 and inst.n == 1000):
        print(str(inst.f) + " " + str(inst.t))
    file.write(str(inst.f) + ' ' + str(inst.h) + ' ' + str(inst.r))
    for j in inst.jobs:
        file.write(' ' + str(j.id))
    file.close()


def export_tuner(instances, attempts, max_gen, const_mem, pop_size, cross_cha, mut_cha, swap_cha, change_cha):
    path = "tuner_results"

    n = instances[0].n
    f = sum(i.f for i in instances)/attempts
    t = sum(i.t for i in instances)/attempts

    filename = os.path.join(path, "n{0}.csv".format(n))
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(filename):
        with open(filename, "a") as file:
            file.write("n" + '\t' + "f" + '\t' + "time" + "\t"
                       + "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}".format("MAX_GENERATIONS", "CONSTANT_MEMBERS", "POPULATION_SIZE", "CROSSOVER_CHANCE",
                                                                      "MUTATION_CHANCE", "SWAP_ELEMENT_CHANCE", "CHANGE_R_CHANCE"))

    with open(filename, "a") as file:
        file.write("\n" + str(n) + '\t' + str(f) + '\t' + str(t)
                   + "\t" + "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}".format(max_gen, const_mem, pop_size, cross_cha, mut_cha, swap_cha, change_cha))
