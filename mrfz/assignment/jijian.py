# -*- encoding=utf8 -*-
__author__ = "Number‘s Laptop"

from airtest.core.api import *
from common import c, e, p, w
from network import message_group, ocr_str, send_notice
import common as cn
import time
# from pid import getport2
import numpy as np
from mrfz_common.mrfz_common import search, quickswipe, snapcheck, distance
import mrfz_common.mrfz_common as mc
import random as r
import network

ALERT_CLOCK = 0
MDX_CLOCK = 0
detect_interval = 23 * 60 + r.randint(-120, 120)


def tc_change(tor=1):
    trade_group = [["wulian", "baihui", "longsl", 1],
                   ["lapld", "dekss", "jue", 1],
                   ["nengts", "xuezhi", "kesong", 2],
                   ["kongbao", "gumi", "yuejy", 3]]

    gold_group = [["li", "midx", "huaihu", 1],
                  ["qingliu", "wendi", "senran", 1],
                  ["paopao", "huoshen", "beina", 2],
                  ["bandian", "yeyan", "meier", 3]]

    exp_group = [["xiyin", "keeb", "hongyun", 1],
                 ["shits", "baixue", "hongdou", 1],
                 ["paopao", "huoshen", "beina", 2],
                 ["shuiyue", "tiaoxs", "xiangcao", 3],
                 ["shuangye", "c3", "jiexk", 4]]

    p()
    if tor == 1:
        cn.log_out("开始进行贸易站检查")
        work_group = trade_group
        cn.clink("trade_station", "station_extend", th=0.8)
    else:
        cn.log_out("开始进行制造站检查")
        work_group = gold_group
        cn.clink("craft_station", "station_extend", th=0.8)

    c("station_extend")
    special = 0
    for room_no in range(0, 2 * tor):
        if room_no == 0:
            station_work_group = []
        elif room_no == 2:
            work_group = exp_group
            station_work_group = []
        change_flag = -1
        cn.w("station_rooms")
        c((200, 320 + room_no * 123), wt=1)
        c((483, 966))  # 小人头像
        cn.w("jijian_select")
        # print("station_work" + str(station_work_group))
        for x in range(0, len(work_group)):
            # print("x", x)
            # print(work_group[x])
            if x in station_work_group:
                continue
            pos = e(work_group[x][0], th=0.8)
            # print(pos)
            if pos and mc.distance_in_and_un([(712, 253), (930, 257), (711, 695)], pos, 50):
                # print(distance((712, 253), pos))
                # print(work_group[x][0] + "jiaru")
                station_work_group.append(x)
                if not e("distracted"):
                    change_flag = search(work_group, skip=station_work_group, level=work_group[x][3])
                else:
                    change_flag = search(work_group, skip=station_work_group)
                if change_flag == 1 and tor == 2:
                    special = 1
                if x == 1 and change_flag != 1:
                    special = 2
                station_work_group.append(change_flag)
                break
        print("change_flag==%s" % change_flag)
        if change_flag != -1:
            c("jijian_confirm")
        else:
            cn.clink("back", "jijian_order", logic=True)
    cn.clink("back", "base_overview")

    return special


def dormitory_spare_search(check=0):
    # distracted = cn.fa("distracted")
    on_shift = cn.fa("on_shift", th=0.75)
    in_room = cn.fa("in_room")

    e_yellow = cn.fa("emotion_yellow", th=0.7, rgb=False)

    # print(on_shift)
    # print(e_yellow)
    spare = []
    on_shift_num = 0
    in_room_num = 0
    for eye in e_yellow:
        not_spare_flag = 0
        if on_shift_num < len(on_shift):
            # print("本次对比")
            # print(on_shift[on_shift_num])
            # print(eye)
            # print(distance(eye, on_shift[on_shift_num]))
            if distance(eye, on_shift[on_shift_num]) < 152:
                on_shift_num += 1
                not_spare_flag += 1
        if in_room_num < len(in_room):
            # print("本次对比")
            # print(in_room[in_room_num], eye)
            # print(distance(eye, in_room[in_room_num]))
            if distance(eye, in_room[in_room_num]) < 355 and in_room[in_room_num][1] < eye[1]:
                in_room_num += 1
                not_spare_flag += 1
        if not_spare_flag == 0:
            spare.append(tuple(eye))
    if check == 1:
        print(on_shift_num)
        print(spare)
        print(len(spare))
        snapcheck(on_shift, "on_shift")
        snapcheck(e_yellow, "e_yellow")
        snapcheck(in_room, "in_room")
        snapcheck(spare, "spare")
    return spare


