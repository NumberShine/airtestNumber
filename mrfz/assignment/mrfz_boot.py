from common import *
from random import randint
from airtest.core.error import AdbError,AirtestError,DeviceConnectionError

import psutil as pt


def mrfz_boot(connect=1):
    ST.FIND_TIMEOUT = 60
    flag = 0
    pids = pt.pids()
    for pid in pids:
        try:
            p = pt.Process(pid)
            # print(p.name())
            if p.name() == "NemuHeadless.exe":
                flag = 1
                break
        except pt.NoSuchProcess:
            continue

    if flag == 0:
        print("MuMu模拟器启动")
        os.popen("start F:/Netease/emulator/nemu/EmulatorShell/NemuPlayer.exe")
        time.sleep(35)

    while 1:
        try:
            pause = randint(1, 13)
            if connect:
                mission_name = "jijian"
                ini = initial(name=mission_name, chdir=2)
                ini.start()
            if not e("mrfz_app") and (e("back") or e("terminal")):
                break
            t1 = time.time()
            stop_app("com.hypergryph.arknights")
            start_app("com.hypergryph.arknights")
            time.sleep(10)
            c("start_signal", wt=12)
            w("login_surface")
            pos = e("account_login", th=0.9)
            if pos:
                c("account_login", times=2)
                c("mima")
                text("Num15316107907")
                c((640, 30))
                clink("login")
            else:
                c("start_call", wt=2)
                pos = e("re_enter")
                if pos:
                    c(pos, wt=1)
                    clink("account_login")
                    c("mima")
                    text("Num15316107907")
                    c((640, 100), times=3)
                    clink("login")
            w("base_entrance")
        except AdbError:
            print("AdbError，%d秒后重试" % pause)
            time.sleep(pause)
        except AirtestError:
            print("AirtestError，%d秒后重试" % pause)
            time.sleep(pause)
        except DeviceConnectionError:
            print("DeviceConnectionError，%d秒后重试" % pause)
            time.sleep(pause)
        except ConnectionResetError:
            print("ConnectionResetError，%d秒后重试" % pause)
            time.sleep(pause)
        except StopIteration:
            print("StopIteration，重启")
            os.system('''start cmd /k"python mrfz_boot.py"''')
            os.popen('taskkill.exe /pid:' + str(os.getppid()))
            exit(1)
        except RuntimeError:
            print("RuntimeError，%d秒后重试" % pause)
            time.sleep(pause)
        except IndexError:
            print("IndexError，%d秒后重试" % pause)
            time.sleep(pause)
        except TargetNotFoundError:
            print("TargetNotFoundError，%d秒后重试" % 1)
            time.sleep(1)
        else:
            break


if __name__ == '__main__':
    mrfz_boot()














