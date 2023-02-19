import datetime

from airtest.core.api import *
from airtest.core.error import AdbError

from common import c, e, w, clink
import common as cn
import time
import math
import schedule
import psutil as pt
from func_timeout import func_set_timeout
import func_timeout

ini = cn.initial(chdir=3)


def simulator_boot():
    flag = 0
    pids = pt.pids()
    for pid in pids:
        try:
            p = pt.Process(pid)
            print(p.name())
            if p.name() == "NemuPlayer.exe":
                flag = 1
            if "adb" in p.name():
                os.system("taskkill /F /IM %s" % p.name())
        except pt.NoSuchProcess:
            continue

    if flag == 0:
        if ini.daily_read("todaystart") is None:
            ini.daily_write({"todaystart": time.time()})
        print("MuMu模拟器启动")
        os.system('''start cmd /c shutdown -s -t 3600"''')
        os.popen("start E:/Software/MuMu/emulator/nemu9/EmulatorShell/NemuPlayer.exe")
        time.sleep(30)


SPECIAL_EVENT = True


def locate(path, th=0.7):
    route = []
    for i in range(0, len(path)):
        point_name = path[len(path) - i - 1]
        if not e(point_name):
            route.append(point_name)
        else:
            route.append(point_name)
            break

    if len(route) > 1:
        for i in range(0, len(route) - 1):
            clink(route[len(route) - i - 1], route[len(route) - i - 2], th=th)


def login():
    if ini.daily_read("login", zero=True) != 0:
        return 0
    stop_app("com.proximabeta.nikke")
    stop_app("com.github.kr328.clash.foss")

    clink("clash_icon", "vpn_start")
    clink("vpn_start", "vpn_running")

    home()
    clink("nikke_icon", least=1)

    for i in range(60):
        time.sleep(5)
        if not e("login_surface"):
            if e("login_sign"):
                clink("login_account", "login_input")
                text("numberrifu@outlook.com")
                clink("login_sign", "login_input", logic=True)
                clink("login_passcode", "login_input")
                text("Num15316107907")
                clink("login_enter", "login_sign", logic=True)

            if e("login_confirm"):
                clink("login_confirm")
                time.sleep(20)

            if e("login_annoucement"):
                clink("login_annoucement_1", "login_annoucement_2")
                clink("login_annoucement_3", "login_annoucement", logic=True)

            if e("nikke_icon"):
                raise TargetNotFoundError('闪退')
        else:
            break

    clink("space.", "login_surface", logic=True)
    w("login_annoucement")
    clink("window_cancle")
    if SPECIAL_EVENT and ini.daily_read("event_login") is None:
        if e("event_login_cancle", timeout=5):
            clink("event_login_cancle", "main")
            ini.daily_write({"event_login": 1})
    ini.daily_write({"login": 1})


def shop():
    buy_times = ini.daily_read("shop_buy", zero=True)
    if buy_times == 2:
        return 0
    c("shop_entrance")
    if buy_times == 0:
        clink("shop_free", "shop_buy")
        clink("shop_buy", "defense_reward_view", th=0.9)
        clink("shop_space.", "shop_reset")
        buy_times += 1
        ini.daily_write({"shop_buy": buy_times})

    if ini.daily_read("shop_reset") is None:
        c("shop_reset")
        c("window_confirm")
        ini.daily_write({"shop_reset": 1})

    if buy_times == 1:
        clink("shop_free", "shop_buy")
        clink("shop_buy", "defense_reward_view", th=0.9)
        clink("shop_space.", "shop_reset")
        buy_times += 1
        ini.daily_write({"shop_buy": buy_times})
    clink("home")


def defense(force=False):
    flag1, flag2 = False, False
    if ini.daily_read("defense_add") is None:
        flag1 = True
    if time.time() - ini.daily_read("defense_reward", zero=True) > 3600:
        flag2 = True
    if force:
        flag2 = True
    if not flag1 and not flag2:
        return 0
    clink("defense_entrance", "defense_reward")
    if flag1:
        clink("defense_add_1", "defense_add_2")
        clink("defense_add_2")
        clink("shop_space.", "defense_reward_view", logic=True, wt=3)
        ini.daily_write({"defense_add": 1})
    if flag2:
        clink("defense_reward", "defense_reward_view", th=0.8)
        clink("shop_space.", "main")
        ini.daily_write({"defense_reward": time.time()})


