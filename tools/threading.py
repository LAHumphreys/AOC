"""
Multi-threading wrappers and utilities
"""
import threading


def async_run(task):
    """
    Kick off a task in a new thread and return a handle to the
    new thread so it can be managed.

    :param task: The argument-less lambda to run in a new thread

    :return: The thread object the task is running on.
    """
    thread = threading.Thread(target=task)
    thread.start()
    return thread


class QueueMustPopFront(Exception):
    """
    Currently the thread safe queue only supports popping off
    from the front
    """


class MultiProdSingleConQueue:
    """
    Allow multi publishers to push onto this queue,
    and for a consuming thread to retrieve / wait for
    objects on the queue.

    WARNING: Care should be taken to ensure that
             different threads are publishing to consuming
             (since we block when on read when the queue
              is empty)

    In theory this should work fine with multiple consumers,
    but additional tests should be added.
    """

    def __init__(self):
        self.data = []
        self.condition = threading.Condition()

    def push(self, item):
        """
        Push an item onto the queue.
        :param item: The item to push onto the queue
        """
        self.condition.acquire()
        self.data.append(item)
        self.condition.notify(1)
        self.condition.release()

    def append(self, item):
        """
        alias for push, allowing the queue to be used as a list
        """
        self.push(item)

    def pop(self, idx=0):
        """
        Retrieve the next item due to be removed from the queue.

        If no such item exists, block and wait (forever) until
        the queue has an item

        :param idx: Must be zero. Parameter allowed to fulfil
                    list interface

        :return: The item
        """
        if idx != 0:
            raise QueueMustPopFront

        self.condition.acquire()
        if len(self.data) == 0:
            self.condition.wait()
        item = self.data.pop(0)
        self.condition.release()

        return item
