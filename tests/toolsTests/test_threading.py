from unittest import TestCase

from tools.threading import MultiProdSingleConQueue, async_run, QueueMustPopFront


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
                word = queue.pop()
                result += word
            return word

        conThread = async_run(con)
        async_run(lambda: queue.push("Hello")).join()
        async_run(lambda: queue.push(" World"))
        async_run(lambda: queue.push("!"))
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

        conThread = async_run(con)
        async_run(lambda: queue.append("Hello")).join()
        async_run(lambda: queue.append(" World"))
        async_run(lambda: queue.append("!"))
        conThread.join()
        self.assertEqual(result, "Hello World!")
