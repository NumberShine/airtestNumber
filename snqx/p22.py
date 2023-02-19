# -*- encoding=utf8 -*-
__author__ = "Number‘s Laptop"

from airtest.core.api import *
from random import randint as r
from common import c, w, clink
from network import message_group
import common as cn


mission_name = "p22"

ini = cn.initial(name=mission_name, port="7555")
ini.start()
# script content
try:
    if cn.e(mission_name):
        clink(mission_name, "battle_confirm", th=0.9)
        c("battle_confirm")
    for times in range(1, 20):
        flag = True
        t1 = time.time()
        while flag:
            w("mission_start")
            c("base.")
            cn.man_repair(num=2)
            c("mission_start", wt=3)
            flag = cn.man_dec(rtb=4)
        c("base.")
        c("plan_mode", ranpos=False)
        c("step_1.")
        c("plan_go")
        cn.PAUSE_TIME = 30
        cn.progress_bar("plan_mode", times)
        c("step_2.", cp=True, wt=0.5)
        c("plan_mode", ranpos=False)
        c("step_3.", wt=1)
        c("step_4.")
        c("plan_go")
        cn.PAUSE_TIME = 120
        cn.progress_bar("plan_mode", times)
        clink("mission_end")
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
