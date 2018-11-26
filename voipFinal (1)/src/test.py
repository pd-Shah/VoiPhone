from threading import Thread

def print_hi():
    while True:
        print("hi")

def print_bye():
    while True:
        print("bye")

Thread(target=print_hi).start()
Thread(target=print_bye).start()
