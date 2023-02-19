from common import c, e, p, w
from network import message_group, ocr_str, send_notice
import common as cn
import time
from datetime import datetime
import mrfz_common.mrfz_common as mc
import random as r

import json
from MeoAssistantArknights.asst import Asst
from MeoAssistantArknights.message import Message

TODAY_FLAG = False
ALERT_CLOCK = 0
detect_interval = 23 * 60 + r.randint(-120, 120)


def daytime_fetch():
    global TODAY_FLAG
    dt = datetime.now()
    f = open(cn.project_pos + "save_data/today.txt", "a+")
    f.seek(0)
    data = f.readlines()
    date_dif = int(dt.strftime('%j')) - int(data[-1])
    if date_dif != 0 and int(dt.strftime('%H')) > 4:
        TODAY_FLAG = False
        f.close()
        return False
    else:
        TODAY_FLAG = True
        f.close()
    return True


def job(asst):
    # print("I'm running on thread %s" % threading.current_thread())
    print("现在时间：" + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # asst.set_penguin_id('1234567')
    asst.append_task('StartUp')
    asst.append_task('Fight', {
        'stage': 'LastBattle',
        # 'penguin_id': '1234567'
    })
    asst.append_task('Recruit', {
        'select': [4],
        'confirm': [3, 4],
        'times': 2
    })
    asst.append_task('Infrast', {
        'facility': [
            "Mfg", "Trade", "Control", "Power", "Reception", "Office", "Dorm"
        ],
        'drones': "Money"
    })
    asst.append_task('Visit')
    asst.append_task('Mall', {
        'shopping': True,
        'shopping': ['家具', '碳'],
        'is_black_list': True
    })
    asst.append_task('Award')

    asst.start()

    asst.start()


def jm(asst):
    f = open(cn.project_pos + "save_data/jm.txt", "a+")
    f.seek(0)
    data = f.readlines()
    # print(data[-1].rstrip())
    last = datetime.strptime(data[-1].rstrip(), "%Y-%m-%d %H:%M:%S.%f")
    now = datetime.now()

    if (now - last).days >= 7:
        asst.append_fight("Annihilation", 3, 0, 5)
        asst.start()
        f.write(str(now) + "\n")
    f.close()


if __name__ == "__main__":
    jm(1)