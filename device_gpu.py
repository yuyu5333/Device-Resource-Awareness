import subprocess
import re

def has_command(cmd):
    """检查系统中是否存在给定的命令"""
    try:
        subprocess.check_output(["which", cmd], stderr=subprocess.STDOUT)
        return True
    except:
        return False

def get_nvidia_smi_gpu_usage():
    try:
        result = subprocess.check_output(["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"]).decode()
        gpu_usages = re.findall(r'(\d+)', result)
        return [int(usage) for usage in gpu_usages]
    except:
        return []

def get_tegrastats_gpu_usage():
    try:
        # 启动tegrastats并立即终止，只获取一次输出
        process = subprocess.Popen(["tegrastats"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result, _ = process.communicate(timeout=0.5)  # 1秒的超时应该足够获取输出
        process.terminate()
        print("result: ", result)
        result = result.decode()
        print("result: ", result)
        gpu_usage_match = re.search(r'GR3D_FREQ (\d+)%', result)
        print("gpu_usage_match: ", gpu_usage_match)
        if gpu_usage_match:
            return [int(gpu_usage_match.group(1))]
        else:
            return []
    except:
        print("error at get_tegrastats_gpu_usage")
        return []

def get_tegrastats_gpu_usage_notry():
    try:
        # 使用Popen启动tegrastats
        with subprocess.Popen(["tegrastats"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) as process:
            
            # 仅读取第一行输出
            result = process.stdout.readline()
        
            # 关闭进程
            process.terminate()

        gpu_usage_match = re.search(r'GR3D_FREQ (\d+)%', result)
        if gpu_usage_match:
            return [int(gpu_usage_match.group(1))]
        else:
            return []
    except:
        return []

def MyGpuUse():
    if has_command("nvidia-smi"):
            gpu_usages = get_nvidia_smi_gpu_usage()
    elif has_command("tegrastats"):
        # gpu_usages = get_tegrastats_gpu_usage()
        gpu_usages = get_tegrastats_gpu_usage_notry()
    else:
        gpu_usages = []

    if not gpu_usages:
        print("没有GPU或无法获取GPU")
    else:
        usage_list = {}
        for idx, usage in enumerate(gpu_usages):
            print(f"GPU {idx}: {usage}%")
            usage_list[f"GPU {idx}"] = float(usage)
        return usage_list


if __name__ == "__main__":

    GPU_Use = MyGpuUse()
    print(GPU_Use)