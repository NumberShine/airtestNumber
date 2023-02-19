# -*- encoding=utf8 -*-
__author__ = "Number‘s Laptop"

from airtest.core.api import *
from random import randint as r
from common import c, w, clink
from network import message_group

import common as cn

from snqx import daily as da

mission_name = "134"
NoBe = eval(input("请输入需求模式\n1.做日常\n2.拖尸\n"))
if NoBe == 1:
    NoB = r(6, 8)
else:
    NoB = r(20, 30)
ini = cn.initial(name=mission_name, port="7555", add_para=[NoBe])
ini.start()
# script content
cn.PAUSE_TIME = [220]
mini = cn.mission_ini("134", "normal_mission", auto_supply=0)
try:
    for times in range(1, NoB+1):
        t1 = time.time()
        clink("134", "normal_mission", th=0.9)
        c("normal_mission")
        cn.man_dec("134", rtb=1)
        w("mission_start")
        c("base_1.")
        if cn.change(name1="hk416", name2="vec",filter=["ar", "sm", "max"], corr=True):
            c("base_1.")
        cn.man_repair()
        c("airport_1.")
        if not mini:
            c("echelon_choose")
        c("confirm")
        c("mission_start", wt=3)
        c("airport_1.", times=2)
        c("supply")
        c("base_1.")
        c("plan_mode", ranpos=False)
        c("step_1.")
        c("step_2.")
        c("step_3.")
        if r(1, 4) > 1:
            c("step_4.")
        elif r(1, 4) > 1:
            c("step_2.")
        else:
            c("step_1.")
        c("plan_go")
        cn.progress_bar("mission_finish", times)
        c("middle2.", times=4, interval=0.5, wt=2)
        c("middle2.", times=4, interval=0.5, wt=2)
        context = [mission_name, times, time.time() - t1]
        cn.fileopr(context)
        """print("延迟检测平均值:%s 最大值：%s 总值：%s" % (np.mean(cn.delay_collect),
                                           max(cn.delay_collect), np.sum(cn.delay_collect)))"""
except Exception as exc:
    context = [mission_name, times, time.time() - t1]
    message_group(context, exc, mode="fail")

else:
    message_group(context, mode=1)
    da.daily_reset()
    os.system("start cmd /k python monitor_snqx.py")
    os.popen('taskkill.exe /pid:' + str(os.getppid()))
