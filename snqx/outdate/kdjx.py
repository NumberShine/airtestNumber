# -*- encoding=utf8 -*-
__author__ = "Number‘s Laptop"

from airtest.core.api import *
from random import randint as r
from common import c, w, clink
from network import message_group
import common as cn


mission_name = "kdjx"

ini = cn.initial(name=mission_name, port="7555")
ini.start()
# script content
cn.PAUSE_TIME = 60
try:
    for times in range(1, 7):
        t1 = time.time()
        clink("kdjx", "normal_mission", th=0.9)
        c("normal_mission")
        cn.man_dec("kdjx", rtb=2)
        w("mission_start")
        c("base.")
        cn.man_repair(num=3)
        c("airport_1.")
        c("confirm")
        c("mission_start", wt=3)
        c("base.")
        c("plan_mode")
        c("step_1.")
        c("step_2.")
        c("plan_go", wt=2)
        cn.progress_bar("mission_finish", times)
        c("middle.", times=5, interval=0.6, wt=1)
        context = [mission_name, times, time.time() - t1]
        cn.fileopr(context)
        """print("延迟检测平均值:%s 最大值：%s 总值：%s" % (np.mean(cn.delay_collect),
                                           max(cn.delay_collect), np.sum(cn.delay_collect)))"""
    c("back")
except TargetNotFoundError:
    context = [mission_name, times, time.time() - t1]
    message_group(context, mode="fail")
    print("没找到")
else:
    message_group(context, mode=1)

os.popen('taskkill.exe /pid:' + str(os.getppid()))
