import os
import time
import logging
from jtop import jtop
import json
import requests
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

# get the type of GPU
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

# get physical memory
def getMemory():
    info = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = info.readline()
        if i == 2:
            return (line.split()[ 1 : 2 ])

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
#get resourceinfo:
def get_resourceinfo():
    CPU_Use = getCPUuse()
    GPU_Use = getGPUuse()
    MEM_Total = round(int(getMEMuse()[0])/1024,1)
    MEM_Use = round(int(getMEMuse()[1])/1024,1) / MEM_Total * 100
    DISK_Free = getDISKfree()[2].replace('G','')
    return (CPU_Use,GPU_Use,MEM_Use,DISK_Free)

import argparse

# 创建参数解析器
parser = argparse.ArgumentParser(description='Test Script')

# 添加url参数
# parser.add_argument('--ip', type=str, help='ip', required=True)

# 解析命令行参数
args = parser.parse_args()

# 在这里可以使用url变量进行相应的操作
# print("URL:", url)



#get info 
if __name__  == '__main__':
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
    while True:
        CPU_Arch,CPU_Type,GPU_Type,OS_Version,RAM_Total=get_deviceinfo()
        CPU_Use,GPU_Use,MEM_Use,DISK_Free=get_resourceinfo()
        data={
            'DEVICE_NAME':'NVIDIA Jetson',
            'CPU_Arch':CPU_Arch,
            'CPU_Type':CPU_Type,
            'GPU_Type':GPU_Type,
            'OS_Version':OS_Version,
            'RAM_Total':RAM_Total,
            'CPU_Use':CPU_Use,
            'GPU_Use':GPU_Use,
            'MEM_Use':MEM_Use,
            'DISK_Free':DISK_Free
        }
        
        print(data)

        time.sleep(1)
