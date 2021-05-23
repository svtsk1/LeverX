from threading import Thread, Lock
import queue


class ThreadLocker(object):
    def __init__(self, lock):
        self.lock = lock

    def __enter__(self):
        self.lock.acquire()

    def __exit__(self, *args):
        self.lock.release()


def function(arg, lock, a, result_queue):

    for _ in range(arg):
        with ThreadLocker(lock):
            a += 1

    result_queue.put(a)


def main():
    a = 0
    result_queue = queue.Queue()
    lock = Lock()
    threads = []
    for i in range(5):
        thread = Thread(target=function, args=(1000000, lock, a, result_queue))
        thread.start()
        threads.append(thread)

    [t.join() for t in threads]
    while not result_queue.empty():
        a += result_queue.get()
    print("----------------------", a)  # ???


main()
