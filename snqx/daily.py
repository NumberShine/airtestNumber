# -*- encoding=utf8 -*-
__author__ = "Number‘s Laptop"

from airtest.core.api import *
from random import randint as r
from common import c, w, clink, e
from datetime import datetime
import common as cn
from snqx import monitor_snqx as ms


def located():
    w("main_battle")


def support_check(to=2):
    try:
        while 1:
            w("L_support", to=to, interval=2)
            c("middle.")
            c("confirm")
    except TargetNotFoundError:
        print("\n-- support 检查完毕 --")


def deal_build_depart():
    print("\n-- 进入拆解部分 --\n")
    support_check()
    try:
        if e("main_battle"):
            support_check()
            c("main_factory", wt=3)
        elif e("retire"):
            c("retire", th=0.8)
        else:
            c("quick_bar")
            c("quick_fac", wt=3)
        c("retire", th=0.8)
        while 1:
            c("select_equip")
            c("ai_select", ranpos=False, times=3)
            if e("ai_select"):
                clink("back", "retire")
            else:
                break
        c("depart")
        c("select_equip")
        c("filter_by")
        c("f_4s")
        c("f_3s")
        c("select_confirm", ranpos=False)
        if not e("depart_empty"):
            for y in range(0, 2):
                for x in range(0, 6):  # 181 305
                    cn.point["equip"] = cn.deepcopy(cn.point["equip_start"])
                    cn.point["equip"][0] += x * 181
                    cn.point["equip"][1] += y * 305
                    c("equip.", fc=False, wt=0)
            c("depart_confirm")
            c("depart")
            c("confirm", wt=0.5)
        else:
            c("back")

        c("select_doll", wt=2)
        if not e("filter_by"):
            return 0
        c("ai_select", times=3, interval=1)
        if e("ai_select"):
            clink("back", "retire")
            return 0

        c("depart", wt=0.5)
        c("select_doll", wt=2)
        if e("filter_by"):
            clink("back", "retire")
            return 0
        for y in range(0, 1):
            for x in range(0, 6):  # 181 305
                cn.point["equip"] = cn.deepcopy(cn.point["equip_start"])
                cn.point["equip"][0] += x * 181
                cn.point["equip"][1] += y * 305
                c("equip.", fc=False, wt=0)
        c("depart_confirm")
        c("depart")
        c("confirm", wt=0.5)
    except TargetNotFoundError:
        print("装备拆解出错，重试")
        c("quick_bar")
        c("rtb")
        deal_build_depart()


def deal_build():
    print("\n-- 进入建造部分 --\n")
    support_check()
    if e("main_battle"):
        c("main_factory", wt=3)
    elif e("pro_man_block"):
        c("pro_man_block")
    else:
        c("quick_bar")
        c("quick_fac", wt=3)
    w("quick_bar")
    if e("collect_all"):
        c("collect_all", wt=3)
        clink("pro_confirm")
        clink("middle1.", "quick_bar")
    c("man_pro", wt=1)
    clink("man_pro_2", "pro_confirm", wt=1)
    clink("pro_confirm", least=1)
    clink("pro_equ_block", "equ_mark")
    if e("collect_all"):
        c("collect_all", wt=3)
        clink("pro_confirm")
        clink("middle1.", "quick_bar")
    c("equ_pro")
    c("man_pro_2")
    c("pro_confirm")
    c("heavy_equ_pro")
    c("confirm")
    c("man_pro_2")
    clink("pro_confirm", least=1)


def deal_msg():
    print("\n-- 进入情报部分 --\n")
    support_check()
    if e("main_battle"):
        clink("timer_1")
        c("main_msg", wt=3)
    else:
        c("quick_bar")
        c("quick_msg", wt=3)
    w("quick_bar")
    pos = e("msg_collect")
    if pos:
        c(pos)
        c("msg_close")
    clink("msg_mac", "msg_mark")
    pos = e("msg_all")
    if pos:
        c(pos)
        clink("pro_confirm", "msg_result", th=0.8, wt=2)
        c("middle.", times=2)
    clink("msg_trans_1", "pro_confirm", th=0.8)
    c("pro_confirm", th=0.8)
    clink("white_back")


def deal_room():
    print("\n-- 进入宿舍部分 --\n")
    support_check()
    if e("visit_0", th=0.8):
        a = 0
    elif e("main_battle"):
        clink("timer_1")
        c("main_room")
    else:
        c("quick_bar")
        c("quick_room")
    w("quick_bar")
    clink("battery")
    clink("visit_0", "visit_friend")
    c("visit_friend")
    c("visit_1")
    w("visit_next")
    for i in range(0, 10):
        try:
            c("like", fc=False, th=0.8)
        except TargetNotFoundError:
            a = 0
        c("visit_next", wt=1, th=0.8, fc=False, rgb=True)
    w("visit_next")
    clink("visit_back")


def deal_task():
    print("\n-- 进入任务部分 --\n")
    support_check()
    if e("main_battle"):
        c("main_task", wt=3)
    else:
        c("quick_bar")
        swipe((193, 371), (1000, 430))
        time.sleep(2)
        c("quick_task", wt=3)
    w("quick_bar")
    c("collect_all")
    clink("back")
    w("main_name", th=0.8)


