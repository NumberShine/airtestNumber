# -*- encoding=utf8 -*-
__author__ = "Number‘s Laptop"

from airtest.core.api import *

from common import c, e
from network import message_group, ocr_str
import common as cn
import time
# from pid import getport2
import math
from airtest.core.android.android import Android
import cv2
import numpy as np

dev = None


def quickswipe(d=300, times=1, duration=0.5):
    global dev
    if dev is None:
        dev = Android()
    for i in range(0, times):
        dev.swipe((960, 540), (960 - d, 540), duration=1, steps=3)
        dev.swipe((960, 540), (960 + 10, 540), duration=0.05)
    time.sleep(abs(d) / 1500)


def findandclick(name):
    cn.log_out("准备寻找并选择%s" % name, layer=0)
    pos = e(name, th=0.8, layer=1)
    if pos:
        c(pos, layer=1)
        cn.log_out("%s找到并选择" % name, layer=0)
        return 1
    else:
        cn.log_out("%s未找到" % name, layer=0)
        return 0


def search(name: list, max_choose=3, skip=None, level=10):
    if skip is None:
        skip = [-1]
    if not len(name[0]) == 2:
        c("clear_all")
    ST.FIND_TIMEOUT_TMP = 0.05
    finish_find = []
    for name_1 in name:
        """
        print("66666666666666")
        print(skip)
        print(name_1[-1])
        print("66666666666666")
        """
        if name.index(name_1) in skip or name_1[-1] >= level:
            continue
        quickswipe(d=-1500, times=3)
        while 1:
            for oper in name_1:
                if oper in finish_find or type(oper) == int:
                    continue
                if findandclick(oper):
                    finish_find.append(oper)
            if len(finish_find) == len(name_1) - 1 or len(finish_find) >= max_choose:
                print("本次搜索完成， 已找到")
                return name.index(name_1)
            if e("shuichen"):
                if max_choose>  1:
                    cn.clink("clear_all", "jijian_select", logic=True)
                break
            quickswipe(d=1950, duration=1)
    print("没找到")
    return -1


def findallclick(name, max=5):
    all_pos = cn.fa(name, th=0.65)
    print(len(all_pos))
    for target in all_pos:
        target_mid = target['result']
        cn.c(target_mid)
        max -= 1
        if max == 0:
            break


def snapcheck(pos ,name="point_check"):
    font = cv2.FONT_HERSHEY_SIMPLEX
    dev = device()
    img = dev.snapshot()
    for poi in pos:
        cv2.circle(img, (poi[0], poi[1]), 10, (255, 180, 0))
        cv2.putText(img, str(poi[0]) + " " + str(poi[1]), (poi[0], poi[1]), font, 0.8, (180, 255, 0), 2)
    cv2.imshow(name, img)
    cv2.waitKey()


def distance(p1, p2):
    d = 0
    for i in range(len(p1)):
        d += pow((p1[i] - p2[i]), 2)
    d = math.sqrt(d)
    return d


def distance_in_and_un(l1, p2, dist, logic=2):
    dt = []
    logic_num = len(l1)
    for p in l1:
        if distance(p, p2) <= dist:
            logic_num -= 1
    if logic == 1:
        if logic_num == 0:
            return True
        else:
            return False
    else:
        if logic_num < len(l1):
            return True
        else:
            return False


def average_gray_scale():
    total_ags = []
    b = device().snapshot()

    x = [[188, 427], [426, 427], [664, 427],
         [68, 547], [306, 547], [544, 547],
         [188, 667], [426, 667], [664, 667],
         [1497, 297], [1627, 427], [1617, 537], [1095, 237]]

    for cor in x:
        c = b[cor[1]:cor[1] + 104, cor[0]:cor[0] + 224]
        cv2.imwrite("test.png", c)
        c = cv2.imread("test.png")
        d = cv2.cvtColor(c, cv2.COLOR_RGB2GRAY)
        e = np.average(d)
        total_ags.append(e)

        #name = str(e)
        #cv2.imshow(name, c)
    #cv2.waitKey(0)


    tired_group = []
    for ags in total_ags:
        if ags > 64:
            tired_group.append(total_ags.index(ags))

    os.remove("test.png")
    return tired_group


def comp_com(l1, l2):
    for i in l1:
        if i in l2:
            return True
    return False