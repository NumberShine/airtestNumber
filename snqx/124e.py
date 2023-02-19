# -*- encoding=utf8 -*-
__author__ = "Number‘s Laptop"

from airtest.core.api import *
from random import randint as r
from common import c, w, clink
from network import message_group
import common as cn


mission_name = "124e"
argp = cn.arg_analysis()
if argp:
    NoBe = eval(argp[0])
else:
    NoBe = eval(input("请输入需求模式\n1.做日常\n2.拖尸\n"))
if NoBe == 1:
    NoB = r(6, 8)
else:
    NoB = r(20, 30)
ini = cn.initial(name=mission_name, port="7555", add_para=[NoBe])
ini.start()
# script content
pause_time = 100
time.sleep(10000)
try:
    for times in range(1, NoB+1):
        t1 = time.time()
        clink("mission_124e", "normal_mission", th=0.9)
        c("normal_mission")
        cn.man_dec("mission_124e", rtb=1)
        w("mission_start")
        c("airport_1.")
        cn.change(name1="hk416", name2="vec", filter=["ar", "sm"])
        c("airport_1.")
        cn.man_repair()
        c("base_1.")
        c("confirm")
        c("mission_start", wt=3)
        c("base_1.", times=2)
        clink("supply")
        c("airport_1.")
        c("plan_mode", ranpos=False)
        c("step_1.")
        c("step_2.")
        if r(1, 3) > 1:
            c("step_3.")
        elif r(1, 3) > 1:
            c("step_4.")
        else:
            c("step_5.")
        c("plan_go")
        cn.progress_bar("mission_finish", times)
        c("middle.", times=4, interval=0.5, wt=2)
        context = [mission_name, times, time.time() - t1]
        cn.fileopr(context)
        """print("延迟检测平均值:%s 最大值：%s 总值：%s" % (np.mean(cn.delay_collect),
                                           max(cn.delay_collect), np.sum(cn.delay_collect)))"""
except :
    context = [mission_name, times, time.time() - t1]
    message_group(context, mode="fail")
    print("没找到")
else:
    message_group(context, mode=1)

os.popen('taskkill.exe /pid:' + str(os.getppid()))
