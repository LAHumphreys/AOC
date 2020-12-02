import threading


def AsyncRun(task):
    thread = threading.Thread(target=task)
    thread.start()
    return thread

class QueueMustPopFront(Exception):
    pass

class MultiProdSingleConQueue:
    def __init__(self):
        self.data = []
        self.condition = threading.Condition()

    def Push(self, item):
        self.condition.acquire()
        self.data.append(item)
        self.condition.notify(1)
        self.condition.release()

    def pop(self, idx):
        if idx == 0:
            return self.Pop()
        else:
            raise QueueMustPopFront

    def append(self, item):
        self.Push(item)

    def Pop(self):
        item = None

        self.condition.acquire()
        if len(self.data) == 0:
            self.condition.wait()
        item = self.data.pop(0)
        self.condition.release()

        return item
