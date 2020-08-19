import threading
import time


def printhread(threadName, delay):
    while 1:
        time.sleep(delay)
        print("%s: %s" % (threadName, time.ctime(time.time())))


thread3 = threading.Thread(target=printhread, args=("Thread-1", 1))
thread4 = threading.Thread(target=printhread, args=("Thread-2", 3))

# Start new Threads
thread3.daemon = True
thread4.daemon = True
thread3.start()
thread4.start()
thread3.join()
thread4.join()
