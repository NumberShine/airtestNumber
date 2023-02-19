# -*- encoding=utf8 -*-
__author__ = "Number‘s Laptop"

from random import randint as r
from random import uniform as u
from airtest.core.api import *
import cv2
from airtest.cli.parser import cli_setup
from airtest.core.android.adb import ADB
import time
from math import log as logg
from datetime import datetime
import datetime
from copy import deepcopy

import AirtestIDE.airtest.core.android.adb
from network import message_group, send_notice
import logging
import numpy as np
from airtest.core.android.android import Android
import json

logger = logging.getLogger("airtest")
logger.setLevel(logging.ERROR)

filename = ""
png = {}
point = {}
ST.CVSTRATEGY = ["surf", "sift", "mstpl", "tpl", "brisk"]
ST.FIND_TIMEOUT_TMP = 0.2
ST.FIND_TIMEOUT = 20
PAUSE_TIME = [50]
HOUR_CLOCK = time.time()
delay_collect = []
project_pos = "D:/SynologyDrive/airtest_copy/"
Mission_Name = ""
file_path = ""

dev = None


def png_detail():
    global png
    global file_path
    os.chdir(file_path)
    with open("png/png_detail.txt", "a+") as dlt:
        dlt.seek(0)
        for line in dlt:
            line = line.replace("touch", "").replace("Template", "") \
                .replace("(", "").replace(")", "").replace('"', "") \
                .replace("record_pos", "").replace("resolution", "") \
                .replace(",", "").replace("=", "").replace(".png", "")
            line = line[1:]
            xline = line.split()
            png[str(xline[0])] = [xline[1], xline[2], xline[3], xline[4]]


def point_detail(name):
    global point
    global file_path
    os.chdir(file_path)
    if name == "spl":
        return 0
    with open("file/" + name + ".txt", "a+") as dlt:
        dlt.seek(0)
        for line in dlt:
            if line == "\n":
                continue
            xline = line.translate(str.maketrans('[,<>:]', '      ')).split()
            point[str(xline[0])] = [int(xline[1]), int(xline[2]), int(xline[3]), int(xline[4])]


def c(name, wt=0.25, times=1, interval=0.2, rgb=False, fc=False, ranpos=True, th=0.7, dura=0.01, cp=False, layer=0):
    global file_path
    os.chdir(file_path)
    t1 = time.time()
    interval += u(0, 0.7 * interval)
    log_out("准备点击 %s" % str(name), layer=layer)
    if isinstance(name, str):
        if "." in name:
            name = name.replace(".", "")
            for i in range(0, times):
                if ranpos:
                    pos_x = u(-0.5 * point[name][2], 0.5 * point[name][2])
                    pos_y = u(-0.5 * point[name][3], 0.5 * point[name][3])
                else:
                    pos_x = pos_y = 0
                ptx = point[name][0] + pos_x
                pty = point[name][1] + pos_y
                if times > 0:
                    time.sleep(interval)
                touch((ptx, pty), duration=dura)
        else:
            dtl = png[name]
            na_plus = "png/" + name + ".png"
            temp = Template(na_plus, rgb=rgb, record_pos=(float(dtl[0]), float(dtl[1])),
                            resolution=(float(dtl[2]), float(dtl[3])), threshold=th)
            pos = touch(temp)
            for _ in range(1, times):
                time.sleep(interval)
                touch(pos, duration=dura)
    elif isinstance(name, tuple):
        touch(name, duration=dura)
    elif isinstance(name, list):
        touch(name, duration=dura)
    else:
        print("输入出错")
        exit(1)
    if cp:
        time.sleep(0.3)
        touch((ptx - 100, pty))
        print("执行换位")
    if fc:
        time.sleep(0.05)
        wait_judge()
    time.sleep(wt)
    log_out("点击 " + str(name) + " 本步用时 = {:.2f}".format(time.time() - t1), layer=layer + 1)


