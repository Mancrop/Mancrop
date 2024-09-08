from collections import deque
from threading import Lock


class CircularQueue:
    def __init__(self, size):
        self.queue = deque(maxlen=size)
        self.size = size
        self.lock = Lock()

    def enqueue(self, item):
        with self.lock:
            if len(self.queue) == self.size:
                self.queue.popleft()  # Remove the oldest item
            self.queue.append(item)

    def dequeue(self):
        with self.lock:
            if self.queue:
                return self.queue.popleft()
            else:
                raise IndexError("Queue is empty")

    def peek(self):
        with self.lock:
            if self.queue:
                return self.queue[0]

    def is_full(self):
        with self.lock:
            return len(self.queue) == self.size

    def is_empty(self):
        with self.lock:
            return len(self.queue) == 0

    def __str__(self):
        with self.lock:
            return str(self.queue)
