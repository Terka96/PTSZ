import random
from timeit import default_timer as timer


class Instance:
	def __init__(self,n,k,h,d,r,f,jobs):
		self.n = n
		self.k = k
		self.h = h
		self.d = d
		self.t = 0
		self.r = r
		self.f = f
		self.jobs = jobs
	
class Job:
	p = 0
	a = 0
	b = 0
	w = 0

def read(size):
	problemId = 0
	jobsN = 0
	jobsLeft = 0
	instances = []
	inst = 0

	handle = open("data/sch"+str(size)+".txt","r")
	for line in handle.readlines():
		if inst == 0:
			inst = Instance(0,0,0,0,0,0,[])
		elif jobsLeft==0 :
			inst = Instance(0,0,0,0,0,0,[])
			inst.jobs=[]
			inst.k = problemId + 1
			inst.n = size
			jobsN=int(line)
			jobsLeft=jobsN
		else :
			line = [int(s) for s in line.split()]
			j = Job()
			j.id = jobsN-jobsLeft
			j.p = line[0]	#czas
			j.a = line[1]	#kara za szybko
			j.b = line[2]	#kara za późno
			inst.d += j.p
			inst.jobs.append(j)
			jobsLeft-=1
			if jobsLeft==0 :
				for h in [0.2,0.4,0.6,0.8]:
					instances.append(Instance(inst.n,inst.k,h,inst.d,inst.r,inst.f,inst.jobs))
				problemId += 1
	handle.close()
	return instances

def calcResult(inst):
	dd = int(inst.d * inst.h)
	t = inst.r
	for j in inst.jobs:
		t += j.p
		if t < dd:
			inst.f += (dd-t)*j.a
		elif t > dd:
			inst.f += (t-dd)*j.b
	inst.f = int(inst.f)

def mutate(inst):
	if random.randrange(10) > 4:	
		#swap two jobs
		swap1 = random.randint(0,inst.n-1)
		swap2 = random.randint(0,inst.n-1)
		inst.jobs[swap1],inst.jobs[swap2] = inst.jobs[swap2],inst.jobs[swap1]
	else:
		#move jobs block
		inst.r +=random.randint(-inst.r,inst.d*inst.h)

def generateFisrtPopultaion(inst,count):
	population=[]
	for i in range(count):
	#TODO make copy of instance
		population.append(mutate(copyofinst))
	return population


def shedule(inst):
	start=timer()	
	for j in inst.jobs:
		j.w = (-j.a + j.b) * j.p
	inst.jobs = sorted(inst.jobs, key=lambda j: j.w,reverse=True)
	dd = int(inst.d * inst.h)
	t=0
	center=0
	weights=0
	for j in inst.jobs:
		t += j.p
		w = abs(j.w)
		weights += w
		center += t * w
	center = int(center/weights)
	inst.r = max(0,dd - center)
	inst.t=timer() - start
	#liczenie kary
	calcResult(inst)

def export(inst):
	filename = "results/n" + str(inst.n) + "k" + str(inst.k) + "h" + str(int(inst.h*10))
	file = open(filename,"w+")
	if (inst.h==0.2 and inst.n==10) or (inst.h==0.4 and inst.n==20) or (inst.h==0.6 and inst.n==50)	or (inst.h==0.8 and inst.n==100) or (inst.h==0.2 and inst.n==200) or (inst.h==0.4 and inst.n==500) or (inst.h==0.6 and inst.n==1000):
		print(str(inst.f)+" "+str(inst.t))
	file.write(str(inst.f)+' '+str(inst.h)+' '+str(inst.r))
	for j in i.jobs:
		file.write(' '+str(j.id))
	file.close()
for s in [10,20,50,100,200,500,1000]:
	print("n="+str(s)+"\n")	
	instances = read(s)
	for i in instances:
		shedule(i)
	for i in instances:
		export(i)