def dormitory_change():
    cn.log_out("开始进行宿舍检查")
    p()
    rooms = cn.fa("dormitory")
    print(len(rooms))

    for room in rooms:
        cn.clink(tuple(room), "room_info")
        if not e("room_clear"):
            cn.clink("inside_info", "room_clear")
        c("room_clear")
        cn.clink("room_place_in", "clear_all")
        full = 0

        while 1:
            spare = dormitory_spare_search()
            for pos in spare:
                c(pos)
                full += 1
                if full == 5:
                    break
            if full == 5:
                break
            quickswipe(d=1950, duration=1)

        c("jijian_confirm")
        cn.clink("back", "base_overview")
        p()
        cn.log_out("结束宿舍检查")


def power_change():
    cn.log_out("开始进行发电站检查")
    work_group = [["gely", 1], ["leishe", 1], ["axiao", 2], ["gelks", 2], ["yiflt", 2], ["huang", 3], ["te", 3]]
    power_pos = [(789, 483), (660, 600), (800, 730)]
    p()

    """
    rooms = rooms[np.lexsort((rooms[:, 0], rooms[:, 1]))]
    rooms = cn.fa("power_station", th=0.8)
    rooms = np.array([x['result'] for x in rooms])
    """

    station_work_group = []

    for room in power_pos:
        change_flag = 0
        cn.clink(tuple(room), "room_info")
        if not e("room_clear"):
            cn.clink("inside_info", "room_clear")
        c((1540, 241))
        w("jijian_select")

        for x in range(0, len(work_group)):
            if x in station_work_group:
                continue
            pos = e(work_group[x][0], th=0.7)
            if pos and (pos[0] < 833 and pos[1] < 534):
                print(work_group[x][0] + " jiaru")
                station_work_group.append(x)
                if not e("distracted"):
                    change_flag = search(work_group, skip=station_work_group, level=work_group[x][-1], max_choose=1)
                else:
                    change_flag = search(work_group, skip=station_work_group, max_choose=1)
                station_work_group.append(change_flag)
                break

        if change_flag != -1:
            print(work_group[change_flag][0] + " jiaru")
            c("jijian_confirm")
        cn.clink("back", "base_overview")
        p()
        cn.log_out("结束发电站检查")


def center_change():
    work_group = [["shihy", "kaiex", "zhanche", "shanji", "huijin", 1],
                  ["amy", "qinliu", "baoyu", "yanwei", "zaolu", 2]]
    p()
    cn.clink("center_room", "room_info")
    change_flag = 0
    w("room_info")
    if not e("room_clear", th=0.8):
        cn.clink("inside_info", "room_clear", th=0.8)
    c((1540, 241))
    w("jijian_select")
    station_work_group = []

    for x in range(0, len(work_group)):
        pos = e(work_group[x][0], th=0.7)
        if pos and distance((712, 253), pos) < 400:
            print(work_group[x][0] + " jiaru")
            station_work_group.append(x)
            if not e("distracted"):
                change_flag = search(work_group, skip=station_work_group, level=work_group[x][-1], max_choose=5)
            else:
                change_flag = search(work_group, skip=station_work_group, max_choose=5)
            station_work_group.append(change_flag)
            break

    if change_flag != -1:
        c("jijian_confirm")
    cn.clink("back", "base_overview")


def reception_change():
    work_group = [["hong", "chen", 1],
                  ["xingji", "yuanshan", 1]]
    p()
    c("reception_room")
    change_flag = 0
    w("room_info")
    if not e("room_clear", th=0.8):
        cn.clink("inside_info", "room_clear", th=0.8)
    c((1540, 241))
    w("jijian_select")
    station_work_group = []

    for x in range(0, len(work_group)):
        pos = e(work_group[x][0], th=0.7)
        if pos and (pos[0] < 833 and pos[1] < 534):
            print(work_group[x][0] + " jiaru")
            station_work_group.append(x)
            if not e("distracted"):
                change_flag = search(work_group, skip=station_work_group, level=work_group[x][-1], max_choose=2)
            else:
                change_flag = search(work_group, skip=station_work_group, max_choose=2)
            station_work_group.append(change_flag)
            break

    if change_flag != -1:
        c("jijian_confirm")

    cn.clink("back", "base_overview")


