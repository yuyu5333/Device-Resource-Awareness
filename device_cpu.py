import time

def get_cpu_stats():
    with open("/proc/stat", "r") as f:
        lines = f.readlines()
    return [line.split() for line in lines if line.startswith("cpu")]

def compute_cpu_usage(prev, current):
    prev_total = sum(map(int, prev[1:]))
    current_total = sum(map(int, current[1:]))

    prev_non_idle = int(prev[1]) + int(prev[2]) + int(prev[3])
    current_non_idle = int(current[1]) + int(current[2]) + int(current[3])

    total_delta = current_total - prev_total
    non_idle_delta = current_non_idle - prev_non_idle

    if total_delta == 0:
        return 0
    return 100 * (non_idle_delta / total_delta)

def MyCpuUse():
    sampletimes = 1
    cpu_usages = {cpu_stat[0]: [] for cpu_stat in get_cpu_stats()}

    print(f"sample times: {sampletimes}")

    while sampletimes <= 1:
        prev_stats = get_cpu_stats()
        time.sleep(0.5)
        current_stats = get_cpu_stats()

        # print(f"sample times: {sampletimes}")
        for prev, current in zip(prev_stats, current_stats):
            cpu_usage = compute_cpu_usage(prev, current)
            cpu_usages[prev[0]].append(cpu_usage)
            # print(f"{prev[0]}: {cpu_usage:.2f}%")

        sampletimes += 1

    print("cpu avg usage: ")
    for cpu, usages in cpu_usages.items():
        avg_usage = sum(usages) / len(usages)
        print(f"{cpu}: {avg_usage:.2f}%")

if __name__ == "__main__":

    # 获取每个cpu的使用情况，并且获得总的cpu使用情况
    MyCpuUse()