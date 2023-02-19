# -*- encoding=utf8 -*-
__author__ = "Number‘s Laptop"

from airtest.core.api import *
from common import c
from common import w
import common as cn

cn.start(name="gpy2", port="7555", add=True)
# script content
print("start...")
for times in range(0, 31):
    flag = True
    while flag:
        w("mission_start")
        c("base_1.")
        c("confirm")
        c("mission_start", wt=3)
        flag = cn.man_dec(name="gpy2", rtb=2)
    c("base_1.", times=2)
    c("supply")
    c("plan_mode", ranpos=False)
    c("step_1.")
    c("plan_go", wt=3)
    time.sleep(20)
    w("plan_mode", to=300, interval=2, wt=2)
    c("mission_end")
    c("mission_restart")