def office_change(force_change=-1):
    work_group = [["aiyfl", 1],
                  ["xuyu", 2]]
    p()
    c("office")
    change_flag = 0
    w("room_info")
    if not e("room_clear", th=0.8):
        cn.clink("inside_info", "room_clear", th=0.8)
    c((1540, 241))
    w("jijian_select")
    station_work_group = []
    if force_change == -1:
        for x in range(0, len(work_group)):
            pos = e(work_group[x][0], th=0.7)
            if pos and (pos[0] < 833 and pos[1] < 534):
                print(work_group[x][0] + " jiaru")
                station_work_group.append(x)
                if not e("distracted"):
                    change_flag = search(work_group, skip=station_work_group, level=work_group[x][-1], max_choose=1)
                else:
                    change_flag = search(work_group, skip=station_work_group, max_choose=1)
                station_work_group.append(change_flag)
                break
    else:
        search(work_group, skip=work_group.pop(force_change), max_choose=1)

    if change_flag != -1:
        c("jijian_confirm")

    cn.clink("back", "base_overview")


TARGET_CLOCK_2 = 0


def trade_acc():
    global TARGET_CLOCK_2
    if time.time() > TARGET_CLOCK_2:
        drone = int(network.ocr_str(select="drone")[0])
        print(drone)
        TARGET_CLOCK_2 = time.time() + (130 - drone) * 210

    if time.time() >= TARGET_CLOCK_2:
        p()
        c("trade_station")
        c("station_extend")
        for room_no in range(0, 2):
            c((200, 320 + room_no * 123), wt=1.5)
            if e("wl_working", th=0.8):
                for i in range(0, 2):
                    cn.clink("drone_acc", "acc_max")
                    c("acc_max")
                    c("acc_confirm", wt=2)
                break
        cn.clink("back", "base_overview")


def special_change():
    global MDX_CLOCK
    if time.time() - MDX_CLOCK > 21600:
        tc_change(tor=2)
    MDX_CLOCK = time.time() + 999999


def tired_station_arrangement():
    global MDX_CLOCK
    special = 0
    cn.log_out("开始疲劳处理")
    tired_group = mc.average_gray_scale()
    print("tired_group", tired_group)
    if mc.comp_com([0, 3], tired_group):
        tc_change(tor=1)
    if mc.comp_com([1, 4, 6, 7], tired_group):
        special = tc_change(tor=2)
        if special == 1:
            MDX_CLOCK = time.time() + 999999
            office_change(force_change=2)
        elif special == 2:
            MDX_CLOCK = time.time()
    if mc.comp_com([2, 5, 8], tired_group):
        power_change()
    if mc.comp_com([9], tired_group):
        reception_change()
    if mc.comp_com([10], tired_group):
        print("continue")
    if mc.comp_com([11], tired_group):
        office_change()
    if mc.comp_com([12], tired_group):
        center_change()
    dormitory_change()
    cn.log_out("疲劳处理完成")


def colloct_resource():
    global ALERT_CLOCK, detect_interval

    if e("base_alert", th=0.9):
        cn.clink("base_alert", "wait_list", th=0.8, repeat=10)
        cn.clink("base_trust")
        cn.clink("base_trade", th=0.8)
        cn.clink("base_craft")
        if e("base_tired", th=0.8):
            if (time.time() - ALERT_CLOCK) > 3600:
                send_notice("js_alert", "基建存在疲劳，请上线更换")
                ALERT_CLOCK = time.time()
            else:
                ALERT_CLOCK = 0
            c("base_tired", th=0.8)
            tired_station_arrangement()
        detect_interval = 23 * 60 + r.randint(-60, 60)
        cn.clink((544, 870), "base_overview")
    else:
        if detect_interval > 30:
            detect_interval *= 0.8
        else:
            detect_interval = 30
    special_change()
    trade_acc()
    return detect_interval