def w(name, timeout=200, interval=0.8, rgb=False, wt=1, ct=1, fc=True, layer=0, th=0.7):
    global file_path
    os.chdir(file_path)
    t2 = time.time()
    flag = 0
    dtl = png[name]
    na_plus = "png/" + name + ".png"
    log_out("正在等待 %s" % name, layer=layer)
    while flag != ct:
        if fc:
            if find_circle():
                flag = 0
        t1 = time.time()
        temp = Template(na_plus, rgb=rgb, record_pos=(float(dtl[0]), float(dtl[1])),
                        resolution=(float(dtl[2]), float(dtl[3])), threshold=th)
        wait(temp, interval=interval, timeout=timeout)
        if time.time() - t1 > 2:
            flag = 0
        flag += 1
    time.sleep(wt)
    log_out("找到 %s 本步用时 = %.2f" % (name, time.time() - t2), layer=layer + 1)


def e(name, th=0.7, layer=0, rgb=False, timeout=0.2, method=None, scale_step=0.01, scale_max=800):  # e1
    global file_path
    os.chdir(file_path)
    if method is None:
        method = ["brisk"]
    method.extend(["mstpl"])
    basic = ST.FIND_TIMEOUT_TMP
    ST.FIND_TIMEOUT_TMP = timeout
    ST.CVSTRATEGY = method
    # print(ST.CVSTRATEGY)
    log_out("检测 %s 是否存在" % name, layer=layer)
    dtl = png[name]
    na_plus = "png/" + name + ".png"
    temp = Template(na_plus, record_pos=(float(dtl[0]), float(dtl[1])),
                    resolution=(float(dtl[2]), float(dtl[3])), scale_step=scale_step, scale_max=scale_max, threshold=th,
                    rgb=rgb)

    flag = exists(temp)
    if isinstance(flag, list):
        flag = (flag[0], flag[1])
    if flag:
        log_out("%s 存在" % name, layer=layer + 1)
    else:
        log_out("%s 不存在" % name, layer=layer + 1)
    ST.CVSTRATEGY = ["surf", "sift", "mstpl", "tpl", "brisk"]
    ST.FIND_TIMEOUT_TMP = basic
    return flag


def fa(name, th=0.7, rgb=False):
    global file_path
    os.chdir(file_path)
    ST.CVSTRATEGY = ["tpl"]
    dtl = png[name]
    na_plus = "png/" + name + ".png"
    temp = Template(na_plus, record_pos=(float(dtl[0]), float(dtl[1])),
                    resolution=(float(dtl[2]), float(dtl[3])), threshold=th, rgb=rgb)
    result = find_all(temp)
    if result is None:
        result_2 = np.array([[0, 0]])
    else:
        result_1 = np.array([x['result'] for x in result])
        result_2 = result_1[np.lexsort((result_1[:, 0], result_1[:, 1]))]
    print(ST.CVSTRATEGY)
    ST.CVSTRATEGY = ["surf", "sift", "mstpl", "tpl", "brisk"]
    return result_2


def find_circle():
    return 0
    # t1 = time.time()
    # dev = device()
    # circle_img = dev.snapshot()
    # circle_img = circle_img[780:912, 1150:1280]
    # gray = cv2.cvtColor(circle_img, cv2.COLOR_BGR2GRAY)
    # result = cv2.medianBlur(gray, 5)
    # circles = cv2.HoughCircles(result, cv2.HOUGH_GRADIENT, 1, 50, param1=90, param2=40, minRadius=10, maxRadius=100)
    # if circles is None or circles[0, 0, 0] == 0:
    #     # delay_collect.append(time.time() - t1)
    #     return False
    # else:
    #     # print("出现延迟")
    #     # delay_collect.append(time.time() - t1)
    #     return True


def p(percent=0.5, duration=0.5, steps=5, in_or_out='in'):
    global dev
    if dev is None:
        dev = Android()
    dev.pinch(percent=percent, duration=duration, steps=steps, in_or_out=in_or_out)
    time.sleep(0.5)


def wait_judge():
    wtc = 0
    while find_circle():
        time.sleep(0.3)
        wtc += 1
        if wtc > 15 / 0.3:
            log_out("出现网络延迟")
        if wtc > 30 / 0.3:
            print("网络延迟超时，自动退出")
            exit(1)


