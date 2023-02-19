from airtest.core.api import *
from random import randint as r
from random import uniform as u
from common import c, w
import common as cn
import AirThreading as at

cn.start(name="46", port="7555")


if __name__ == '__main__':
    for _ in range(0, 100):
        w("mission_start")
        c("airport_1.")
        c("confirm")
        c("base.")
        c("confirm")
        c("mission_start", wt=3)
        c("airport_1.")
        while not cn.e("plan_go"):
            c("plan_mode", ranpos=False)
        if r(0, 10) > 5:
            c("step_1.", wt=0.1)
            c("step_2.", wt=0.1)
        else:
            c("step_2.", wt=0.1)
            c("step_1.", wt=0.1)
        c("plan_go", wt=1)
        time.sleep(15)
        pro = at.pro_check(name="doll_recycle")
        pro.run()
        w("plan_mode", ct=3, wt=0)
        pro.stop()
        time.sleep(cn.ranln(2))
        while not cn.e("mission_restart"):
            c("mission_end", ranpos=False)
        c("mission_restart")
        print("完成第%s次" % _)
