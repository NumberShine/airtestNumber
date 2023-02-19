# -*- encoding=utf8 -*-
__author__ = "Number‘s Laptop"

from airtest.core.api import *
from common import c, e, w
import common as cn
from network import message_group, ocr_str
from control import control
from snqx.outdate import snqx_boot as sb

mission_name = "support"
con = control(1)
ini = cn.initial(name=mission_name)
ini.start()
con.refresh()
ST.FIND_TIMEOUT = 15


def hq_check():
    stats = con.check()
    for key in stats.keys():
        if stats[key] == "1":
            return 1
    return 0


def hang():
    global hang_time
    t1 = time.time()
    if hq_check():
        con.file_change(2)
        print("----------------\n   support 挂起\n----------------")
        while hq_check():
            time.sleep(5)
    con.file_change(1)
    hang_time = time.time() - t1


def timer_ocr():
    timer = []
    cn.clink("timer", "timer_1")
    time_total = ocr_str("hq", length=8)
    print(time_total)
    for time_str in time_total:
        tsp = time_str.split(":")
        timer.append(int(tsp[0]) * 3600 + int(tsp[1]) * 60 + int(tsp[2]))
    timer.sort()
    return timer


def support_check():
    global flag
    global con
    while 1:
        try:
            c("L_support")
            c("middle.")
            c("confirm")
            flag += 1
        except TargetNotFoundError:
            boot()
            continue
        else:
            break


def boot():
    pos = e("back")
    if pos:
        cn.clink("quick_bar", "rtb")
        c("rtb")
    else:
        start_app("com.sunborn.girlsfrontline.cn")
        time.sleep(15)
        c("boot_start")
        w("boot_eye")
        c("middle.", wt=8, fc=False)
        pos = e("boot_confirm")
        if pos:
            c("boot_square", fc=False)
            c(pos, fc=False, wt=2)
        pos = e("mima")
        if pos:
            c(pos, fc=False)
            text("Num15316107907")
            c("login", fc=False)
        time.sleep(20)
        sb.login_today()


def main():
    global flag
    flag = 0
    times = 0
    hang_time = 0

    try:
        while flag <= 99:  # support_check内+1

            t1 = time.time()
            timer = timer_ocr()
            con.hq_release()
            cn.PAUSE_TIME = [timer[0] + min(cn.ranln(12) + 3, 0.1 * timer[0])]
            cn.progress_bar(False, flag, gap=7000)
            hang()
            support_check()
            for i in range(0, 3):
                if timer[i + 1] - timer[i] <= 120 + hang_time:
                    print("间距小 时长为： %.2f" % (timer[i + 1] - timer[i]))
                    cn.PAUSE_TIME = [timer[i + 1] - timer[i] + min(cn.ranln(5) + 3, 0.1 * (timer[i + 1] - timer[i]))]
                    cn.progress_bar(False, flag, gap=100)
                    support_check()
                else:
                    break
            context = [mission_name, flag, time.time() - t1]
            message_group(context, mode=8)
            cn.fileopr(context)
    except TargetNotFoundError:
        context = [mission_name, flag]
        message_group(context, mode="fail")
        print("没找到")
    else:
        message_group(context, mode=1)
        # os.popen('taskkill.exe /pid:' + str(os.getppid()))


if __name__ == "__main__":
    main()
