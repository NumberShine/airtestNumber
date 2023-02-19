# -*- encoding=utf8 -*-
__author__ = "Number‘s Laptop"

from airtest.core.api import *
from common import c, e, w
import common as cn
from network import message_group, ocr_str
from snqx import daily as da
from datetime import datetime
import psutil as pt


def simulator_boot():
    flag = 0
    pids = pt.pids()
    for pid in pids:
        try:
            p = pt.Process(pid)
            if p.name() == "NemuHeadless.exe":
                flag = 1
                break
        except pt.NoSuchProcess:
            continue

    if flag == 0:
        print("MuMu模拟器启动")
        os.popen("start F:/ksdler/emulator/nemu/EmulatorShell/NemuPlayer.exe")
        time.sleep(15)


mission_name = "monitor_snqx"
ST.FIND_TIMEOUT = 15
TODAY_FLAG = False
def monitor_begin():
    global mission_name
    global TODAY_FLAG
    while 1:
        try:
            simulator_boot()
            ini = cn.initial(name=mission_name, add_para="t")
            ini.start()
            e("main_name")
        except Exception as eee:
            print(eee)
            time.sleep(3)
            os.system('''start cmd /k"python monitor_snqx.py"''')
            os.popen('taskkill.exe /pid:' + str(os.getppid()))
            exit(1)
        else:
            break


def timer_ocr():
    timer = []
    cn.clink("timer_1", "main_msg")
    time_total = ocr_str("hq", length=8)
    print(time_total)
    for time_str in time_total:
        tsp = time_str.split(":")
        timer.append(int(tsp[0]) * 3600 + int(tsp[1]) * 60 + int(tsp[2]))
    timer.sort()
    return timer


def support_check():
    global flag
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


def daytime_fetch():
    global TODAY_FLAG
    dt = datetime.now()
    f = open(cn.project_pos + "save_data/today.txt", "a+")
    f.seek(0)
    data = f.readlines()
    date_dif = int(dt.strftime('%j')) - int(data[-1])
    f.close()
    if date_dif != 0:
        print("daily_work")
        TODAY_FLAG = False
        f = open(cn.project_pos + "snqx/mission_ini/time/wk_log.txt", "w")
        f.close()
        return False
    else:
        TODAY_FLAG = True
        f.close()
    return True

def daytime_set():
    dt = datetime.now()
    f = open(cn.project_pos + "save_data/today.txt", "a+")
    f.write(dt.strftime('%j') + "\n")
    f.close()

def ini_clear():
    a = os.listdir(cn.project_pos + "snqx/mission_ini/")
    for name in a:
        if ".txt" not in name:
            continue
        f = open(cn.project_pos + "snqx/mission_ini/" + name, "a+")
        f.write("0\n")
        f.close()


def boot():
    global TODAY_FLAG
    try:
        stop_app("com.sunborn.girlsfrontline.cn")
        start_app("com.sunborn.girlsfrontline.cn")
        ini_clear()
        time.sleep(5)
    except TargetNotFoundError:
        boot()
        return 0
    c("boot_start")
    w("boot_eye")
    c("middle.", wt=4, fc=False)
    try:
        w("boot_square", fc=False, to=10)
        c("boot_square", fc=False)
        c("boot_confirm", fc=False)
    except TargetNotFoundError:
        cn.log_out("nsqure")
    pos = e("mima")
    if pos:
        c(pos, fc=False)
        text("Num15316107907")
        try:
            c("login", fc=False)
        except TargetNotFoundError:
            a = 0
    time.sleep(20)
    if not TODAY_FLAG:
        try:
            cn.clink("detail_back", "main_battle", repeat=10)
        except TargetNotFoundError:
            print("-" * 20)
    da.support_check(to=5)


def main():
    monitor_begin()
    while not daytime_fetch() or not e("main_name", th=0.8):
        try:
            boot()
        except TargetNotFoundError:
            continue
        else:
            daytime_set()
    if not TODAY_FLAG:
        da.daily_work()
    global flag
    flag = 0
    hang_time = 0
    try:
        while flag <= 99:  # support_check内+1
            while not daytime_fetch():
                try:
                    boot()
                except TargetNotFoundError:
                    continue
                else:
                    daytime_set()
                da.daily_work()
            da.daily_patrol()
            t1 = time.time()
            timer = timer_ocr()
            cn.PAUSE_TIME = [timer[0] + min(cn.ranln(12) + 3, 0.1 * timer[0])]
            cn.progress_bar(False, flag, gap=7000)
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
    except Exception as exc:
        context = [mission_name, flag]
        message_group(context, exc, mode="fail")
        print("\n"*3)
        print(exc)
    else:
        message_group(context, mode=1)
        # os.popen('taskkill.exe /pid:' + str(os.getppid()))


if __name__ == "__main__":
    main()