def friend():
    friend_num = ini.daily_read("friend", zero=True)
    friend_time = ini.daily_read("friend_time", zero=True)
    if time.time() - friend_time < 7200 or friend_num == 3:
        return 0

    clink("friend_entrance", "friend_view")
    clink("friend_give")
    friend_num += 1
    ini.daily_write({"friend": friend_num})
    ini.daily_write({"friend_time": time.time()})
    clink("window_cancle", "main")


def arena():
    arena_times = ini.daily_read("arena")
    if arena_times == 5:
        return 0
    if arena_times is None:
        arena_times = 0
    clink("ark_entrance", "arena_entrance", wt=2)
    if e("arena_special"):
        clink("arena_special")
        c("defense_reward_view")

    clink("arena_entrance", "arena_rookie")
    clink("arena_rookie", "arena_battle_1")

    while arena_times < 5:
        clink("arena_battle_1", "arena_battle_2")
        clink("arena_battle_2")
        arena_times += 1
        ini.daily_write({"arena": arena_times})
        w("arena_end")
        clink("arena_space.", "arena_battle_1")

    clink("home")


def sim():
    if ini.daily_read("sim_finish") is None:
        if ini.daily_read("sim_start", zero=True) != 0:
            locate(["home", "ark_entrance", "sim_entrance", "sim_mission"])
        else:
            locate(["home", "ark_entrance", "sim_entrance", "sim_choose"])
        sim_ini()
        sim_buff()
        sim_5()
        clink("home")


def sim_ini():
    if ini.daily_read("sim_ini") is not None:
        return 0
    locate(["sim_choose", "sim_start", "sim_mission"])
    c("sim_normal", th=0.8)
    w("sim_quick")
    if e("common_battle_empty"):
        c("common_battle_empty")
        c("common_battle_group")
        c("common_battle_save")
    clink("sim_quit", "sim_select_no_confirm")
    c("sim_select_no_confirm")
    ini.daily_write({"sim_ini": 1})


def sim_buff():
    sim_progress = ini.daily_read("sim_progress", zero=True)
    sim_choose = ini.daily_read("sim_choose", zero=True)
    sim_pattern = ini.daily_read("sim_pattern")
    sim_start = ini.daily_read("sim_start", zero=True)
    target_num = ini.daily_read("sim_num")
    pattern = ["square", "triangle", "circle", "lozenge"]

    if target_num == 8:
        return 0

    if target_num is None:
        target_num = 0

    while target_num < 8:
        if sim_progress == 0 and sim_start == 0:
            locate(["sim_choose", "sim_start", "sim_mission"])
            ini.daily_write({"sim_start": 1})
            if sim_pattern is None:
                for name in pattern:
                    if e("sim_%s" % name):
                        sim_pattern = pattern.index(name)
                        break
                    else:
                        print("未找到图案")
                        sim_pattern = 0
                ini.daily_write({"sim_pattern": sim_pattern})

        target_pattern = "sim_%s" % pattern[sim_pattern]

        break_flag = False
        while sim_progress < 3:
            w("sim_mission", wt=1.5)
            if e(target_pattern):
                c(target_pattern, wt=1)
            elif e("sim_normal", method=["surf", "sift", "mstpl", "tpl", "brisk"]):
                c("sim_normal", wt=1)
            else:
                break_flag = True
                break

            clink("sim_quick", least=1)
            sim_select()
            sim_progress += 1
            ini.daily_write({"sim_progress": sim_progress})

        if ini.daily_read("sim_choose", zero=True) != 1 or break_flag:
            print(sim_choose, break_flag)
            clink("sim_quit", "sim_select_no_confirm")
            c("sim_select_no_confirm")
            sim_progress, sim_choose, sim_start = 0, 0, 0
            ini.daily_write({"sim_progress": sim_progress})
            ini.daily_write({"sim_start": sim_start})
            ini.daily_write({"sim_choose": sim_choose})
            continue

        if sim_progress == 3:
            c("sim_heal", wt=2)
            c("sim_heal_1")
            c("sim_select_no_confirm")
            c("sim_select_no_confirm")
            sim_progress += 1
            ini.daily_write({"sim_progress": sim_progress})

        if sim_progress == 4:
            clink("sim_boss", "sim_battle", wt=2)
            c("sim_battle")
            time.sleep(40)
            w("common_battle_end")
            c("battle_space.")
            sim_progress += 1
            ini.daily_write({"sim_progress": sim_progress})

        c("sim_select_no")
        c("sim_select_no_confirm")
        c("sim_end")
        c("sim_select_no_confirm")
        w("sim_end_effect")
        c("sim_first.")
        c("sim_select_yes")
        if e("sim_select_yes"):
            c("sim_end_empty")
            c("sim_select_yes")
            c("sim_select_no_confirm")
        else:
            target_num += 1

        sim_progress, sim_choose, sim_start = 0, 0, 0
        ini.daily_write({"sim_num": target_num})
        ini.daily_write({"sim_progress": sim_progress})
        ini.daily_write({"sim_start": sim_start})
        ini.daily_write({"sim_choose": sim_choose})


