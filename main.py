import math

import problem_manager

MAX_S = 1000
TIME_FACTOR = 30

for s in [10, 20, 50, 100, 200, 1000]:
    instances = problem_manager.read(s)
    # print(math.pow(s, 1/6))
    for i in range(len(instances)):
        instances[i] = problem_manager.schedule(instances[i], (s/MAX_S)*TIME_FACTOR/math.pow(s, 1/5))

    print("\n\nWyniki dla n={0}:\n".format(s))
    for i in instances:
        problem_manager.export(i)
