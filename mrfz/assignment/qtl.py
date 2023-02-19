# -*- encoding=utf8 -*-
__author__ = "Number‘s Laptop"

from airtest.core.api import *
from common import c, e
from network import message_group, ocr_str
import common as cn
import time
# from pid import getport2
import math


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


def qtl_main(hcy=9999):
    try:
        tx = tx_ocr()
        print("----------"
              "\n欲消耗体力:%s"
              "\n体力上限:%s"
              "\n每关消耗体力:%s"
              "\n----------" % (tx[0], tx[1], tx[2]))
        time.sleep(2)
    except SyntaxError:
        print("ocr识别出错，请手动输入")
        tl = eval(input("欲消耗体力"))
        xh = eval(input("每关消耗体力"))
        tx = [tl,xh]

    print(os.getcwd())
    pt = 0
    count = 0
    if hcy != 9999:
        maxbattle = math.ceil((1800-hcy)/370)
    else:
        maxbattle = 9999

    if tx[0] < tx[1]:
        t = time.time()
    cn.clink("daili")
    while tx[0] - tx[2] >= 0 and maxbattle > count:
        count += 1
        cn.clink("o_sb", "o_sr", fc=False, th=0.8)
        c("o_sr", fc=False)
        if hcy != 9999:
            cn.PAUSE_TIME = [15*60]
            cn.progress_bar("jm_finish", count)
            cn.clink((50, 360), "jm_start", wt=2)
            cn.clink("jm_start", "o_sb")
        else:
            cn.progress_bar("cash", count)
            c((587, 261), wt=3, fc=False)
        tx[0] = tx[0] - tx[2]
        if tx[0] + tx[2] >= tx[1] > tx[0]:
            t = time.time()
        if tx[0] < tx[1]:
            pt = pt + time.time() - t
            t = time.time()
        if pt >= 360:
            tx[0] += 1
            pt -= 360
            print("体力 +1")
        print("当前体力：%s" % tx[0])

    if count > 2:
        message_group(["qtl", count], mode=1)
        print(1)
    return tx[0]