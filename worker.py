from rq import Connection, Worker, Queue

with Connection():
	worker = Worker(map(Queue, ['default']))
	worker.work()
