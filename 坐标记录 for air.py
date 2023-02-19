import pyautogui
import time
import win32gui
import sys

global locatedx
global locatedy
from pynput import mouse
from backup import point_pos_check


def on_click(x, y, button, pressed):
    # print(x,y)
    return False


def find_window_pos(targetTitle):
    hWndList = []
    posList = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
    for hwnd in hWndList:
        clsname = win32gui.GetClassName(hwnd)
        title = win32gui.GetWindowText(hwnd)
        if (title.find(targetTitle) >= 0):
            posList = win32gui.GetWindowRect(hwnd)
    return posList


def reposition():
    original = [1280, 960]
    posList = find_window_pos("少女前线 - MuMu模拟器")
    locatedx = posList[0]
    locatedy = posList[1]
    size = [1920/(posList[2] - posList[0]), 1080/(posList[3] - posList[1] - 89)]
    print(posList)
    print("横坐标：{:}，纵坐标：{:}".format(locatedx, locatedy))
    return locatedx, locatedy, size


# filename = input("请输入文件名\n")
filename = "common_1"
path = eval(input("1.snqx\n2.mrfz\n"))
if path == 1:
    path = "snqx/file/" + filename + ".txt"
else:
    path = "mrfz/file/" + filename + ".txt"
with open(path, 'a') as f_object:
    i, message = 0, 0
    func = eval(input("1.录入点 2.检查点\n"))
    while True:
        locatedx, locatedy, size = reposition()
        img = pyautogui.screenshot()
        i += 1
        print("请点击第 " + str(i) + " 点")
        with mouse.Listener(on_click=on_click) as listener:
            listener.join()
        currentMouseX, currentMouseY = pyautogui.position()
        (r, g, b) = img.getpixel((currentMouseX, currentMouseY))
        currentMouseX = int((currentMouseX - locatedx)*size[0])
        currentMouseY = int((currentMouseY - locatedy - 37)*size[1])
        print("该点坐标：[{:},{:}]".format(currentMouseX, currentMouseY))
        print("{:}r  {:}g  {:}b".format(r, g, b))
        if func == 2:
            time.sleep(1)
            continue
        try:
            message = eval(input("是否将该点存入文件？\n1.是 2.否 3.退出 4.显示已有点并退出\n"))
        except SyntaxError:
            message = 2
        if message == 1:
            name = input("请输入该点名称:\n")
            random_rangeX = input("请输入X坐标范围:\n")
            random_rangeY = input("请输入Y坐标范围:\n")
            f_object.write(name + " : <{:},{:}> {:},{:}\n".format(currentMouseX, currentMouseY, random_rangeX,
                                                                       random_rangeY))
        elif message == 2:
            i -= 1
        elif message == 3:
            f_object.close()
            break
        elif message == 4:
            f_object.close()
            with open(path, "r+") as dlt:
                for line in dlt:
                    print(line.rstrip())
                i -= 1
            break
        else:
            i -= 1
            print("输入有误请重新输入")
        print("----------分割线----------")
    point_pos_check(filename)
