import os
from shutil import copyfile


def line_cut(line):
    xline = line.replace("touch", "").replace("Template", "") \
        .replace("(", "").replace(")", "").replace('"', "") \
        .replace("record_pos", "").replace("resolution", "") \
        .replace(",", "").replace("=", "").replace(".png", "")
    xline = xline[1:]
    xline = xline.split()
    return xline


def findq(list_1, target):  # 查询列表里元素是否与target内元素重合
    for name in list_1:
        if 'r"' + name + '.png' in target or "tpl" in target:
            return True


#mode = eval(input("1. snqx \n2. mrfz \n3. snqxt \n4. mrfzt \n"))
mode = 2
print(123)

path = "nikke"

delete = []
s_name = []  # screenshot.py里的名字
p_name = []  # png_detail里的名字
sst = open("screenshot.air/screenshot.py", "r")
sst_c = sst.readlines()  # screen1shot's context
pgd = open("%s/png/png_detail.txt" % path, "r+")
pgd_c = pgd.readlines()

for sline in sst_c:  # 读取
    s_name.append(line_cut(sline)[0])

for pline in pgd_c:
    p_name.append(line_cut(pline)[0])

for name in s_name:  # 找到两个名字列表里相同的加入删除表
    if name in p_name:
        delete.append(name) # 只有名字

new_png = open("%s/png/new_png.txt" % path, "w")

for line in pgd_c:  # 原文件
    
    if findq(delete, line):  # 包含删除表内元素的行均不加入新文件
        continue
    new_png.write(line)

for line in sst_c:
    new_png.write(line)
if "\n" not in line:
    new_png.write("\n")

png_name = os.listdir("screenshot.air")  # 把文件夹下的图片复制过去
for line in png_name:
    print(line)
    
    if "tpl" in line:
        os.remove("screenshot.air/" + line)
        continue
        
    if findq(list_1=s_name, target='r"'+line):
        source = "screenshot.air/" + line
        destin = "%s/png/" % path + line
        copyfile(source, destin)

png_name = os.listdir("%s/png" % path)  # 把文件夹下的图片复制过去
for line in png_name:
    if "tpl" in line:
        os.remove("%s/png/" % path + line)
    
sst.close()
pgd.close()
new_png.close()
os.remove("%s/png/png_detail.txt" % path)
os.rename("%s/png/new_png.txt" % path, "%s/png/png_detail.txt" % path)
new_png = open("%s/png/png_detail.txt" % path, "r")
for line in new_png:
    print(line.rstrip())
