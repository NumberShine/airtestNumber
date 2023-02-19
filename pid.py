import psutil as pt
from subprocess import check_output
import os


def get_pid(name):
    return map(int, check_output(["pidof", name]).split())


def getport():
    pids = pt.pids()
    for pid in pids:
        p = pt.Process(pid)
        # print("pid-%d,pname-%s" % (pid, p.name()))
        if p.name() == "NoxVMHandle.exe":
            os.system("Netstat -ano | findstr %s > %s/port.txt" % (pid, os.getcwd()))
    f = open("port.txt", "r")
    flines = f.readline().split()[1][10:]
    f.close()
    os.remove("port.txt")
    return flines


def getport2():
    f = open("F:/Program Files (x86)/Nox/bin/BignoxVMS/nox/nox.vbox", "r")
    for line in f.readlines():
        if "5555" in line:
            return line.split()[4][10:].rstrip('"')


getport2()