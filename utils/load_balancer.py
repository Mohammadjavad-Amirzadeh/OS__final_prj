from queue import PriorityQueue

def load_balancing(readyqueue1: PriorityQueue, readyqueue2: PriorityQueue, readyqueue3: PriorityQueue):
    t = min(readyqueue1.qsize, readyqueue2.qsize, readyqueue3.qsize)
    if t == readyqueue1.qsize:
        return readyqueue1
    elif t == readyqueue2.qsize:
        return readyqueue2
    elif t == readyqueue3.qsize:
        return readyqueue3