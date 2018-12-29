import problem_manager

for s in [10, 20, 50, 100, 200, 500, 1000]:
    print("n=" + str(s) + "\n")
    instances = problem_manager.read(s)
    for i in instances:
        problem_manager.schedule(i)
    for i in instances:
        problem_manager.export(i)
