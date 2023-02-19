from common import *
import threading
from time import time as t
from multiprocessing import Process, Queue

que = Queue()


def tr_check(name, interval, to, q=que):  # 使用子进程的原因是使用子线程就是在与主线程的同一进程下
    initial.start()                               # 因此会导致子线程与主线程airtest函数不能同时执行
    print("子进程启动完成")
    time_out = t()
    while t() - time_out < to:
        pos = e(name)
        if pos:
            c("middle.")
            time.sleep(interval)
        time.sleep(interval)


class mythread(threading.Thread):
    def __init__(self, name, time_out, interval):
        threading.Thread.__init__(self)
        self.time_out = time_out
        self.name = name
        self.interval = interval

    def run(self):
        print("开始线程,检测" + self.name)
        print("退出线程，检测" + self.name)


def run_out(name, interval=3, to=300):
    ps = Process(target=tr_check, args=(name, interval, to))
    ps.start()


def delay1():
    time.sleep(1)


class pro_check:
    def __init__(self, name, interval=5, to=200):
        self.name = name
        self.interval = interval
        self.time_out = to
        self.p1 = Process(target=tr_check, args=(name, interval, to))

    def run(self):
        self.p1.start()

    def stop(self):
        self.p1.terminate()

# if __name__ == '__main__':
