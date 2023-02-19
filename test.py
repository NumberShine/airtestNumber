import common as cn
from datetime import datetime
from common import c, w, clink, exp_dec
import network
from airtest.core.api import *
import cv2
import numpy as np
from matplotlib import pyplot as plt
import random
import math
import datetime
from mrfz_common.mrfz_common import search, findallclick, snapcheck, quickswipe, distance, average_gray_scale
from assignment.jijian import center_change, power_change, dormitory_change, tc_change, trade_acc, dormitory_spare_search
from airtest.core.android.android import Android
from assignment.first_page import credit_check

trade_group = [["wulian", "baihui", "longsl"],
               ["lapld", "dekss", "jue"],
               ["nengts", "xuezhi", "kesong"]]


def connect():
    mission_name = "jijian"
    ini = cn.initial(name=mission_name, chdir=2)
    ini.start()


def e_check():
    b = []
    for i in range(1, 10):
        c = cn.e("lapld", th=0.1 * i, method=['brisk'])
        if type(c) != bool:
            b.append(c)
        print(0.1 * i)
    snapcheck(b)


def fa_check():
    a = cn.fa("on_shift")
    #a = np.append(a, cn.fa("c99_small"), axis=0)
    #a = np.append(a, cn.fa("expedited_plan"), axis=0)

    print(a)
    snapcheck(a)



def all():

    tc_change(tor=1)

    # tc_change(tor=2)

    #power_change()

    #center_change()

    dormitory_change()


def cut():
    # 188 427  x+238
    # 68 547
    # 188 667
    # 1507 307
    # 1627 427
    # 1627 547
    # 1095 237
    b = Android().snapshot()
    x = [1160, 37]
    while 1:
        x_plus = eval(input("x?"))
        y_plus = eval(input("y?"))
        x[0] += x_plus
        x[1] += y_plus
        c = b[x[1]:x[1] + 40, x[0]:x[0] + 66]
        cv2.imwrite("test.png", c)
        c = cv2.imread("test.png")
        cv2.imshow(str(x[0]) + " " + str(x[1]), c)
        cv2.waitKey(0)


def cut2():
    b = Android().snapshot()
    x = [[1507, 307], [1627, 427], [1627, 547], [1095, 237]]
    for cor in x:
        for i in range(0, 1):
            c = b[cor[1]:cor[1] + 104, cor[0] + 238 * i:cor[0] + 224 + 238 * i]
            cv2.imwrite("test.png", c)
            c = cv2.imread("test.png")
            d = cv2.cvtColor(c, cv2.COLOR_RGB2GRAY)
            e = np.average(d)
            print(e)
            name = str(e)
            cv2.imshow(name, c)
    cv2.waitKey(0)


connect()

"""
while 1:
    x = eval(input("x?"))
    quickswipe(d=1950 + x, duration=1)
    time.sleep(1)
    quickswipe(d=-2000, duration=1)
    print(1640 + x)
"""
def swipe_check():
    for j in range(10):
        for i in range(3):
            quickswipe(d=1950, duration=1)
        quickswipe(d=-4000, duration=1, times=2)


# dormitory_spare_search(check=1)
# fa_check()

# credit_check()

#trade_acc()
#average_gray_scale()

all()
# e_check()
