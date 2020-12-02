from tools.threading import MultiProdSingleConQueue, AsyncRun, QueueMustPopFront
from unittest import TestCase

class TestMessaging(TestCase):
    def test_HelloWorld(self):
        queue = MultiProdSingleConQueue()
        result = ""
        def con():
            nonlocal queue
            nonlocal result
            result = ""
            word = None
            while word != "!":
                word = queue.Pop()
                result += word
            return word

        conThread = AsyncRun(con)
        AsyncRun(lambda: queue.Push("Hello")).join()
        AsyncRun(lambda: queue.Push(" World"))
        AsyncRun(lambda: queue.Push("!"))
        conThread.join()
        self.assertEqual(result, "Hello World!")

    def test_Queue_NoMiddlePop(self):
        queue = MultiProdSingleConQueue()
        queue.append(0)
        queue.append(1)
        queue.append(2)
        self.assertRaises(QueueMustPopFront, lambda: queue.pop(1))

    def test_HelloWorld_ListInterface(self):
        queue = MultiProdSingleConQueue()
        result = ""
        def con():
            nonlocal queue
            nonlocal result
            result = ""
            word = None
            while word != "!":
                word = queue.pop(0)
                result += word
            return word

        conThread = AsyncRun(con)
        AsyncRun(lambda: queue.append("Hello")).join()
        AsyncRun(lambda: queue.append(" World"))
        AsyncRun(lambda: queue.append("!"))
        conThread.join()
        self.assertEqual(result, "Hello World!")
