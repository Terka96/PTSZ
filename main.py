import problem_manager
import genetics

for s in [10, 20]: #, 50, 100, 200, 500, 1000]:
    print("n=" + str(s) + "\n")
    instances = problem_manager.read(s)
    for i in range(len(instances)):
        problem_manager.schedule(instances[i])

        # Testing genetic algorithm
        instances[i] = genetics.start(instances[i])

    #     todo: dlaczego nie działa (czytelność) for job in instances:
    #                                       job = genetics.start(job)

    for i in instances:
        problem_manager.export(i)