def clink(name1, name2=None, logic=False, wt=1.5, fc=False, th=0.7, repeat=20, least=0, times=1, rgb=False):
    # clinkp
    log_out("准备进行 clink %s ,%s" % (name1, name2))
    t1 = time.time()
    flag = 0
    if least == 1:
        c(name1, layer=1)
    if name2 is None:  # name1 == name2 说明是找自己
        pos = e(name1, th=th, layer=1, rgb=rgb)
        while pos:
            c(pos, wt=wt, fc=fc, layer=2)
            pos = e(name1, th=th, layer=1, rgb=rgb)
            flag += 1
            if flag > repeat:
                print("clink重复次数过多")
                raise TargetNotFoundError('clink异常')
    else:
        if logic:  # False 为找不到 name2 点 name1
            e_flag = e(name2, th=th, layer=1)  # 确认第二目标是否存在
            while e_flag:
                if "." in name1 or isinstance(name1, tuple):
                    c(name1, wt=wt, layer=1, times=times)
                else:
                    pos = e(name1, th=th, layer=1, rgb=rgb)
                    if pos:
                        c(pos, wt=wt, layer=2)
                e_flag = e(name2, th=th, layer=1, rgb=rgb)
                flag += 1
                if flag > repeat:
                    print("clink重复次数过多")
                    raise TargetNotFoundError('clink异常')
        else:
            e_flag = e(name2, th=th, layer=1, rgb=rgb)  # 确认第二目标是否存在
            while not e_flag:
                if "." in name1 or isinstance(name1, tuple):
                    c(name1, wt=wt, times=times, layer=1)
                else:
                    pos = e(name1, th=th, layer=1, rgb=rgb)
                    if pos:
                        c(pos, wt=wt, layer=2)
                e_flag = e(name2, th=th, layer=1, rgb=rgb)
                flag += 1
                if flag > repeat:
                    print("clink重复次数过多")
                    raise TargetNotFoundError('clink异常')
    log_out("clink %s ,%s 本步用时：%.2f" % (name1, name2, time.time() - t1))


def log_out(info, layer=0):
    if layer != 0:
        print("%s|\n" % (" " * 2 * layer), end="")
        print("%s -- %s --" % ((" " * 2 * layer), info))
    else:
        print("\n-- %s --" % info)


def mission_ini(name, cw, auto_supply=0):
    log_out("开始关卡预设")
    f = open(project_pos + "snqx/mission_ini/" + name + ".txt", "a+")
    f.seek(0)
    result = f.readlines()
    if not result:
        result = [0]
    if result[-1] == "1\n":
        f.close()
        log_out("关卡已预设")
        return 1
    if cw is None:
        c(name)
    else:
        clink(name, cw)
        c(cw)
    w("rtm")
    c("bg_detail")
    c("bg_set")
    w("bg_mark")
    if auto_supply == 0:
        clink("as_off.", "auto_supply", logic=True, th=0.8)
    else:
        clink("as_off.", "auto_supply", th=0.8)

    c("white_back", wt=3)
    for i in range(0, 2):
        pinch("in")
        time.sleep(1)
    clink("rtm", least=1)
    f.write("1\n")
    f.close()
    log_out("预设完成")
    return 0


def man_repair(adjust=0, num=5):  # 带确定
    t1 = time.time()
    w("echelon_group", ct=1)
    dev = device()
    repair_img = dev.snapshot()
    for i in range(1, num + 1):
        name = "repair_" + str(i)
        x = point[name][0] + int(adjust * 1.4)
        y = point[name][1]
        (b1, g1, r1) = repair_img[y, x]
        print((b1, g1, r1))
        if r1 <= 50 and g1 <= 50 and b1 <= 50:
            c((x, y), wt=1)
            c("repair_confirm", wt=1)
            print("修复%s个人形" % i)
    while e("echelon_group"):
        c("confirm")
        if time.time() - t1 > 30:
            print("修复超时")
            exit(1)
    print("修复完毕")


def exp_dec(name=False, rtb=0):
    global HOUR_CLOCK
    if time.time() - HOUR_CLOCK <= 3600:
        return 0
    if rtb == 0:
        exit(1)
    elif rtb == 2:
        clink("rtm", "quick_bar", wt=2)
        clink("quick_bar", "quick_exp", wt=2)
        clink("quick_exp", wt=3)
        clink("exp_book", "exp_confirm")
        c("exp_confirm")
        c("exp_confirm_2")
        clink("quick_bar", "rtb")
        swipe((193, 371), (1000, 430))
        clink("quick_battle", wt=2)
        if isinstance(name, str):
            clink(name, "normal_mission", th=0.9)
            c("normal_mission", fc=False)
            equ_dec()
    HOUR_CLOCK = time.time()


