import requests
import base64
import cv2
from airtest.core.api import *
import random
from datetime import datetime
from json.decoder import JSONDecodeError
import math


def send_notice(event_name, text):
    for i in range(0, 3):
        try:
            url = "https://maker.ifttt.com/trigger/" + event_name + "/with/key/" + "bJ4jto4PBEfMcMqV70oG8F" + ""
            payload = "{\n    \"value1\": \"" + text + "\"\n}"
            headers = {
                'Content-Type': "application/json",
                'User-Agent': "PostmanRuntime/7.15.0",
                'Accept': "*/*",
                'Cache-Control': "no-cache",
                'Postman-Token': "a9477d0f-08ee-4960-b6f8-9fd85dc0d5cc,d376ec80-54e1-450a-8215-952ea91b01dd",
                'Host': "maker.ifttt.com",
                'accept-encoding': "gzip, deflate",
                'content-length': "63",
                'Connection': "keep-alive",
                'cache-control': "no-cache"
            }
            response = requests.request("POST", url, data=payload.encode('utf-8'), headers=headers)
            print(response.text)
        except ConnectionResetError:
            continue
        else:
            break


def message_group(detail, det2=None, mode=10):
    message = "k"
    if len(detail) == 2:
        detail.append("0")
    if isinstance(mode, str):
        message = "任务名：{} 已执行次数：{} 执行中途出错 错误信息：{}".format(detail[0], detail[1], det2)
    elif isinstance(mode, int):
        if mode == 1:
            message = "任务名：{} 已执行次数：{} 错误次数：{} 执行完成！".format(detail[0], detail[1], detail[2])
        elif detail[1] % mode == 0 and detail[1] != 0:
            message = "任务名：{} 已执行次数：{} 错误次数：{} 执行中".format(detail[0], detail[1], detail[2])
    if message != "k":
        send_notice("js_alert", message)


API_KEY = ['1lPexFKvG4s2FWG1doNo8xmh', 'nuwiDcm8d42PERnE1rs9GgzF']

SECRET_KEY = ['Xl0HGdQOtvHEoWtC0WDiDoKmvg6h7Y1D', 'WneGs4OFdwmD4NCQ3YQMkERNrtzgxsc8']

OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"

TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'

REQUEST_URL = ["accurate_basic", "general_basic", "accurate", "general"]


def fetch_token():
    dt = datetime.now()
    f = open("D:/SynologyDrive/airtest_copy/save_data/access.txt", "a+")
    f.seek(0)
    data = f.readlines()
    at = []
    date_dif = int(dt.strftime('%j')) - int(data[-1])
    if date_dif > 5 or date_dif < 0:
        print("access_token_net")
        for _ in range(0, len(API_KEY)):
            host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client' \
                   '_id=%s&client_secret=%s' % (API_KEY[_], SECRET_KEY[_])
            response = requests.get(host)
            res_list = response.json()
            at.append(res_list['access_token'])
            f.write(res_list['access_token'] + "\n")
        f.write(dt.strftime('%j') + "\n")

    else:
        print("access_token_local")
        at.append(data[-3].rstrip())
        at.append(data[-2].rstrip())
    f.close()
    return at


# access_token = fetch_token()
call_times = random.randint(0, 3)


def img_to_str(file_name):
    global call_times
    while 1:
        try:
            call_times += 1
            text_1 = ""
            request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/%s" % REQUEST_URL[
                math.ceil((call_times + 1) / 2) % 4]
            f = open(file_name, 'rb')
            img = base64.b64encode(f.read())
            params = {"image": img}
            request_url = request_url + "?access_token=" + access_token[call_times % 2]
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            try:
                t1 = time.time()
                response = requests.post(request_url, data=params, headers=headers, timeout=3)
                t = response.json()
                if time.time() - t1 <= 0.25:
                    time.sleep(0.25 - time.time() + t1)
            except requests.exceptions.RequestException as e:
                print(e, "文字识别超时，重传")
                time.sleep(1)
                continue
            except JSONDecodeError as e:
                print("JSONDecodeError，重传")
                continue
            # if response:
            # print(response.json())
            for words_result in response.json()["words_result"]:
                text_1 = text_1 + words_result["words"]
                # print(text_1)
            if time.time() - t1 <= 0.5:
                time.sleep(0.5 - time.time() + t1)
            f.close()
        except KeyError as key:
            print("ocr识别出错, qps过高", key)
            time.sleep(0.8)
        else:
            break

    return text_1


def ocr_str(select, length=0):
    a = device().snapshot()
    arg = []
    if select == "zy":
        a = a[0:100, 500:1200]
    elif select == "hq":
        diff = 140
        for _ in range(0, 4):
            flag = 1
            while flag == 1:
                b = a[124 + _ * diff:160 + _ * diff, 550:687]
                cv2.imwrite("up_ocr.png", b)
                its = img_to_str("up_ocr.png")
                if len(its) == length:
                    flag = 0
                else:
                    raise TargetNotFoundError("错误截图")
            arg.append(its)
        os.remove("up_ocr.png")
    elif select == "zj":
        diff = 206
        for _ in range(0, 3):
            b = a[185 + _ * diff:243 + _ * diff, 1030:1212]
            cv2.imwrite("up_ocr.png", b)
            arg.append(img_to_str("up_ocr.png"))
    elif select == "qtl":
        b = a[21:96, 1692:1900]
        c = a[1015:1054, 1772:1841]
        cv2.imwrite("up_ocr.png", b)
        arg.append(img_to_str("up_ocr.png"))
        cv2.imwrite("up_ocr.png", c)
        arg.append(img_to_str("up_ocr.png"))
    elif select == "tl":
        for i in range(0, 3):
            b = a[216: 311, 1148: 1323]
            GrayImage = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
            GrayImage = cv2.medianBlur(GrayImage, 5)
            ret, th = cv2.threshold(GrayImage, 128, 255, cv2.THRESH_BINARY)
            cv2.imwrite("up_ocr.png", th)
            arg.append(img_to_str("up_ocr.png"))
            # print("\n", arg)
            if arg[0] == '':
                time.sleep(1)
                arg.clear()
                continue
            break
    elif select == "drone":
        for i in range(0,3):
            b = a[37:37+40,1160:1160+66]
            cv2.imwrite("up_ocr.png", b)
            arg.append(img_to_str("up_ocr.png"))
            if arg[0] == '':
                cv2.imwrite("error_img.png", b)
                time.sleep(1)
                arg.clear()
                continue
            break

        if not arg:
            arg=["100"]
    while 1:
        try:
            os.remove("up_ocr.png")
        except PermissionError:
            print("bbbbb")
        else:
            break
    return arg


if __name__ == '__main__':
    send_notice('js_alert', '124567')
