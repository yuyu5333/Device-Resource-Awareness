def get_memory_info():
    mem_info = {}
    with open("/proc/meminfo", "r") as f:
        for line in f.readlines():
            key, value = line.split(":")
            # 获取数值，转为整数，并从kB转换到GB
            mem_info[key.strip()] = int(value.strip().split()[0]) / (1024 * 1024)

    total_memory = mem_info['MemTotal']
    free_memory = mem_info['MemFree']
    used_memory = total_memory - free_memory
    usage_percentage = (used_memory / total_memory) * 100

    return total_memory, used_memory, free_memory, usage_percentage

def MyMemoryUse():
    total, used, free, usage_pct = get_memory_info()
    print(f"Total Memory: {total:.2f} GB")
    print(f"Used Memory: {used:.2f} GB")
    print(f"Free Memory: {free:.2f} GB")
    print(f"Memory Usage: {usage_pct:.2f}%")


if __name__ == "__main__":
    
    MyMemoryUse()
