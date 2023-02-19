# -*- encoding=utf8 -*-
__author__ = "Number‘s Laptop"

from airtest.core.api import *
from random import randint as r
from common import c, w, e
import common as cn

cn.start(name="kw", port="7555")

a = 1
while 1:
    t1 = time.time()
    w("kw", to=20, interval=0.5)
    if not e("coin"):
        break
    cn.clink(name1="kw", name2="battle_confirm", wt=0.5, fc=False)
    c("battle_confirm", fc=False)
    cn.man_dec(name="bdg2", rtb=0)
    w("mission_start")
    c("base.")
    c("confirm")
    c("mission_start", wt=3)
    c("base.", times=2)
    c("supply")
    c("plan_mode", ranpos=False)
    if r(1, 10) > 5:
        c("step_1.")
        c("step_2.")
        c("step_3.")
    else:
        c("step_3.")
        c("step_2.")
        c("step_1.")
    c("base.")
    c("plan_go")
    cn.progress_bar("mission_finish")
    c("middle.", times=5, interval=0.8)
    a += 1
    cn.fileopr("kw", [time.time() - t1, a])
