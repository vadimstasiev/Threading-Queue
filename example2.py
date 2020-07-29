import os
import sys
import threading
from queue import Queue
import time

print_lock = threading.Lock()
q = Queue()


def _getThreads():
    """ Returns the number of available threads on a posix/win based system """
    if sys.platform == 'win32':
        return (int)(os.environ['NUMBER_OF_PROCESSORS'])
    else:
        return (int)(os.popen('grep -c cores /proc/cpuinfo').read())

def worker_thread():
    while True:
        job=q.get()
        job()
        q.task_done()

def random_function_1():
    time.sleep(0.5)
    with print_lock:
        print("random_function_1")

def random_function_2():
    time.sleep(0.5)
    with print_lock:
        print("random_function_2")

if __name__ == "__main__":
    num_workers=_getThreads()

    for wk in range(num_workers):
        t = threading.Thread(target = worker_thread)
        t.name='Worker-'+str(wk)
        t.daemon = True
        t.start()

    start=time.time()
    
    num_jobs=10

    q.put(random_function_1)
    q.put(random_function_2)

    q.join() # Blocks until all items in the Queue have been gotten and processed

    print('Entire job took:', time.time()-start)
