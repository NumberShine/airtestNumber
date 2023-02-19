# -*- encoding=utf8 -*-
__author__ = "Number‘s Laptop"

from airtest.core.api import *
from random import randint as r
from common import c, w, clink
from network import message_group
import common as cn


mission_name = "shoulei"

ini = cn.initial(name=mission_name, port="7555")
ini.start()
# script content
try:
    for times in range(1, 50):
        flag = True
        t1 = time.time()
        w("mission_start")
        c("base.")
        c("confirm")
        c("mission_start", wt=3)
        clink("detail_back", wt=2)
        c("base.")
        c("plan_mode", ranpos=False)
        c("step_1.")
        c("plan_go")
        cn.PAUSE_TIME = 5
        cn.progress_bar("plan_mode", times)
        c("plan_mode", ranpos=False)
        c("step_2.", wt=1)
        c("plan_go")
        cn.PAUSE_TIME = 23
        cn.progress_bar("pick", times)
        c("pick")
        clink("mission_end", "mission_restart")
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
