import os
import time
import logging
from jtop import jtop
import json
import requests

# CPU GPU DSP

# get the info of cpu
def getCPUinfo():
    info = os.popen('lscpu')
    i = 0
    while 1:
        i = i + 1
        line = info.readline()
        if i == 1:
            CPU_Arch = line.split()[ 1 : 2 ]
        if i == 10:
            CPU_Type = line.split()[ 1 : 7 ]
            return (CPU_Arch[0],CPU_Type)


# Jetson get the type of GPU 
def getGPUinfo():
    #get version of jetson
    with jtop() as jetson:
        jet_v = jetson.board.info['machine'].split('(')[0]
    #version:GPU
    jet_info = {'NVIDIA Jetson Nano ':'128-core Maxwell @ 921 MHz',
    'NVIDIA Jetson TX1 ':'256-core Maxwell @ 998 MHz',
    'NVIDIA Jetson TX2 ':'256-core Pascal @ 1.3 GHz',
    'NVIDIA Jetson TX2i ':'256-core Pascal @ 1.3 GHz',
    'NVIDIA Jetson Xavier ':'512-core Volta @ 1.37 GHz',
    'NVIDIA Jetson Xavier NX ':'384-core NVIDIA Volta TM GPU'}
    try:
        GPU_Type = jet_info[jet_v]
    except Exception:
        GPU_Type = ''
        print('未匹配到jetson版本')
    return GPU_Type


# get the version of OS
def getOSversion():
    info = os.popen('head -n 1 /etc/issue')
    line = info.readline()
    return (line.split()[ 0 : 3 ])


#get deviceinfo:CPU_Arch  CPU_Type  GPU_Type  OS_Version  RAM_Total
def get_deviceinfo():
    CPU_Arch,CPU_Type = getCPUinfo()
    CPU_Type = " ".join(str(i) for i in CPU_Type[1:6])
    
    GPU_Type = getGPUinfo()

    OS_Version = getOSversion()
    OS_Version = " ".join(str(i) for i in OS_Version[0:3])

    RAM_Total = int(getMemory()[0]) / 1024
    #data = {CPU_Arch,CPU_Type,GPU_Type,OS_Version,RAM_Total}
    return (CPU_Arch,CPU_Type,GPU_Type,OS_Version,RAM_Total)


# get physical memory
def getMemory():
    info = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = info.readline()
        if i == 2:
            return (line.split()[ 1 : 2 ])

# def  getCPUuse():
def getCPUuse():
    with open('/proc/stat', 'r') as f:
        line = f.readline()
    fields = line.split()
    total_cpu_time_prev = sum([int(fields[i]) for i in range(1, len(fields))])
    idle_cpu_time_prev = int(fields[4])

    time.sleep(1)

    with open('/proc/stat', 'r') as f:
        line = f.readline()
    fields = line.split()
    total_cpu_time = sum([int(fields[i]) for i in range(1, len(fields))])
    idle_cpu_time = int(fields[4])

    diff_total_cpu_time = total_cpu_time - total_cpu_time_prev
    diff_idle_cpu_time = idle_cpu_time - idle_cpu_time_prev
    cpu_usage = 100.0 * (diff_total_cpu_time - diff_idle_cpu_time) / diff_total_cpu_time
    return cpu_usage

     # return ( str (os.popen( "top -b -n1 | awk '/Cpu\(s\):/ {print $2}'" ).readline().strip()))

#get GPU_Use
def getGPUuse():
    info = os.popen('cat /sys/devices/gpu.0/load')
    line = info.readline()
    return line.strip()

#get Mem_Use
def getMEMuse():
    info = os.popen('free')
    i  = 0
    while  1 :
        i  = i  + 1
        line  = info.readline()
        if  i == 2 :
            return (line.split()[ 1 : 4 ])

#get DISK_free
def getDISKfree():
    info = os.popen( "df -h /" )
    i = 0
    while 1 :
        i  = i  + 1
        line  = info.readline()
        if i == 2 :
            return (line.split()[ 1 : 5 ])

def get_CpuNumber():
    info = os.cpu_count()
    return int(info)


#get resourceinfo:
def get_Resourceinfo():

    CPU_Number = get_CpuNumber()

    CPU_Use = round(float(getCPUuse()), 4)
    GPU_Use = round(float(getGPUuse()), 4)
    MEM_Total = float(getMEMuse()[0])/1024
    MEM_Use = round(float(getMEMuse()[1])/1024 / MEM_Total * 100, 4)
    return (CPU_Use, GPU_Use, MEM_Use)


#get info 
if __name__  == '__main__':

    while False:
        CPU_Use, GPU_Use, MEM_Use = get_resourceinfo()
        data={
            'CPU_Use':CPU_Use,
            'GPU_Use':GPU_Use,
            'MEM_Use':MEM_Use,
        }
        print(data)
    
    CPU_Number = get_CpuNumber()

    print("CPU_Number: ", CPU_Number)

        # time.sleep(1)

def uselessnesscode():
    pass
    # get info
    # logger_file = os.path.join('log_jetson_info.txt')
    # handlers = [logging.FileHandler(logger_file, mode='w'),
    #             logging.StreamHandler()]
    # logging.basicConfig(format='%(message)s',
    # level=logging.INFO,
    # handlers=handlers)
    # CPU_Arch,CPU_Type,GPU_Type,OS_Version,RAM_Total = get_deviceinfo()
    # logging.info(
    #     "CPU_Arch: {CPU_Arch}\n"
    #     "CPU_Type: {CPU_Type}\n"
    #     "GPU_Type: {GPU_Type}\n"
    #     "OS_Version: {OS_Version}\n"
    #     "RAM_Total: {RAM_Total}".format(
    #         CPU_Arch = CPU_Arch,
    #         CPU_Type = CPU_Type,
    #         GPU_Type = GPU_Type,
    #         OS_Version = OS_Version,
    #         RAM_Total = str(RAM_Total)
    #     )
    # )