def sim_select():
    w("sim_effect")
    select_pos_array = [0, 1, 2]
    select_pos = -1
    sim_choose = ini.daily_read("sim_choose", zero=True)
    if sim_choose == 0:
        effect_pos = [509, 737, 965]
        target_pos = [x[1] for x in cn.fa("sim_replace", th=0.7)]

        for p in effect_pos:
            for tp in target_pos:
                if abs(p - tp) < 50:
                    select_pos_array.remove(effect_pos.index(p))

        print(select_pos_array)

        if select_pos_array:
            target_pos = [x[1] for x in cn.fa("sim_apply", th=0.9)]
            for p in effect_pos:
                flag = True
                for tp in target_pos:
                    if abs(p - tp) < 50 or effect_pos.index(p) not in select_pos_array:
                        flag = False
                if flag:
                    select_pos = p

        if select_pos_array and select_pos == -1:
            pos = e("sim_fire", th=0.9, method=["surf", "sift", "mstpl", "tpl", "brisk"])
            if pos:
                for p in effect_pos:
                    if abs(pos[1] - p) < 50 and effect_pos.index(p) in select_pos_array:
                        select_pos = pos[1]
                        break

        if select_pos_array and select_pos == -1:
            pos = e("sim_rare", th=0.9, method=["surf", "sift", "mstpl", "tpl", "brisk"])
            if pos:
                for p in effect_pos:
                    if abs(pos[1] - p) < 50 and effect_pos.index(p) in select_pos_array:
                        select_pos = pos[1]
                        break

    if select_pos == -1 or sim_choose == 1:
        c("sim_select_no")
        c("sim_select_no_confirm")
    else:
        c((447, select_pos + 20))
        c("sim_select_yes")
        ini.daily_write({"sim_choose": 1})


def sim_5():
    sim_progress = ini.daily_read("sim_progress", zero=True)
    if sim_progress == 0:
        c("sim_choose")
        c("sim_5")
        c("sim_start")
        ini.daily_write({"sim_start": 1})
    while sim_progress < 5:
        w("sim_mission", wt=2)
        pos = e("sim_normal", method=["surf", "sift", "mstpl", "tpl", "brisk"])
        if pos:
            c(pos, wt=1)
            clink("sim_quick", least=1)
            c("sim_select_no")
            c("sim_select_no_confirm")
            sim_progress += 1
            ini.daily_write({"sim_progress": sim_progress})
            continue

        # pos = e("sim_random")
        # if pos:
        #     c(pos, wt=2)
        #     pos = e("sim_select_no")
        #     if pos:
        #         c(pos, wt=1)
        #         c("sim_select_no_confirm")
        #         c("sim_select_no_confirm")
        #     else:
        #         c("sim_random.", times=2, wt=1)
        #         c("sim_select_yes")
        #     sim_progress += 1
        #     ini.daily_write({"sim_progress": sim_progress})
        #     continue

        pos = e("sim_heal")
        if pos:
            c(pos, wt=2)
            c("sim_heal_1")
            c("sim_select_no_confirm")
            c("sim_select_no_confirm")
            sim_progress += 1
            ini.daily_write({"sim_progress": sim_progress})
            continue

        clink("sim_quit", "sim_select_no_confirm")
        c("sim_select_no_confirm")
        sim_progress = 0
        ini.daily_write({"sim_progress": 0})
        ini.daily_write({"sim_start": 0})

        return sim_5()

    if sim_progress == 5:
        c("sim_heal", wt=2)
        c("sim_heal_1")
        c("sim_select_no_confirm")
        c("sim_select_no_confirm")
        sim_progress += 1
        ini.daily_write({"sim_progress": sim_progress})

    if sim_progress == 6:
        clink("sim_boss", "sim_battle", wt=1)
        clink("sim_battle")
        time.sleep(90)
        w("common_battle_end")
        c("battle_space.")
        sim_progress += 1
        ini.daily_write({"sim_progress": sim_progress})

    c("sim_select_no")
    clink("sim_select_no_confirm", "sim_end")
    clink("sim_end", "sim_select_no_confirm")
    c("sim_select_no_confirm")
    w("sim_end_effect")
    c("sim_end_empty")
    c("sim_select_yes")
    c("sim_select_no_confirm")
    ini.daily_write({"sim_progress": 0})
    ini.daily_write({"sim_start": 0})
    ini.daily_write({"sim_finish": 1})
    w("sim_choose")


