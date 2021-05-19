from threading import Thread, Lock

a = 0


def function(arg, lock):
    global a

    for _ in range(arg):
        lock.acquire()
        a += 1
        lock.release()


def main():
    lock = Lock()
    threads = []
    for i in range(5):
        thread = Thread(target=function, args=(1000000, lock,))
        thread.start()
        threads.append(thread)

    [t.join() for t in threads]
    print("----------------------", a)  # ???


main()
