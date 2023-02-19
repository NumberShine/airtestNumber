# -*- encoding=utf8 -*-
__author__ = "Number‘s Laptop"

from airtest.core.api import *
from common import c
from network import message_group, ocr_str
import common as cn
import time
# from pid import getport2
from assignment.qtl import qtl_main
import datetime
from assignment.mrfz_boot import mrfz_boot
from assignment import Meo_d as md

print(os.getcwd())
mrfz_boot()
COUNT = 0
TARGET_CLOCK = 0
ALERT_CLOCK = 0
TODAY_FLAG = False


def tl_resource():
    wd = datetime.date.today().weekday()
    wd = 9
    dt = datetime.datetime.now()
    if wd in [1, 3, 5, 6] and int(dt.strftime('%H')) > 4:
        cn.clink("resource_collection", "cash_ticket")
        cn.clink("cash_ticket", "ticket_5")
        cn.clink("ticket_5", "o_sb")
    else:
        cn.clink("last_battle", "o_sb", th=0.7)


def tl_check(ct=10):
    for i in range(0, ct):
        tl1 = int(ocr_str("tl")[0])
        if tl1 <= 35:
            time.sleep(1)
            tl2 = int(ocr_str("tl")[0])
            if tl1 == tl2:
                return tl1
            else:
                cn.log_out("体力比对出错")
        else:
            return tl1


def tl_consumption():
    global TARGET_CLOCK
    cn.clink("back", "terminal", th=0.8, repeat=10)
    if time.time() > TARGET_CLOCK:
        tl = tl_check()
        if tl <= 35:
            TARGET_CLOCK = time.time() + (36 - tl) * 360
        else:
            TARGET_CLOCK = time.time() + (100 - tl) * 360

    if time.time() >= TARGET_CLOCK:
        cn.clink("terminal", "quick_bar")
        tl_resource()
        tl = qtl_main()
        TARGET_CLOCK = time.time() + (100 - tl) * 360
        c("quick_bar")
        cn.clink("quick_base", "quick_bar", wt=8, repeat=8, least=1)
    else:
        cn.clink("base_entrance", "quick_bar", wt=8, repeat=8)


try:
    while 1:
        COUNT += 1

        for i in range(0, 11):
            try:
                md.daily_work()
                tl_consumption()
                detect_interval = md.colloct_resource()
                cn.progress_bar_mrfz(False, COUNT, detect_interval, TARGET_CLOCK, gap=200)
                break
            except TargetNotFoundError as a:
                mrfz_boot(connect=0)
            except ConnectionResetError:
                os.system('''start cmd /k"python %s"''' % "mrfz_gj.py")

                os.popen('taskkill.exe /pid:' + str(os.getppid()))  # 真的难
            finally:
                if i == 10:
                    raise TimeoutError("Reboot too many")


except Exception as exc:
    print(exc)
    message_group(["gj", COUNT], exc, mode="fail")
