# -*- encoding=utf8 -*-
__author__ = "Number‘s Laptop"

from airtest.core.api import *
from random import randint as r
from common import c, w, clink, e
import common as cn
import warnings
from network import message_group

warnings.filterwarnings("ignore")
mission_name = "81n"
ini = cn.initial(name=mission_name, port="7555", chdir=1)
ini.start()

cn.PAUSE_TIME = [140]
error_times = 0

if e(mission_name):
    clink(mission_name, "normal_mission", th=0.9)
    c("normal_mission", fc=False)
    cn.equ_dec(rtb=1)
for times in range(1, 99):
    try:
        flag = True
        process_flag = 0
        t1 = time.time()
        if r(1, 100) > 27:
            w("mission_start")
            c("airport_1.")
            cn.change(name1="zms", name2="zml", filter=["ar", "max"], des=True)
            process_flag += 1  # 1
            c("airport_1.", wt=0.5)
            clink("confirm", least=1)
            c("airport_2.", wt=0.5)
            clink("confirm", least=1)
            c("airport_3.", wt=0.5)
            clink("confirm", least=1)
            process_flag += 1  # 2
            c("mission_start", wt=3)
            if cn.equ_dec(rtb=1):
                continue
            c("airport_2.")
            clink("airport_2.", "supply")
            c("supply")
            clink("airport_2.", "retreat")
            clink("retreat", "confirm")
            c("confirm", wt=1.5)
            process_flag += 1
            c("plan_mode", ranpos=False)
            c("airport_1.", wt=0.5)
            if r(1, 5) > 3:
                c("step_1.")
            else:
                c("step_2.")
            c("airport_2.")
            c("plan_go")
            print("错误次数：%d" % error_times)
            cn.progress_bar("plan_mode", times)
            c("airport_2.")
        else:
            w("mission_start")
            c("airport_2.")
            cn.change(name1="zms", name2="zml", filter=["ar", "max"], des=True)
            process_flag += 1
            c("airport_2.", wt=0.5)
            clink("confirm", least=1)
            c("airport_1.", wt=0.5)
            clink("confirm", least=1)
            c("airport_3.", wt=0.5)
            clink("confirm", least=1)
            process_flag += 1
            c("mission_start", wt=3)
            if cn.equ_dec(rtb=1):
                continue
            c("airport_1.")
            clink("airport_1.", "supply")
            c("supply")
            clink("airport_1.", "retreat", wt=0.5)
            clink("retreat", "confirm")
            c("confirm", wt=1.5)
            process_flag += 1
            c("plan_mode", ranpos=False)
            c("airport_2.")
            if r(1, 5) > 3:
                c("step_1.")
            else:
                c("step_2.")
            c("airport_1.")
            c("plan_go")
            print("错误次数：%d" % error_times)
            cn.progress_bar("plan_mode", times)
            c("airport_1.")
        c("retreat")
        c("confirm")
        clink("mission_end", "mission_restart")
        c("mission_restart")
        context = [mission_name, times, time.time() - t1]
        cn.fileopr(context)
        cn.exp_dec(name="81n", rtb=2)
    except TargetNotFoundError:
        try:
            error_times += 1
            print("没找到, 执行纠错模式%d" % process_flag)
            if process_flag == 0:
                clink("echelon_group")
                clink("rte", "back")
                clink("back", "mission_start")
            elif process_flag == 1:
                clink("confirm")
                clink("rtm")
                c("81n")
                c("normal_mission")
            elif process_flag == 2:
                context = [mission_name, times - 1, time.time() - t1]
                message_group(context, mode="fail")
                exit(1)
            elif process_flag == 3:
                clink("cancle")
                clink("confirm")
                clink("mission_end", "mission_restart")
                c("mission_restart")
        except:
            context = [mission_name, times - 1, time.time() - t1]
            message_group(context, mode="fail")
            exit(1)
    except:
        context = [mission_name, times - 1, time.time() - t1]
        message_group(context, mode="fail")
        exit(1)

print("错误次数%s" % error_times)
context = [mission_name, times, error_times]
message_group(context, mode=1)
os.popen('taskkill.exe /pid:' + str(os.getppid()))  # 真的难
