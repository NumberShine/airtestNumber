# -*- encoding=utf8 -*-
__author__ = "Number‘s Laptop"

from airtest.core.api import *
from random import randint as r
from common import c, w, clink
from network import message_group
from control import control
import common as cn


mission_name = "p22-56"
ini = cn.initial(name=mission_name, port="7555")
ini.start()
con = control(0)
# script content
cn.PAUSE_TIME = 80
try:
    for times in range(1, 23):
        t1 = time.time()
        con.file_change(1)
        clink("56", "normal_mission", th=0.9)
        c("normal_mission", wt=1)
        cn.man_dec("56", rtb=1)
        w("mission_start")
        c("airport_1.")
        cn.man_repair(num=3,adjust=20)
        clink("base.", "confirm")
        clink("confirm")
        c("mission_start", wt=3)
        c("airport_1.")
        c("plan_mode", ranpos=False)
        c("step_1.")
        if r(1, 4) > 1:
            c("step_2.")
        else:
            c("step_3.")
        c("plan_go")
        cn.progress_bar("mission_finish", times)
        c("middle.", times=5, interval=0.5, wt=2)
        context = [mission_name, times, time.time() - t1]
        cn.fileopr(context)
        con.b_check()
        """print("延迟检测平均值:%s 最大值：%s 总值：%s" % (np.mean(cn.delay_collect),
                                           max(cn.delay_collect), np.sum(cn.delay_collect)))"""
except TargetNotFoundError:
    context = [mission_name, times, time.time() - t1]
    message_group(context, mode="fail")
    print("没找到")
else:
    message_group(context, mode=1)
    c("quick_bar")
    c("rtb")
    con.file_change(0)
    os.popen('taskkill.exe /pid:' + str(os.getppid()))
