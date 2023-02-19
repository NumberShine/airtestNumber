# -*- encoding=utf8 -*-
__author__ = "Number‘s Laptop"

from airtest.core.api import *
from common import c, e, w
import common as cn
from network import message_group, ocr_str
from control import control
import re

mission_name = "zj"
ini = cn.initial(name=mission_name)
ini.start()
con = control(2)


def zj_timer():
    len_flag = 1
    while len_flag == 1:
        len_flag = 0
        timer = []
        time_total = ocr_str("zj")
        print(time_total)
        for time_str in time_total:
            tsp = re.sub('[^0-9]', '', time_str)
            print(tsp)
            if len(tsp) != 6:
                len_flag = 1
                break
            timer.append(int(tsp[0:2]) * 3600 + int(tsp[2:4]) * 60 + int(tsp[4:6]))
        if len_flag == 0:
            print(timer)

    return timer


def zj_check(timer):
    global flag
    global fairy
    f = 0
    for _ in range(0, 3):
        if timer[_] > 3600:
            c("build_%s." % (_+1))
            c("confirm")
            cn.clink("mid.", "quick_bar")
            c("build_%s." % (_+1))
            c("confirm")
            c("build_start")
            fairy += 1
            flag += 1
            f = 1
        elif timer[_] == 0:
            c("build_%s." % (_+1))
            c("mid.", times=4)
            w("quick_bar")
            c("build_%s." % (_+1))
            c("confirm")
            c("build_start")
            flag += 1
            f = 1
    return f


def boot():
    global boot_time
    t1 = time.time()
    pos = e("boot_snqx")
    if pos:
        c(pos)
        time.sleep(10)
        c("boot_start")
        w("boot_eye")
        c("middle.")
        time.sleep(20)
        w("L_support")
    boot_time = time.time() - t1


flag = 0
times = 0
boot_time = 50
try:
    while flag <= 30:
        fairy = 0
        timer = zj_timer()
        while zj_check(timer) == 1:
            timer = zj_timer()
        cn.PAUSE_TIME = min(timer) + cn.ranln(2) + 1
        cn.progress_bar(False, flag, gap=40)
        # timer = zj_timer()
        context = [mission_name, flag, fairy+1]
        cn.fileopr(context)
        message_group(context, mode=6)

except TargetNotFoundError:
    context = [mission_name, flag]
    message_group(context, mode="fail")
    print("没找到")
else:
    message_group(context, mode=1)
