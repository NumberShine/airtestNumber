# -*- encoding=utf8 -*-
__author__ = "Number‘s Laptop"

from airtest.core.api import *
from common import c, e
from network import message_group, ocr_str
import common as cn
import time
from pid import getport2


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


print(os.getcwd())
mission_name = "qtl"
ini = cn.initial(name=mission_name, port=getport2(), chdir=2)
ini.start()


tl = eval(input("欲消耗体力"))
xh = eval(input("每关消耗体力"))
tx = [tl,130,xh]

print(os.getcwd())

pt = 0
count = 0

if tx[0] < tx[1]:
    t = time.time()
cn.clink("daili")
while tx[0] - tx[2] >= 0:
    count += 1
    c("o_2sb", fc=False, th=0.8, times=2)
    cn.clink("o_3sb", fc=False, th=0.8)
    c("o_sr", fc=False)
    cn.progress_bar("exp", count)
    tx[0] = tx[0] - tx[2]
    if tx[0] + tx[2] >= tx[1] > tx[0]:
        t = time.time()
    c((587, 261), wt=3, fc=False)
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

os.popen('taskkill.exe /pid:' + str(os.getppid()))
