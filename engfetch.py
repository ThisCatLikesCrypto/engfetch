#Needs psutil, GPUtil, screeninfo, distro (if linux)

import platform
import psutil
import sys
import datetime
import time
import os
import GPUtil
import subprocess
from screeninfo import get_monitors

if platform.system() == "Linux":
    import distro

orange = '\033[38;5;208m'
red = "\033[91m"
white = "\033[97m"
green = '\033[38;5;120m'
blue = '\033[38;5;117m' #dark-aqua sort of colour

def get_os_info():
    un = platform.uname()
    if os.name == "nt":
        buold = sys.getwindowsversion().build
        if buold >= 22000:
            return ["OS: " ,  un.system + " 11 Build " + str(buold)]
        else:
            return ["OS: ",  un.system + " " + un.release + "Build " + str(buold)]
    elif un.system == "Linux":
        return ["OS: ", f"{un.system} {un.release} ({distro.name(pretty=True)})"]
    else:
        return ["OS: ", un.system + " " + un.release + ""]

def get_cpu_win():
    try:
        cpu_info = subprocess.check_output("wmic cpu get name", shell=True).strip().split(b"\n")[1].strip()
        return cpu_info.decode()
    except Exception as e:
        return str(e)


def get_cpu_info():
    if os.name == "nt":
        cpu_info = get_cpu_win()
    else:
        cpu_info = platform.processor()
    cores = psutil.cpu_count(logical=False)
    threads = psutil.cpu_count(logical=True)
    return ["CPU: ", f"{cpu_info}, {cores} cores ({threads} threads)"]

def get_memory_info():
    mem = psutil.virtual_memory()
    total_mem = mem.total >> 20
    used_mem = mem.used >> 20
    return ["Memory: ", f"{used_mem}MB / {total_mem}MB"]

def get_gpu_info():
    try:
        gpu = GPUtil.getGPUs()[0]
        return ["GPU: ", f"{gpu.name} ({int(round(gpu.memoryFree, 5))}MB/{int(round(gpu.memoryTotal, 5))}MB)"]
    except:
        return ["GPU not found", ""]

def get_primary_disk_usage():
    try:
        devi = psutil.disk_partitions()[0].device
        totalusage = psutil.disk_usage(devi).total
        used = psutil.disk_usage(devi).used
        free = psutil.disk_usage(devi).free
        return ["Primary Disk: ", f"{str(used/totalusage*100)[:2]} ({str(totalusage)} total, {str(free)} free)"]
    except:
        return ["Primary Disk: ", "Borked :shrug:"]

def get_uptime():
    timeSinceBoot = time.time() - psutil.boot_time()
    time_delta = datetime.timedelta(seconds=timeSinceBoot)

    hours, remainder = divmod(time_delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return ["Uptime: ", f"{time_delta.days} Days {hours} Hours {minutes} Minutes {seconds} Seconds"]

def get_resolution():
    m = get_monitors()
    for monitor in m:
        if monitor.is_primary:
            return ["Primary Screen Resolution: ", f"{monitor.width}x{monitor.height}"]
    return ["No Screen Detected ", ""]

def linetoprint():
    ltp = [get_os_info(), get_uptime(), get_cpu_info(), get_memory_info(), get_gpu_info(), get_primary_disk_usage(), get_resolution()]
    return ltp

#I swear this is ending up in so many of my python scripts, not just Stronge
def producesyntaxed(text, color):
    try:
        sys.stdout.write(color + text + '\033[0m')
    except:
        print(text)

def printinfoline(ltp):
    producesyntaxed(" "+ltp[0], orange)
    producesyntaxed(ltp[1 ]+"\n", blue)

def printEVERYTHING():
    ltp = linetoprint()

    flag_pattern = [
        [white, white, white, white, white, white, white, white, white, red, red, red, white, white, white, white, white, white, white, white, white],
        [white, white, white, white, white, white, white, white, white, red, red, red, white, white, white, white, white, white, white, white, white],
        [white, white, white, white, white, white, white, white, white, red, red, red, white, white, white, white, white, white, white, white, white],
        [red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red],
        [white, white, white, white, white, white, white, white, white, red, red, red, white, white, white, white, white, white, white, white, white],
        [white, white, white, white, white, white, white, white, white, red, red, red, white, white, white, white, white, white, white, white, white],
        [white, white, white, white, white, white, white, white, white, red, red, red, white, white, white, white, white, white, white, white, white]
    ]

    i = 0
    producesyntaxed("                      " + os.getlogin() + "@" + platform.uname().node + "\n", green)
    for row in flag_pattern:
        for color in row:
            producesyntaxed("■", color)  # Using a square character to represent the flag
        try:
            printinfoline(ltp[i])  # Move to the next line after each row
        except IndexError:
            print()
        i+=1

def main():
    printEVERYTHING()

if __name__ == "__main__":
    main()