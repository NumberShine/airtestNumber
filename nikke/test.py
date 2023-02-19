import datetime
import json
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import threading
from func_timeout import func_set_timeout
import func_timeout
import sys
import psutil as pt


def daily_json(info):
    file_path = "F:/Code/airtest/nikke/log"
    date = "abctest"
    full_path = "%s/%s.json" % (file_path, date)
    if os.path.exists(full_path):
        with open(full_path, "r") as f:
            daily_dic = json.load(f)
    else:
        daily_dic = {}

    daily_dic.update(info)
    with open(full_path, "w") as f:
        json.dump(daily_dic, f, indent=4)


def work(msg):
    print(msg)


def timer_123():
    t = Timer(5, work)
    t.start()
    msg = input("input here")
    if len(msg) > 0:
        print(len(msg))
        t.cancel()
        work(msg)


# total = 1000000
# spe = 0
# for i in range(0, total):
#     array = []
#     for j in range(0, 8):
#         array.append(np.random.randint(0, 4))
#     flag = True
#     for i in range(0, 4):
#         if array.count(i) != 2:
#             flag = False
#     if flag:
#         spe += 1
#
# print("%f %%" % (spe * 100/total))

def timeout(f):
    def inner(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except func_timeout.exceptions.FunctionTimedOut:
            print("超时")
            time.sleep(1)
    return inner


@timeout
@func_set_timeout(1)
def timer_set_now():
    chosen = input("是否输入\n")
    now = datetime.datetime.today()
    after = now + datetime.timedelta(seconds=30)
    # print(now)
    print(after)


# now = datetime.datetime.today()
# after = now + datetime.timedelta(seconds=30)
# print(now)
# print(after)
# print("%s:%02d" % (after.hour, after.minute))
# print("{:0>2}:{:0>2}".format(after.hour, after.minute))


def aa():
    pids = pt.pids()
    for pid in pids:
        try:
            p = pt.Process(pid)
            print(p.name())
        except pt.NoSuchProcess:
            continue


flag = 3
print("\r脚本运行中{: <10}".format('.' * flag), end='', flush=True)