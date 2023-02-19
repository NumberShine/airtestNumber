# -*- encoding=utf8 -*-
__author__ = "Number‘s Laptop"

from airtest.core.api import *
from common import c, e
from network import message_group, ocr_str
import common as cn
import time


# from pid import getport2


def find_square():
    while e("square"):
        time.sleep(0.5)


def tx_ocr():
    msg = ["sample"]
    while "/" not in msg[0]:
        msg = ocr_str("qtl")
    a = msg[0].split("/")
    a.append(msg[1])
    msg_1 = []
    for _ in a:
        msg_1.append(abs(int(_)))
    return msg_1


# print(os.getcwd())

mission_name = "qyj"
ini = cn.initial(name=mission_name, chdir=2)
ini.start()
pt = 0
round_times = 0
consume = 0
consume_target = eval(input("欲消耗几次药剂："))

try:
    while 1:
        try:
            tx = tx_ocr()
            print("----------"
                  "\n当前体力:%s"
                  "\n体力上限:%s"
                  "\n每关消耗体力:%s"
                  "\n----------" % (tx[0], tx[1], tx[2]))
            time.sleep(2)
        except SyntaxError:
            print("ocr识别出错，请手动输入")
            tl = eval(input("欲消耗体力"))
            xh = eval(input("每关消耗体力"))
            tx = [tl, xh]

        if tx[0] < tx[1]:
            t = time.time()

        cn.clink("daili")
        while tx[0] - tx[2] > 0:
            round_times += 1
            cn.clink("o_sb", "o_sr", fc=False, th=0.8)
            c("o_sr", fc=False)
            cn.progress_bar("cash", round_times)
            if tx[0] >= tx[1]:
                t = time.time()
            tx[0] = tx[0] - tx[2]
            c((587, 261), wt=3, fc=False)
            if tx[0] < tx[1]:  # 小于体力上限
                pt = pt + time.time() - t
                t = time.time()
            if pt >= 360:
                tx[0] += 1
                pt -= 360
                print("体力 +1")
            print("当前体力：%s" % tx[0])

        if consume >= consume_target:
            break

        while 1:
            ps = e("o_sb")
            if ps:
                c(ps)
            if e("o_sr"):
                c("o_sr", fc=False)
                cn.progress_bar("cash", round_times)  # 说明体力未消耗完全，应继续消耗
                c((587, 261), wt=3, fc=False)
            if e("yj_confirm", th=0.8):
                break
        c("yj_confirm")
        consume += 1
        cn.w("o_sb")


except Exception as exc:
    message_group(["qyj", round_times], exc, mode="fail")

if round_times > 2:
    message_group(["qyj", round_times], mode=1)
    print(1)

os.system('''start cmd /k"python %s"''' % "mrfz_gj.py")

os.popen('taskkill.exe /pid:' + str(os.getppid()))  # 真的难
