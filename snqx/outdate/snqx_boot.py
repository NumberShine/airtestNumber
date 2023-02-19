from common import *
from airtest.core.error import AdbError, DeviceConnectionError, AirtestError
import psutil as pt
from random import randint
from control import control


ST.FIND_TIMEOUT = 100


def login_today():
    dt = datetime.now()
    f = open("/save_data/login.txt", "a+")
    f.seek(0)
    data = f.readlines()
    if (int(dt.strftime('%j')) - int(data[-1])) != 0:
        f.write(dt.strftime('%j') + "\n")
        try:
            clink("detail_back", "main_battle", repeat=10)
        except TargetNotFoundError:
            f.close()
        else:
            f.close()


def simulator_boot():
    flag = 0
    pids = pt.pids()
    con = control(0)
    for pid in pids:
        try:
            p = pt.Process(pid)
            if p.name() == "NemuHeadless.exe":
                flag = 1
                break
        except pt.NoSuchProcess:
            continue

    if flag == 0:
        print("MuMu模拟器启动")
        os.popen("start F:/ksdler/emulator/nemu/EmulatorShell/NemuPlayer.exe")
        time.sleep(35)

    while 1:
        try:
            pause = randint(1, 7)
            ini = initial(name="snqx_boot")
            ini.start()
            t1 = time.time()
            stop_app("com.sunborn.girlsfrontline.cn")
            start_app("com.sunborn.girlsfrontline.cn")
            time.sleep(15)
            c("boot_start", wt=8)
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
            os.system('''start cmd /k"python snqx_boot.py"''')
            os.popen('taskkill.exe /pid:' + str(os.getppid()))
            exit(1)
        except RuntimeError:
            print("RuntimeError，%d秒后重试" % pause)
            time.sleep(pause)
        else:
            break

    w("boot_eye")
    c("middle.", wt=12, fc=False)
    pos = e("boot_confirm")
    if pos:
        c("boot_square", fc=False)
        c(pos, fc=False, wt=2)

    pos = e("mima")
    if pos:
        c(pos, fc=False)
        text("Num15316107907")
        c("login", fc=False)

    time.sleep(10)
    login_today()
    con.refresh()
    support_go()


if __name__ == '__main__':
    main()