def base():
    if ini.daily_read("base") is not None:
        return 0
    if ini.daily_read("base_collect") is None:
        clink("base_entrance", "base_send")
        clink("base_send", "base_send_view")
        clink("base_send_collect", "defense_reward_view")
        clink("shop_space.", "defense_reward_view", logic=True)
        clink("window_white_cancle")
        ini.daily_write({"base_collect": 1})
    if ini.daily_read("base_send") is None:
        clink("base_send", "base_send_view")
        clink("base_send_all", "base_send_2")
        clink("base_send_2")
        ini.daily_write({"base_send": 1})
        clink("window_white_cancle", "home")
    ini.daily_write({"base": 1})
    clink("home")


def interception():
    inter_num = ini.daily_read("inter", zero=True)
    if inter_num == 3:
        return 0
    locate(["ark_entrance", "inter_entrance", "inter_special", "inter_battle_view"])
    if inter_num == 0:
        clink("inter_battle")
        w("inter_end")
        clink("battle_space.", "inter_battle_view")
        inter_num += 1
        ini.daily_write({"inter": inter_num})
    while inter_num < 3:
        clink("inter_quick", "inter_end")
        clink("battle_space.", "inter_battle_view")
        inter_num += 1
        ini.daily_write({"inter": inter_num})
    clink("home")


def consultation():
    consult_num = ini.daily_read("consultation", zero=True)
    if consult_num == 8:
        return 0
    locate(["home", "nikke_entrance", "nikke_consult", "nikke_consult_view"])
    clink("nikke_consult_first.", "nikke_consult_start")
    while consult_num < 8:
        w("nikke_consult_view_3")
        if e("nikke_consult_max"):
            c("nikke_consult_next")
            continue
        c("nikke_consult_start")
        pos = e("window_confirm")
        if pos:
            c(pos, times=3)
        else:
            c("nikke_consult_next")
            continue
        w("nikke_consult_log")
        clink("nikke_consult_choose.", "nikke_consult_log", logic=True, times=2)
        w("nikke_consult_next", wt=1)
        if not e("nikke_consult_view_3"):
            c("nikke_consult_confirm")
        consult_num += 1
        ini.daily_write({"consultation": consult_num})
        c("nikke_consult_next")

    clink("home")


def upgrade():
    upgrade_num = ini.daily_read("upgrade", zero=True)
    if upgrade_num == 1:
        return 0
    locate(["home", "nikke_entrance", "nikke_plwd", "nikke_upgrade_1", "nikke_upgrade_2"])
    c("nikke_upgrade_2")
    locate(["window_cancle", "home", "main"])
    upgrade_num += 1
    ini.daily_write({"upgrade": upgrade_num})


def union():
    union_num = ini.daily_read("union", zero=True)
    if union_num == 3:
        return 0
    while union_num < 3:
        locate(["home", "union_entrance", "union_raid", "union_raid_confirm"])
        clink("union_raid_confirm", wt=2, repeat=100)

        c("union_raid_mid.")
        if union_num == 1:
            c("union_raid_team2")
        if union_num == 2:
            c("union_raid_team3")

        c("union_raid_battle")
        time.sleep(30)
        w("common_battle_end")
        c("battle_space.")
        union_num += 1
        ini.daily_write({"union": union_num})
    clink("home", "main")


def mail():
    mail_num = ini.daily_read("mail", zero=True)
    if mail_num == 1:
        return 0
    locate(["home", "mail_entrance", "mail_collect"])
    c("mail_collect")
    clink("window_cancle")
    mail_num += 1
    ini.daily_write({"mail": mail_num})


def recruit():
    recruit_num = ini.daily_read("recruit", zero=True)
    if recruit_num == 1:
        return 0
    locate(["home", "recruit_entrance", "recruit_next", "recruit_normal_view"])
    c("recruit_normal_one", wt=1.5)
    clink("window_confirm")
    c("recruit_skip")
    c("recruit_skip")
    c("recruit_confirm")
    clink("hall", "main")


def tower():
    tower_num = ini.daily_read("tower", zero=True)
    if tower_num == 1:
        return 0
    locate(["home", "ark_entrance", "tower_entrance", "tower_view"])
    if datetime.datetime.now().isoweekday() in [3, 7]:
        c("tower_pilgrim", wt=3)
    else:
        c("tower_tribe", wt=3)
    c("tower_stage")
    c("tower_battle")
    w("common_battle_end")
    c("battle_space.")
    tower_num += 1
    ini.daily_write({"tower": tower_num})
    clink("home", "main")


