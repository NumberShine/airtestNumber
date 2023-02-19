#!venv/Scripts/python.exe
import os
t1 = []
divition = 0

t1 = os.listdir("D:/SynologyDrive/airtest_copy/snqx")
t1 = []
for name in t1:
    if ".py" in name:
        divition += 1
t1.extend(os.listdir("D:/SynologyDrive/airtest_copy/mrfz"))
t2 = []
for name in t1:
    if ".py" in name:
        t2.append(name)
print("请选择执行文件：")
print("0.清零")
for name in t2:
    print("%d.%s" % (t2.index(name)+1, name))

print("————————分割线————————")

while 1:
    try:
        index = eval(input("输入："))
    except NameError:
        continue
    except SyntaxError:
        continue
    if index == 0:
        os.system("cls")
        t1 = []
        divition = 0
        t1 = os.listdir("D:/SynologyDrive/airtest_copy/snqx")
        t1 = []
        for name in t1:
            if ".py" in name:
                divition += 1

        t1 = []

        t1.extend(os.listdir("D:/SynologyDrive/airtest_copy/mrfz"))
        t2 = []
        for name in t1:
            if ".py" in name:
                t2.append(name)
        print("请选择执行文件：")
        print("0.清零")
        for name in t2:
            print("%d.%s" % (t2.index(name) + 1, name))
        os.system("cd /d D:/SynologyDrive/airtest_copy/")
        print("————————分割线————————")
    elif index > len(t2):
        continue
    elif index <= divition:
        os.system('''start cmd /k"python snqx/%s"''' % (t2[index-1]))
    else:
        os.system('''start cmd /k"python mrfz/%s"''' % (t2[index-1]))