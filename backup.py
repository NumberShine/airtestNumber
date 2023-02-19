author__ = "qx100"

from common import *
from copy import deepcopy
import os
from random import uniform
from math import log as logg
from datetime import datetime
import psutil as pt
import matplotlib.pyplot as plt
import numpy as np
import time as t


ST.SNAPSHOT_QUALITY = 99


def shot():
    snapshot(filename='D:/Application/py/Airtest_mouse/snqx/png/test.bmp')


def man():
    img = cv2.imread("repair.bmp")
    cv2.imshow("repair1", img)
    cv2.line(img, (10, 595), (1000, 595), (0, 0, 255))
    cv2.imshow("repair", img)
    cv2.waitKey()


def cmd():
    command = '''start cmd /k "cd D:\Application\py\Airtest_mouse\snqx & python 124e.py "'''
    os.system(command)


def ranln(t):
    lamada = 1 / t
    x = uniform(0.015 * lamada, 0.95 * lamada)
    y = -1 / lamada * logg(x / lamada)
    return y


def tfind_circle():
    dev = device()
    circle_img = dev.snapshot()
    circle_img = circle_img[780:912, 1150:1280]
    # cv2.imshow("cut_circle", circle_img)
    gray = cv2.cvtColor(circle_img, cv2.COLOR_BGR2GRAY)
    result = cv2.medianBlur(gray, 5)
    circles = cv2.HoughCircles(result, cv2.HOUGH_GRADIENT, 1, 50, param1=90, param2=40, minRadius=10, maxRadius=100)
    if circles is None or circles[0, 0, 0] == 0:
        return False
    else:
        # print("\n出现延迟\n")
        return True


def fileoprr(name="", context=[]):
    dt = datetime.now()
    f = open("log/%s.txt" % name, "a+")
    f.seek(0)
    flines = f.readlines()
    if not flines:
        flines.append("第 0 次")
    fsp = eval(flines[-1].split()[1]) + 1
    f.write("————————分割线——————————\n")
    f.write("日期：{}\n所用时间：{}\n第 {} 次\n".format(dt.strftime('%Y-%m-%d %H:%M:%S'),
                                              context[0], fsp))
    print("所用时间：%s 本次执行第 %s 次 总完成次数：%s" % (context[0], context[1], fsp))
    f.close()


def bgr():
    ini = cn.initial(chdir=3, add_para=["t"])
    ini.start()
    while 1:
        x = eval(input("x坐标"))
        y = eval(input("y坐标"))
        dev = device()
        repair_img = dev.snapshot()
        print(repair_img[y, x])
        cv2.circle(repair_img, (x, y), 3, (0, 0, 222))
        cv2.circle(repair_img, (x, y), 10, (0, 0, 222))
        cv2.imshow("1234", repair_img[y - 20:y + 20, x - 50:x + 50])
        cv2.waitKey(5000)


def point_detail(name):
    global point
    if name == "spl":
        return 0
    with open("file/" + name + ".txt", "r+") as dlt:
        for line in dlt:
            if line == "\n":
                continue
            xline = line.translate(str.maketrans('[,<>:]', '      ')).split()
            point[str(xline[0])] = [int(xline[1]), int(xline[2]), int(xline[3]), int(xline[4])]


def point_pos_check(name="spl"):
    global point
    ini = initial(add_para=['t'])
    ini.start(com_add=0)
    dev = device()
    img = dev.snapshot()
    point_detail(name)
    print(point)
    for poi in point:
        cv2.circle(img, (point[poi][0], point[poi][1]), 10, (0, 0, 0))
    cv2.imshow("point_check", img)
    cv2.waitKey()


def getPidByName(Str):
    pids = pt.process_iter()
    pidList = []
    for pid in pids:
        if pid.name() == Str:
            pidList.append(pid.pid)
    return pidList


def file_readtime(name):
    f = open("snqx/log/%s.txt" % name, "a+")
    f.seek(0)
    flines = f.readlines()
    total = 0
    for _ in range(0, int(len(flines) / 4)):
        ftime = flines[_ * 4 + 2].replace("所用时间：", "")
        total += eval(ftime)
    total *= 1
    print("%.2f" % total)
    h = total / 3600
    m = (h - int(h)) * 60
    s = (m - int(m)) * 60
    print("%d小时 %d分钟 %d秒" % (h, m, s))
    f.close()


def img_cut_test():
    ini = initial()
    ini.start()
    a = device().snapshot()
    while 1:
        cv2.imshow("123", a[185:243, 1041:1210])
        cv2.waitKey(100)


def file_readtime2(name):
    t1 = t.time()
    f = open("snqx/log/%s.txt" % name, "a+")
    f.seek(0)
    flines = f.readlines()
    arr = []
    arr_1 = []
    for _ in range(0, int(len(flines) / 4)):
        ftime = flines[_ * 4 + 2].replace("所用时间：", "")
        arr.append(eval(ftime))
    mean = np.mean(arr)
    print("time:%s" % (t.time() - t1))
    plt.figure(1)
    plt.plot(arr)
    plt.xlabel("mean:%s var:%s total:%s" % (np.mean(arr), np.var(arr), len(arr)))
    plt.ylabel("total:%s" % np.sum(arr))
    for at in arr:
        if abs(at - mean) / mean <= 0.2:
            arr_1.append(at)
            arr_1.pop()
    if arr_1:
        plt.figure(2)
        plt.plot(arr_1)
        plt.xlabel("mean:%s var:%s total:%s" % (np.mean(arr_1), np.var(arr_1), len(arr_1)))
    plt.show()
    f.close()

import common as cn
def reset123():
    f = open(cn.project_pos + "save_data/today.txt", "a+")
    f.write("0")
    f.close()

if __name__ == '__main__':
    reset123()
"""
shot("abc6")
input("1234")
shot("abc7")
"""

"""
jpg = 0
png = 0
for i in range(0,20):
    t = time.time()
    snapshot(filename='D:/Application/py/Airtest_mouse/png/test.jpg')
    jpg += time.time() - t
    t = time.time()i
    snapshot(filename='D:/Application/py/Airtest_mouse/png/test.png')
    png += time.time() - t
    t = time.time()
    snapshot(filename='D:/Application/py/Airtest_mouse/png/test.bmp')
    bmp = time.time() - t


print("jpg = {:.3f}".format(jpg/20))
print("png = {:.3f}".format(png/20))
print("bmp = {:.3f}".format(bmp/20))
"""
