# -*- encoding=utf8 -*-
__author__ = "Number‘s Laptop"

from airtest.core.api import *
from random import randint as r
from common import c, w, clink
from network import message_group
import common as cn


mission_name = "134e"
ini = cn.initial(name=mission_name, port="7555")
ini.start()
# script content
cn.PAUSE_TIME = 80
try:
    if not cn.e("mission_start"):
        clink("134e", "normal_mission", th=0.9)
        c("normal_mission")
    for times in range(1, 20):
        t1 = time.time()
        cn.man_dec("134e", rtb=1)
        w("mission_start")
        c("base.")
        cn.man_repair()
        c("airport_1.")
        c("confirm")
        c("mission_start", wt=3)
        if (times + 1) % 2 == 0:
            c("base.", times=2)
            c("supply")
        else:
            c("base.")
        c("plan_mode", ranpos=False)
        c("step_1.")
        c("base.")
        c("plan_go", wt=2)
        cn.progress_bar("plan_mode", times)
        c("base.")
        c("retreat")
        c("confirm")
        c("mission_end")
        c("mission_restart")
        context = [mission_name, times, time.time() - t1]
        cn.fileopr(context)
        """print("延迟检测平均值:%s 最大值：%s 总值：%s" % (np.mean(cn.delay_collect),
                                           max(cn.delay_collect), np.sum(cn.delay_collect)))"""
except TargetNotFoundError:
    context = [mission_name, times, time.time() - t1]
    message_group(context, mode="fail")
    print("没找到")
else:
    message_group(context, mode=1)

# os.popen('taskkill.exe /pid:' + str(os.getppid()))