def man_dec(name=False, rtb=0, sw=4):
    pos = e("man_full")
    if pos:
        log_out("\n人形已满\n")
        if rtb == 0 or rtb == 4:
            c(pos, wt=0.8)
            send_notice("js_alert", "人形已满！")
            input("程序暂停,输入任意继续")
        else:
            c(pos, wt=0.8)
            clink("retire", "select_doll", th=0.8)
            c("select_doll")
            c("ai_select", times=2, interval=1)
            c("depart", wt=0.5)
            c("select_doll", wt=1)
            if e("filter_by"):
                c("filter_by")
                c("f_4s")
                c("f_3s")
                c("select_confirm", ranpos=False)
                for y in range(0, 1):
                    for x in range(0, 6):  # 181 305
                        point["doll"] = deepcopy(point["equip_start"])
                        point["doll"][0] += x * 181
                        point["doll"][1] += y * 305
                        c("doll.", fc=False, wt=0)
                c("depart_confirm")
                c("depart", times=2)
                c("confirm", wt=0.5)

        clink("quick_bar", "quick_battle", wt=1.5)
        if rtb == 1 or rtb == 0:
            c("quick_battle", times=2, ranpos=False, wt=2)
            if isinstance(name, str):
                clink(name, "normal_mission", th=0.9)
                c("normal_mission", fc=False)
        elif rtb == 2:
            c("jxl", times=2, ranpos=False)
            if isinstance(name, str):
                w("quick_bar")
                """for i in range(0, sw):
                    swipe((1205, 909), (272, 827), duration=0.6)"""
                c(name, fc=False)
                c("battle_confirm", fc=False)
        return True
    else:
        return False


def equ_dec(rtb=1):
    pos = e("equip_full")
    if pos:
        c(pos)
        log_out("\n装备已满\n")
        if rtb == 0:
            input("程序暂停,输入任意继续")
        if rtb == 1:
            try:
                clink("quick_bar", "quick_fac", wt=1.5)
                c("quick_fac", times=2, wt=2)
                c("retire", th=0.8)
                c("select_equip")
                c("ai_select", ranpos=False, times=3)
                c("depart")
                c("select_equip")
                c("filter_by")
                c("f_4s")
                c("f_3s")
                c("select_confirm", ranpos=False)
                for y in range(0, 2):
                    for x in range(0, 6):  # 181 305
                        point["equip"] = deepcopy(point["equip_start"])
                        point["equip"][0] += x * 181
                        point["equip"][1] += y * 305
                        c("equip.", fc=False, wt=0)
                c("depart_confirm")
                c("depart")
                c("confirm", wt=0.5)
            except TargetNotFoundError:
                print("装备拆解出错，跳过")
            clink("quick_bar", "quick_fac", wt=1.5)
            c("quick_battle", times=2, ranpos=False, wt=2)
            c("81n")
            c("normal_mission")
            equ_dec(rtb=1)
        return True
    else:
        return False


fst_gunner = -1


def change(name1, name2, order=[], filter=[], des=False, corr=False):
    global fst_gunner
    w("echelon_group", ct=1)
    dev = device()
    repair_img = dev.snapshot()
    (b1, g1, r1) = repair_img[667, 490]
    if not (r1 <= 50 and g1 <= 50 and b1 <= 50):
        log_out("打手已补给，无需换位")
        return 0
    c("echelon_group", wt=2)
    if fst_gunner == -1:
        w("quick_bar", interval=0.1)
        if e(name1 + "_1", th=0.8):
            fst_gunner += 2
        else:
            fst_gunner += 1
    if fst_gunner % 2 == 1:
        c(name1 + "_1", wt=1)
    else:
        c(name2 + "_1", wt=1)
    if not order and not filter:
        w("order_by")
    if order:
        c("order_by")
        for item in order:
            c("o_" + item)
    if filter:
        c("filter_by", wt=0.5)
        if corr:
            c("f_" + filter[fst_gunner % 2])
            for item in filter[2:]:
                c("f_" + item)
        else:
            for item in filter:
                c("f_" + item)
        c("select_confirm", th=0.8)
    if des:
        c("des_order")
    if fst_gunner % 2 == 1:
        c(name2 + "_2", wt=1, th=0.8)
    else:
        c(name1 + "_2", wt=1, th=0.8)
    fst_gunner += 1
    clink("back")
    w("mission_start")
    return 1


