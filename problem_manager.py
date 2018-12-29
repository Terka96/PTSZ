import os
from timeit import default_timer as timer

from Instance import Instance
from Job import Job

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


def calc_result(inst):
    dd = int(inst.d * inst.h)
    t = inst.r
    for j in inst.jobs:
        t += j.p
        if t < dd:
            inst.f += (dd - t) * j.a
        elif t > dd:
            inst.f += (t - dd) * j.b
    inst.f = int(inst.f)


def schedule(inst):
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
    inst.t = timer() - start
    # liczenie kary
    calc_result(inst)


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
