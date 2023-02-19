# -*- encoding=utf8 -*-
__author__ = "Number‘s Laptop"

from airtest.core.api import *
from random import randint as r
from common import c, w, clink
from network import message_group
import common as cn

mission_name = "txy"

ini = cn.initial(name=mission_name, port="7555")
ini.start()
# script content
cn.PAUSE_TIME = [120]
try:
    for times in range(1, 7):
        t1 = time.time()
        w("quick_bar")
        # for i in range(0, 4):
        # swipe((1205, 909), (272, 827), duration=0.6)
        clink("txy", "normal_mission", th=0.9)
        c("normal_mission", wt=4)
        cn.man_dec("xysj", rtb=2)
        w("mission_start")
        c("airport_1.")
        c("confirm")
        c("airport_2.")
        c("confirm")
        c("base.")
        c("confirm")
        c("mission_start", wt=3)
        c("airport_1.")
        c("plan_mode")
        c("step_1.")
        c("step_2.")
        c("middle.")
        c("airport_2.")
        c("step_3.")
        c("plan_go")
        cn.progress_bar("mission_finish", times)
        c("middle.", times=4, interval=0.6, wt=1)
        c("middle.", times=3, interval=0.6, wt=2)
        context = [mission_name, times, time.time() - t1]
        cn.fileopr(context)
        """print("延迟检测平均值:%s 最大值：%s 总值：%s" % (np.mean(cn.delay_collect),
                                           max(cn.delay_collect), np.sum(cn.delay_collect)))"""
    c("back")
    cn.support_go()
except TargetNotFoundError:
    context = [mission_name, times, time.time() - t1]
    message_group(context, mode="fail")
    print("没找到")
else:
    message_group(context, mode=1)
    os.popen('taskkill.exe /pid:' + str(os.getppid()))
