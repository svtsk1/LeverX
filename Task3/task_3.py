from time import time
from threading import Thread

a = []


def function(arg):
    global a
    for _ in range(arg):
        a.append(1)


def main():
    time_start = time()
    threads = []
    for i in range(5):
        thread = Thread(target=function, args=(1000000,))
        thread.start()
        threads.append(thread)

    [t.join() for t in threads]
    time_finish = time()
    print("----------------------", len(a), f'Время выполнения: {time_finish - time_start}')  # ???


main()
