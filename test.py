#Not Used
class operation:
	def __init__(self, i, ptime):
		self.id = i
		self.processing_time = ptime
		self.state = 0
		self.done = False
	
	def process(self):
		self.state += 1
		if self.state == self.processing_time:
			self.done = True
			return True

class job:
	def __init__(self, i):
		self.id = i
		self.process_times = []
		self.machine = None
		self.state = 0
		self.sub_state = 0
		self.done = False
		#Times
		self.start_time = -1
		self.end_time = -1

	def process(self):
		self.sub_state += 1
		if (self.sub_state == self.process_times[self.state]):
			self.sub_state = 0
			self.state += 1
			if self.state == len(self.process_times):
				self.done = True
			return True
		return False
	
class machine:
	#Common Parameters
	job_buffer_capacity = 1
	def __init__(self, i):
		self.id = i
		self.life = 0
		self.current_job = None
		self.job_buffer = []
		self.pred = None
		self.suc = None
		self.wait_mode = False

	def push_to_buffer(self, job):
		if (len(self.job_buffer) < machine.job_buffer_capacity):
			self.job_buffer.append(job)
			return True
		else:
			return False

	def assign_job(self, job):
		self.current_job = job

	def fetch_job(self):
		if (len(self.job_buffer)>0):
			self.assign_job(self.job_buffer[0])
			if (self.current_job.state==0) & (self.current_job.sub_state == 0):
				self.current_job.start_time = self.life - 1
			# print ("Machine ", self.id, "Fetched Job", self.current_job.id)
			del self.job_buffer[0]
		else:
			# print("Machine ", self.id, "Buffer Empty")
			return
	
	def tick(self):
		self.life += 1
		if (self.current_job is None):
			self.fetch_job()
			return
		
		if (self.wait_mode):
			self.waiting()
		else:
			self.process_job()

	
	def waiting(self):
		self.wait_mode = True
		# print( "Machine ", self.id, "Waiting")
		if self.suc.push_to_buffer(self.current_job):
			self.wait_mode = False
			self.current_job = None
			self.fetch_job()
	
	def process_job(self):
		if (self.current_job is None):
			return
		status = self.current_job.process()
		if status:
			if self.current_job.done:
				self.current_job.end_time = self.life - 1
				self.current_job = None
				return
			else:
				#Check if we can push to successor buffer
				self.waiting()
				


def main():
	#Setup environment
	machs = []
	for i in range(4):
		machs.append(machine(i))

	#Setup machine relationships
	for i in range(4):
		m = machs[i]
		if (i > 0):
			m.pred = machs[i - 1]
		if (i<len(machs) - 1):
			m.suc = machs[i + 1]

	#Report machines
	# for i in range(4):
	# 	m = machs[i]
	# 	print("Machine : ", m, m.id, "Pred", m.pred ,"Suc", m.suc)

	jobs = []
	job_pool = []
	for i in range(2):
		jb = job(i)
		#Add processing times
		jb.process_times=[1, 2, 1, 1]
		jobs.append(jb)
		job_pool.append(jb)

	#Start processing
	jobs_finished = False
	c = 0

	#Feed buffer to first machine
	for i in range(len(jobs)):
		m = machs[0]
		m.job_buffer.append(jobs[i])

	schedule = [0] * len(jobs)

	while (len(jobs)):
		#Check if jobs have finished processing
		jobs_finished = True
		for j in range(len(jobs)-1, -1, -1):
			if (jobs[j].done):
				del jobs[j]

		print("----\nTicking Machines", "Iteration:", c)
		#Tick all machines
		for i in range(len(machs)):
			m = machs[i]
			m.tick()

		print("----\nJob Status")
		for j in jobs:
			if (j.done):
				print("Job", j.id, "Done at", c, "Start Time: ",j.start_time, "End Time: ", j.end_time)
				schedule[j.id] = c

			# print("Job", j.id, "sub_state", j.sub_state, "State", j.state, "Done", j.done)
		
		c += 1


	print(schedule)


if __name__ == "__main__":
	print (" Executing Main ")
	main()
	