def reward():
    reward_daily = ini.daily_read("reward_daily", zero=True)
    reward_week = ini.daily_read("reward_week", zero=True)
    if reward_daily == 1 and datetime.datetime.now().isoweekday() != 7:
        return 0
    locate(["home", "reward_entrance", "reward_daily", "reward_daily_mission"])
    if reward_daily != 1:
        if not e("reward_cleared"):
            clink("reward_collect", "defense_reward_view")
            clink("shop_space.", "reward_cancle")
        if e("reward_cleared"):
            reward_daily += 1
            ini.daily_write({"reward_daily": reward_daily})

    if reward_week != 1 and datetime.datetime.now().isoweekday() == 7:
        c("reward_week")
        if not e("reward_cleared"):
            c("reward_collect")
            if e("defense_reward_view"):
                clink("shop_space.", "reward_cancle")
        reward_week += 1
        ini.daily_write({"reward_week": reward_week})

    clink("reward_cancle")


def mission_pass():
    pass_num = ini.daily_read("pass", zero=True)
    if pass_num == 1:
        return 0
    locate(["home", "pass_entrance", "pass_assign", "pass_assign_view"])
    c("pass_collect")
    clink("pass_cancle")
    pass_num += 1
    ini.daily_write({"pass": pass_num})


def event():
    event_num = ini.daily_read("event", zero=True)
    if event_num == 5:
        return 0
    locate(["home", "event_entrance", "event_enter", "event_mission", "event_battle"])
    c("event_battle")
    w("common_battle_end")
    event_num += 1
    ini.daily_write({"event": event_num})
    while event_num < 5:
        c("event_again", wt=3)
        w("common_battle_end")
        event_num += 1
        ini.daily_write({"event": event_num})
    c("battle_space.")
    clink("home", "main")


def lib():
    lib_num = ini.daily_read("lib", zero=True)
    if lib_num == 1:
        return 0
    locate(["home", "nikke_entrance", "nikke_lib", "nikke_lib_view"], th=0.8)
    clink("nikke_lib_finish")
    lib_num += 1
    ini.daily_write({"lib": lib_num})


def close_all():
    pids = pt.pids()
    for pid in pids:
        try:
            p = pt.Process(pid)
            if "Nemu" in p.name():
                # os.popen('taskkill.exe /pid:%d' % p.pid)
                os.system("taskkill /F /IM NemuPlayer.exe")
            if "adb" in p.name():
                os.system("taskkill /F /IM adb.exe")
        except pt.NoSuchProcess:
            continue
    ini.daily_write({"login": 0})


def shutdown():
    if ini.daily_read("todaystop") is None:
        ini.daily_write({"todaystop": time.time()})
    os.system('''start cmd /c shutdown -a"''')
    os.system('''start cmd /c shutdown -s -t 120"''')
    input("任意输入取消关机")
    os.system('''start cmd /c shutdown -a"''')


def daily():
    global ini
    schedule.clear('one_time')
    simulator_boot()
    ini.start()

    while 1:
        try:
            login()
            defense()
            friend()
            arena()
            shop()
            interception()
            consultation()
            upgrade()
            base()
            mail()
            # union()
            tower()
            sim()
            # defense(True)
            reward()
            # event()
            mission_pass()
            lib()
            ini.kill_server()
            print("Done")

        except TargetNotFoundError or AdbError:
            print("Error")
            ini.daily_write({"login": 0})
        else:
            break
    close_all()
    shutdown()


def timeout(f):
    def inner(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except func_timeout.exceptions.FunctionTimedOut:
            print("超时")

    return inner


@timeout
@func_set_timeout(5)
def timer_set_now():
    input("任意输入值先执行一次，5秒内无输入则跳过\n")
    # now = datetime.datetime.today()
    # after = now + datetime.timedelta(minutes=1)
    # print(after)
    # schedule.every().day.at("{:0>2}:{:0>2}".format(after.hour, after.minute)).do(daily)
    schedule.every(3).seconds.do(daily).tag("one_time")


def timer_setting():
    print("脚本开始")
    timer_set_now()
    schedule.every().day.at("04:30").do(daily)
    schedule.every().day.at("16:20").do(daily)
    schedule.every().day.at("03:30").do(daily)
    flag = 0
    while 1:
        print("\r脚本运行中{: <10}".format('.' * flag), end='', flush=True)
        flag += 1
        if flag > 10:
            flag = 0
        schedule.run_pending()
        time.sleep(5)


if __name__ == "__main__":
    timer_setting()
