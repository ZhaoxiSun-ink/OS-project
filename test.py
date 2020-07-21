from queue import PriorityQueue

event_queue = PriorityQueue()
event_queue.put((1, 0, "C", ("data", "data")))
event_queue.put((2, 1, "D", ("data", "data")))
event_queue.put((1, 2, "A", ("data2", "data")))
event_queue.put((1, -1, "B", ("data", "data")))
while not event_queue.empty():
    print(event_queue.get())
