from threading import Thread

a = []


def function(arg):
    global a
    for _ in range(arg):
        a.append(1)


def main():
    threads = []
    for i in range(5):
        thread = Thread(target=function, args=(1000000,))
        thread.start()
        threads.append(thread)

    [t.join() for t in threads]
    print("----------------------", len(a))  # ???


main()
