import threading
import time


counter_lock = 0
counter = 0
lock = threading.Lock()

def increment():
    global counter_lock
    for _ in range(1_000_000):
        with lock:
            counter_lock +=1

    for _ in range(1_000_000):
        global counter
        tmp = counter
        time.sleep(0)
        counter = tmp + 1

threads = []

for _ in range(4):
    t = threading.Thread(target=increment)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(counter, counter_lock)
