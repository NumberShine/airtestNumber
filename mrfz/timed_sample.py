
import threading
import time
import schedule

import datetime
import json
import pathlib
import sys
import re

from asst import Asst, Message


def get_now_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def first_job():
    # print("I'm running on thread %s" % threading.current_thread())
    print("现在时间：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # 任务及参数请参考 docs/集成文档.md

    asst.append_task('StartUp')
    asst.append_task('Fight', {
        'report_to_penguin': True,
        'stage': 'LastBattle',
        # 'penguin_id': '1234567'
    })
    asst.append_task('Recruit', {
        'select': [4],
        'confirm': [3, 4],
        'times': 4
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
        'buy_first': ['招聘许可', '龙门币'],
        'blacklist': ['家具', '碳'],
    })
    asst.append_task('Award')

    asst.start()


def second_job():
    # print("I'm running on thread %s" % threading.current_thread())
    print("现在时间：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # 任务及参数请参考 docs/集成文档.md

    asst.append_task('StartUp')
    asst.append_task('Fight', {
        'report_to_penguin': True,
        'stage': 'LastBattle',
        # 'penguin_id': '1234567'
    })
    asst.append_task('Infrast', {
        'facility': [
            "Mfg", "Trade", "Control", "Power", "Reception", "Office", "Dorm"
        ],
        'drones': "Money"
    })
    asst.append_task('Award')
    asst.start()


def recruit(times):

    asst.append_task('Recruit', {
        'select': [4],
        'confirm': [3, 4],
        'times': times,
        "expedite": True,
    })
    asst.start()


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


if __name__ == "__main__":
    global target_time
    global asst

    # asst 的回调
    @Asst.CallBackType
    def my_callback(msg, details, arg):
        m = Message(msg)
        d = json.loads(details.decode('utf-8'))

        print(m, d, arg)

    # 请设置为存放 dll 文件及资源的路径
    # path = str(pathlib.Path.cwd().parent)
    # path += "\mrfz\MeoAssistantArknights"
    path = "D:/SynologyDrive/airtest_copy/mrfz/MeoAssistantArknights"

    print(path)
    Asst.load(path)

    # 若需要获取详细执行信息，请传入 callback 参数
    # 例如 asst = Asst(callback=my_callback)
    asst = Asst()
    port = "62001"
    print('version', asst.get_version())

    # 请自行配置 adb 环境变量，或修改为 adb 可执行程序的路径
    if asst.connect('adb.exe', '127.0.0.1:' + port):
        print('连接成功')
    else:
        print('连接失败')
        exit()
    chose = eval(input("\n选择：？\n 0. 默认开始\n 1. 先执行一次\n 2. 刷招募\n"))
    if chose == 1:
        first_job()
    elif chose == 2:
        chose2 = eval(input("刷招募次数：？\n"))
        recruit(chose2)

    schedule.every().day.at('07:00').do(run_threaded, first_job)
    #schedule.every().day.at('10:43').do(run_threaded, second_job)

    schedule.every().day.at('13:00').do(run_threaded, second_job)
    schedule.every().day.at('19:00').do(run_threaded, second_job)
    schedule.every().day.at('01:00').do(run_threaded, second_job)
    # schedule.every(30).seconds.do(run_threaded, job)
    #print("定时任务已设置，将于每天 " + target_time + " 运行")

    # print('下次定时任务开始于：' + target_time)

    while True:
        schedule.run_pending()
        time.sleep(1)