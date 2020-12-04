import threading


def async_run(task):
    thread = threading.Thread(target=task)
    thread.start()
    return thread


class QueueMustPopFront(Exception):
    pass


class MultiProdSingleConQueue:
    def __init__(self):
        self.data = []
        self.condition = threading.Condition()

    def push(self, item):
        self.condition.acquire()
        self.data.append(item)
        self.condition.notify(1)
        self.condition.release()

    def append(self, item):
        self.push(item)

    def pop(self, idx=0):
        if idx != 0:
            raise QueueMustPopFront

        self.condition.acquire()
        if len(self.data) == 0:
            self.condition.wait()
        item = self.data.pop(0)
        self.condition.release()

        return item