def ranln(t):
    if t == 0:
        return 0
    lamada = 1 / t
    x = u(0.02 * lamada, 0.95 * lamada)
    y = -1 / lamada * logg(x / lamada)
    return y


def progress_bar(name, count, gap=100, bar_length=40, ata=0.8, fc=False):  # gap控制百分比 bar_length控制进度条长度
    global PAUSE_TIME
    global Mission_Name
    t1 = time.time()
    pause_time = np.mean(PAUSE_TIME)
    mean_pause_time = np.mean(PAUSE_TIME)
    h = pause_time / 3600
    m = (h - int(h)) * 60
    s = (m - int(m)) * 60
    time_str = "%dh %dm %ds" % (h, m, s)

    print('本次为第{}次 总计完成次数:{} 睡眠时间:{}'.format(count, fileopr([Mission_Name], opr="r") - 1, time_str))
    for i in range(0, gap):
        print("\r当前进度：[{:.2f}%] {}".format((i * 100 / gap), '>' * int(i / gap * bar_length)), end='', flush=True)
        time.sleep(pause_time / gap)
    print('\r本次睡眠时间{:.1f} 已完成'.format(pause_time) + "   " * 20, end='\n')

    if name:
        w(name, to=300, wt=1, ct=2, interval=2, fc=fc)
    if time.time() - t1 - pause_time > 6:
        pause_time = time.time() - t1 - 8
    else:
        pause_time = ata * pause_time
    PAUSE_TIME.append(pause_time)
    if len(PAUSE_TIME) >= 5:
        out = np.argwhere(abs(np.array(PAUSE_TIME) - mean_pause_time) > 0.4 * mean_pause_time)
        if out:
            PAUSE_TIME.pop(out[0][0])


def progress_bar_mrfz(name, count, pause_time, target_time, gap=100, bar_length=40,
                      fc=False):  # gap控制百分比 bar_length控制进度条长度
    h = pause_time / 3600
    m = (h - int(h)) * 60
    s = (m - int(m)) * 60
    time_str = "%dh %dm %ds" % (h, m, s)
    print('\n-- 预计清体力时间：%s --' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(target_time)))
    print('-- 本次为第{}次 睡眠时间:{} --'.format(count, time_str))
    for i in range(0, gap):
        print("\r-- 当前进度：[{:.2f}%] {} --".format((i * 100 / gap), '>' * int(i / gap * bar_length)), end='', flush=True)
        time.sleep(pause_time / gap)
    print('\r-- 本次睡眠时间{:.1f} 已完成 --'.format(pause_time) + "   " * 20, end='\n')

    if name:
        w(name, to=300, wt=1, ct=2, interval=2, fc=fc)


def fileopr(context, opr="a"):
    dt = datetime.now()
    f = open("log/%s.txt" % context[0], "a+")
    f.seek(0)
    flines = f.readlines()
    if not flines:
        flines.append("第 0 次")
    fsp = eval(flines[-1].split()[1]) + 1
    if opr == "r":
        f.close()
        return fsp
    tb_ratio = (np.mean(PAUSE_TIME) + 5) / context[2] * 100
    f.write("————————分割线——————————\n")
    f.write("日期：{}\n所用时间：{:.2f}\n第 {} 次\n".format(dt.strftime('%Y-%m-%d %H:%M:%S'),
                                                  context[2], fsp))
    os.system("cls")
    print("本次执行第 %s 次 所用时间：%.2f  \n总战比：%.2f%% 总完成次数：%s" % (context[1], context[2], tb_ratio, fsp))
    f.close()


def arg_analysis():
    args = []
    try:
        f = open("arg_save.txt", mode="r")
        for line in f.readlines():
            args.append(line.rstrip())
    except FileNotFoundError:
        a = 1
    finally:
        return args


