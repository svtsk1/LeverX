from time import time
from threading import Thread

a = 0


def function(arg):
    global a
    b = 0
    for _ in range(arg):
        b += 1
    a += b


def main():
    time_start = time()
    threads = []
    for i in range(5):
        thread = Thread(target=function, args=(1000000,))
        thread.start()
        threads.append(thread)

    [t.join() for t in threads]
    time_finish = time()
    print("----------------------", a, f'Время выполнения: {time_finish - time_start}')  # ???


main()