def deal_power():
    a = datetime.today()
    a = a.isoweekday()
    print("\n-- 进入动能部分 --\n")
    f = open(cn.project_pos + "snqx/mission_ini/time/power_time.txt", "a+")
    f.seek(0)
    t1 = time.time()
    t = f.readlines()
    # print(t1 - float(t[-1]))
    if (t1 - float(t[-1].rstrip())) < (3600 * 6):
        print("\n-- 未到动能时间 --\n")
        f.close()
        return 0
    if e("main_battle"):
        support_check()
        c("main_battle", wt=3)
    else:
        c("quick_bar")
        swipe((193, 371), (1000, 430))
        time.sleep(2)
        c("quick_battle", wt=3)
    w("quick_bar")
    c("moni")
    if a == 2 or a == 5 or a == 7:
        cn.PAUSE_TIME = [10]
        c("ziliao")
        c("gaoji")
        c("enter_battle")
        c("confirm")
        t1 = time.time()
        f.write("%.2f\n" % t1)
        f.close()
        w("ziliao_finish")
    else:
        cn.PAUSE_TIME = [60]
        c("yuntu")
        cn.mission_ini("suipian", cw=None)
        c("suipian")
        w("mission_start")
        c("base.")
        c("eche_8")
        c("confirm")
        c("mission_start")
        c("confirm", wt=3)
        t1 = time.time()
        f.write("%.2f\n" % t1)
        f.close()
        c("base.")
        c("plan_mode", ranpos=False)
        c("step_1.")
        c("plan_go")
        cn.progress_bar("suipian_finish", 0)
    c("middle.", times=3, wt=1)
    w("quick_bar")


def deal_rh_power():
    print("\n-- 进入融合动能部分 --\n")
    f = open(cn.project_pos + "snqx/mission_ini/time/rhpower_time.txt", "a+")
    f.seek(0)
    t1 = time.time()
    t = f.readlines()
    # print(t1 - float(t[-1]))
    if (t1 - float(t[-1].rstrip())) < (3600 * 6):
        print("\n-- 未到融合动能时间 --\n")
        f.close()
        return 0
    if e("rh"):
        a = 1
    elif e("main_name"):
        support_check()
        c("main_battle", wt=3)
    else:
        c("quick_bar")
        swipe((193, 371), (1000, 430))
        time.sleep(2)
        c("quick_battle", wt=3)
    cn.PAUSE_TIME = [20]
    c("rh")
    w("rh_mark")
    a = datetime.today()
    a = a.isoweekday()
    if a == 1 or a == 4:
        c("cj_1.")
    elif a == 2 or a == 5:
        c("cj_2.")
    else:
        c("cj_3.")
    c("chuji")
    c("confirm")
    t1 = time.time()
    f.write("%.2f\n" % t1)
    f.close()
    cn.progress_bar("mission_finish", 0)
    c("middle.", times=3, wt=1)
    w("quick_bar")


def main():
    c("visit_back")
    while 1:
        try:
            flag = eval(input("？："))
            if flag == 1:
                deal_build()
            elif flag == 2:
                deal_msg()
            elif flag == 3:
                deal_room()
            elif flag == 4:
                deal_task()
        except Exception as e:
            print(e)


def daily_work():
    f = open(cn.project_pos + "snqx/mission_ini/time/wk_time.txt", "a+")
    f.write(str(time.time()) + "\n")
    f.close()
    f = open(cn.project_pos + "snqx/mission_ini/time/wk_log.txt", "a+")
    f.seek(0)
    d = f.readlines()
    if not d:
        dd = 0
    else:
        dd = int(d[-1])
    try:
        if dd < 1:
            deal_build_depart()
            f.write("1\n")
        if dd < 2:
            deal_build()
            f.write("2\n")
        if dd < 3:
            deal_msg()
            f.write("3\n")
        if dd < 4:
            deal_room()
            f.write("4\n")
        if dd < 5:
            deal_task()
            f.write("5\n")
    except Exception as exc:
        f.close()
        daily_reset()
        daily_work()
    else:
        f.close()
        f = open(cn.project_pos + "snqx/mission_ini/time/wk_log.txt", "w")
        f.close()


def daily_reset():
    pos1 = e("main_name", th=0.8)
    pos2 = e("quick_bar")
    if pos1:
        support_check()
        return 0
    elif pos2:
        c(pos2)
        c("rtb", wt=2)
        support_check()
    else:
        ms.boot()


def daily_patrol():
    deal_power()
    deal_rh_power()
    f = open(cn.project_pos + "snqx/mission_ini/time/wk_time.txt", "a+")
    f.seek(0)
    q = f.readlines()
    f.close()
    if (time.time() - float(q[-1].rstrip())) > 3600 * 13:
        daily_work()
    daily_reset()


if __name__ == '__main__':
    mission_name = "daily"
    print("daily")
    ini = cn.initial(name=mission_name)
    ini.start()
    chose = eval(input("1. depart 2. build 3. msg 4. room 5. task 6.pw 7. rh?："))
    if chose == 1:
        deal_build_depart()
    elif chose == 2:
        deal_build()
    elif chose == 3:
        deal_msg()
    elif chose == 4:
        deal_room()
    elif chose == 5:
        deal_task()
    elif chose == 6:
        deal_power()
    elif chose == 7:
        deal_rh_power()
    os.popen('taskkill.exe /pid:' + str(os.getppid()))