def support_go():
    if e("back"):
        c("quick_bar")
        c("rtb")
    try:
        while 1:
            w("L_support", to=5, interval=2)
            c("middle.")
            c("confirm")
    except TargetNotFoundError:
        os.system("start cmd /k python support.py")
        os.popen('taskkill.exe /pid:' + str(os.getppid()))  # 真的难


class initial:
    def __init__(self, name="spl", port="7555", chdir=1, add_para=["a"]):
        global Mission_Name
        self.name = name
        self.port = port
        self.chdir = chdir
        self.add_para = add_para
        self.file_path = os.getcwd()
        self.capmethd = ""
        Mission_Name = name

    def start(self, com_add=1):
        global file_path
        if self.chdir == 4:
            print(0)
        else:
            if self.chdir == 1:
                if "snqx" not in self.file_path:  # 应对两种情况，pycharm启动和cmd启动
                    self.file_path = os.getcwd() + "/snqx"
                    # self.capmethd = "MINICAP_STREAM"

            elif self.chdir == 2:
                if "mrfz" not in self.file_path:
                    self.file_path = os.getcwd() + "/mrfz"
                    self.capmethd = "JAVACAP"

            elif self.chdir == 3:
                if "nikke" not in self.file_path:
                    self.file_path = os.getcwd() + "/nikke"
                    self.capmethd = "JAVACAP"

            os.chdir(self.file_path)
            file_path = self.file_path
            if com_add == 1:
                point_detail("common_1")
            png_detail()
            point_detail(self.name)
        # self.para_trans()
        self.connect()

    def connect(self):
        while True:
            try:
                # connect_device("Android://127.0.0.1:5037/127.0.0.1:" + self.port + "?cap_method=JAVACAP")
                if not cli_setup():
                    auto_setup(__file__, logdir=None, devices=[
                        "android://127.0.0.1:5037/127.0.0.1:" + self.port + "?cap_method=" + self.capmethd])
                print("连接中")
                Android().snapshot()
                # e("timer")
                os.system('cls')
                print("初始化完成")
            # except AdbShellError:
            # os.system('''start cmd /k"python %s.py"''' % self.name)
            # os.popen('taskkill.exe /pid:' + str(os.getppid()))  # 真的难
            except OSError as ose:
                print(ose)
                if self.add_para[-1] != "t":
                    print("连接出错，正在重连")
                    os.system('''start cmd /k"python %s.py"''' % self.name)
                    os.popen('taskkill.exe /pid:' + str(os.getppid()))  # 真的难
            else:
                break

    def para_trans(self):
        f = open("arg_save.txt", "w")
        for para in self.add_para:
            if para == "t":
                break
            f.write(str(para) + "\n")
        f.close()

    def snapshot(self, name):
        img = device().snapshot()
        cv2.imwrite(name, img)
        return img

    def daily_write(self, info):
        now = datetime.datetime.today()
        if now.hour < 4:
            date = str(datetime.date(year=now.year, month=now.month, day=now.day-1))
        else:
            date = str(datetime.date(year=now.year, month=now.month, day=now.day))
        full_path = "%s/log/%s.json" % (self.file_path, date)
        if os.path.exists(full_path):
            with open(full_path, "r") as f:
                daily_dic = json.load(f)
        else:
            daily_dic = {}

        daily_dic.update(info)
        with open(full_path, "w") as f:
            json.dump(daily_dic, f, indent=4)

    def daily_read(self, name, zero=False):
        now = datetime.datetime.today()
        if now.hour < 4:
            date = str(datetime.date(year=now.year, month=now.month, day=now.day - 1))
        else:
            date = str(datetime.date(year=now.year, month=now.month, day=now.day))
        full_path = "%s/log/%s.json" % (self.file_path, date)
        if os.path.exists(full_path):
            with open(full_path, "r") as f:
                daily_dic = json.load(f)
        else:
            if not zero:
                return None
            else:
                return 0

        if name in daily_dic:
            return daily_dic[name]

        if not zero:
            return None
        else:
            return 0

    def kill_server(self):
        ADB().kill_server()


# point_detail("common_1")
