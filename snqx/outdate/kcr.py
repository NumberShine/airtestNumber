# -*- encoding=utf8 -*-
__author__ = "Number‘s Laptop"

from airtest.core.api import *
from random import randint as r
from common import c, w, clink
from network import message_group
import common as cn


mission_name = "kcr"

ini = cn.initial(name=mission_name, port="7555")
ini.start()
# script content
cn.PAUSE_TIME = 60
try:
    for times in range(1, 20):
        flag = True
        t1 = time.time()
        while flag:
            w("mission_start")
            c("airport_2.")
            cn.man_repair(num=2)
            c("base.")
            c("confirm")
            c("mission_start", wt=3)
            flag = cn.man_dec("kcr", rtb=2, sw=2)
        c("airport_2.", times=2)
        c("supply", wt=0.5)
        c("plan_mode")
        c("step_3.")
        c("step_4.")
        c("airport_2.")
        c("plan_go", wt=2)
        cn.progress_bar("plan_mode", times)
        c("airport_2.")
        c("retreat")
        c("confirm")
        c("mission_end")
        c("mission_restart")
        context = [mission_name, times, time.time() - t1]
        cn.fileopr(context)
        """print("延迟检测平均值:%s 最大值：%s 总值：%s" % (np.mean(cn.delay_collect),
                                           max(cn.delay_collect), np.sum(cn.delay_collect)))"""
    c("back")
except :
    context = [mission_name, times, time.time() - t1]
    message_group(context, mode="fail")
    print("没找到")
    input()
else:
    message_group(context, mode=1)

os.popen('taskkill.exe /pid:' + str(os.getppid()))
