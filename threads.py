from threading import Thread, Condition
from time import sleep
from queue import Queue

q = Queue(maxsize=1)
c = Condition

q.put(True)

def printEvery3Seconds():
    n = 0
    while True:
        print("I am printing something thread\n")
        sleep(0.5)

thread = Thread(target=printEvery3Seconds, daemon=True)
thread.start()



while True:
    input("stop thread")

    input("start thread")

        
