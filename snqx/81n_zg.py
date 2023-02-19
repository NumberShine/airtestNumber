# -*- encoding=utf8 -*-
__author__ = "Number‘s Laptop"

from airtest.core.api import *
from random import randint as r
from common import c, w, clink
import common as cn
from network import message_group


mission_name = "81n_zg"
argp = cn.arg_analysis()
if argp:
    air_atk = eval(argp[0])
else:
    air_atk = int(eval(input("请输入妖精指令："))/15)
ini = cn.initial(name=mission_name, port="7555", chdir=1, add_para=[air_atk*15])
ini.start()

try:
    for times in range(1, air_atk+1):
        flag = True
        t1 = time.time()
        if r(1, 100) > 37:
            w("mission_start")
            while flag:
                c("airport_1.")
                c("confirm")
                c("mission_start", wt=3)
                flag = cn.equ_dec(rtb=1)
            clink("plan_mode", "plan_go")
            c("airport_1.")
            if r(1, 5) > 3:
                c("step_1.")
            else:
                c("step_2.")
            c("step_4.")
            c("plan_go")
            cn.progress_bar("plan_mode", times)
        else:
            w("mission_start")
            while flag:
                c("airport_2.")
                c("confirm")
                c("mission_start", wt=3)
                flag = cn.equ_dec(rtb=1)
            clink("plan_mode", "plan_go")
            c("airport_2.")
            if r(1, 5) > 3:
                c("step_1.")
            else:
                c("step_2.")
            c("step_3.")
            c("plan_go")
            cn.progress_bar("plan_mode", times)
        c("mission_end")
        c("mission_restart")
        context = [mission_name, times, time.time() - t1]
        cn.fileopr(context)
except TargetNotFoundError:
    context = [mission_name, times, time.time() - t1]
    message_group(context, mode="fail")
    print("没找到")
else:
    message_group(context, mode=1)
