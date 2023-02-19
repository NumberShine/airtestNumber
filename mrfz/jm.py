# -*- encoding=utf8 -*-
__author__ = "Number‘s Laptop"

from airtest.core.api import *
from common import c, e
from network import message_group, ocr_str
import common as cn
import time
# from pid import getport2
import math
from assignment.qtl import qtl_main


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


if __name__ == "__main__":
    print(os.getcwd())
    hcy = eval(input("当前石头数量："))
    mission_name = "qtl"
    ini = cn.initial(name=mission_name, chdir=2)
    ini.start()
    cn.clink("jm_start", "o_sb")
    qtl_main(hcy)
    # os.system('''start cmd /c"python %s"''' % "mrfz_gj.py")
