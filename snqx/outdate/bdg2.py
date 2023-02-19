# -*- encoding=utf8 -*-
__author__ = "Number‘s Laptop"

from airtest.core.api import *
from common import c
from common import w
import common as cn
cn.start("bdg2", port="7555")

# script content
print("start...")
try:
    for times in range(0, 10):
        t1 = time.time()
        flag = True
        cn.clink(name1="bdg2", name2="battle_confirm", wt=0.5, fc=False)
        c("battle_confirm", fc=False)
        while flag:
            flag = cn.man_dec(name="bdg2", rtb=2)
        w("mission_start")
        c("airport_1.")
        c("confirm")
        c("mission_start", wt=3)
        if times % 2 == 0:
            c("airport_1.", times=2)
            c("supply")
        else:
            c("airport_1.")
        c("plan_mode", ranpos=False)
        c("step_1.")
        c("plan_go", wt=3)
        time.sleep(70)
        w("plan_mode", to=300, wt=2, ct=2)
        cn.clink("round_end")
        w("mission_finish", to=60, interval=5)
        c("middle.", times=5, interval=0.5, wt=3)
        print("全程所用时间：{:.2f}".format(time.time()-t1))
except OSError:
    print("连接出错")


 # generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath=True)3