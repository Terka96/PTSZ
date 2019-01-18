import math
import os

import problem_manager

MAX_S = 1000
TIME_FACTOR = 750

for s in [100]:
    instances = problem_manager.read(s)
    # print(math.pow(s, 1/6))
    for i in range(len(instances)):
        instances[i] = problem_manager.schedule(instances[i], 1)

    print("\n\nWyniki dla n={0}:\n".format(s))

    if os.path.exists("results.csv"):
        os.remove("results.csv")

    for i in instances:
        problem_manager.export(i)
