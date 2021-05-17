from threading import Thread, Lock


def function(arg, a, lock):

    lock.acquire()
    for _ in range(arg):
        a += 1
    lock.release()


def main():
    a = 0
    lock = Lock()
    threads = []
    for i in range(5):
        thread = Thread(target=function, args=(1000000, a, lock,))
        thread.start()
        threads.append(thread)

    [t.join() for t in threads]
    print("----------------------", a)  # ???


main()
