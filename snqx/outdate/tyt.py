# -*- encoding=utf8 -*-
__author__ = "Number‘s Laptop"

from airtest.core.api import *
from random import randint as r
from common import c, w, clink
from network import message_group
import common as cn

mission_name = "tyt"


def fd(a):
    t = 0.52 * a / 6
    if t == 0:
        t = 0.01
    print("t = %.2f gap = %s " % (t, a))
    c("fd.", dura=t, wt=1.5)


def up(a):
    t = 0.52 * a / 6
    if t == 0:
        t = 0.01
    print("t = %.2f gap = %s " % (t, a))
    c("fd.", dura=t, wt=1.5)


def down(a):
    t = 0.52 * a / 6
    if t == 0:
        t = 0.01
    print("t = %.2f gap = %s " % (t, a))
    c("fd.", dura=t, wt=1.5)


ini = cn.initial(name=mission_name, port="7555")
ini.start()

# script content
gap_list = []

mode = eval(input("mode="))
if mode == 1:
    while 1:
        fdp = eval(input("gap:"))
        if fdp == 7:
            break
        elif fdp == 8:
            gap_list.clear()
            continue
        fd(fdp)
        gap_list.append(fdp)

    f = open("tyt.txt", "w")
    for i in gap_list:
        f.write(str(i)+"\n")
else:
    f = open("tyt.txt", "r")
    gap_list = f.readlines()
    print(gap_list)
    for i in gap_list:
        fd(eval(i.rstrip()))
