from threading import Thread, local
import queue

threadLocal = local()


def function(arg, result_queue):
    threadLocal.value = 0

    for _ in range(arg):
        threadLocal.value += 1

    result_queue.put(threadLocal.value)


def main():
    a = 0
    result_queue = queue.Queue()
    threads = []
    for i in range(5):
        thread = Thread(target=function, args=(1000000, result_queue))
        thread.start()
        threads.append(thread)

    [t.join() for t in threads]
    while not result_queue.empty():
        a += result_queue.get()
    print("----------------------", a)  # ???


main()
