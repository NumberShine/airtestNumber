# -*- encoding=utf8 -*-
__author__ = "Number‘s Laptop"

from airtest.core.api import *
from common import c, e, p, w
from network import message_group, ocr_str, send_notice
import common as cn
import time
import numpy as np
from mrfz_common.mrfz_common import search, quickswipe, snapcheck, distance, average_gray_scale, comp_com
import random as r
import network
import datetime
from asst import Asst, Message


def credit_check():

    if not e("terminal"):
        cn.clink("quick_bar", "quick_base", repeat=10)
        c("quick_main")
    cn.clink("friend_1", "friend_2")
    cn.clink("friend_2", "base_visit")
    cn.clink("base_visit", "credit_obtain", wt=5)
    cn.clink("credit_obtain", wt=3, rgb=True, th=0.5)
    cn.clink("quick_bar", "quick_store")
    cn.clink("quick_store", "credit_store")
    cn.clink("credit_store", "credit_stored")
    cn.clink("credit_obtain_2")
    cn.clink((930,66), "credit_obtained", wt=2)
    garbage = cn.fa("credit_empty")
    garbage = np.append(garbage, cn.fa("c99_mid"), axis=0)
    garbage = np.append(garbage, cn.fa("c99_small"), axis=0)
    garbage = np.append(garbage, cn.fa("expedited_plan"), axis=0)

    for i in range(0, 2):
        for j in range(0, 5):
            flag = 1
            pos = (205 + 377 * j, 412 + 382 * i)
            for garb in garbage:
                if distance(pos, garb) < 100:
                    flag = 0
                    break
            if flag:
                cn.clink(pos, "credit_buy")
                c("credit_buy")

    dt = datetime.datetime.now()
    f = open(cn.project_pos + "save_data/today.txt", "a+")
    f.write(dt.strftime('%j') + "\n")
    f.close()
    cn.clink((930, 66), "credit_obtained", wt=2)
    cn.clink("quick_bar", "quick_base", repeat=10)
    c("quick_main")


def assignment_obtain():
    if not e("terminal"):
        cn.clink("quick_bar", "quick_base", repeat=10)
        cn.clink("quick_main", "terminal")
    if e("assignment_complete"):
        c("assignment", wt=1)
        cn.clink("assignment_collect", wt=1)
        cn.clink((295,154), "back")
        cn.clink("weekly_assignment", wt=1)
        cn.clink("assignment_collect", wt=1)
        cn.clink((295, 154), "back")
    cn.clink("back", "terminal")

