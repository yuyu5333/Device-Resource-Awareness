# Device Monitoring Utilities
This repository contains a collection of Python scripts designed to monitor and report various aspects of device hardware, specifically focusing on CPU, GPU, and memory statistics. These tools are particularly useful for understanding the performance and resource utilization of devices, especially in compute-intensive environments.

## Scripts Overview

#### 1. device_aware.py

This script includes functionality to obtain information about CPU, GPU, and DSP (Digital Signal Processor).
Utilizes libraries like jtop, json, and requests.

#### 2. device_aware_copy.py

Appears to be a variant of device_aware.py, with additional emphasis on CPU information retrieval.
Implements a function getCPUinfo() that uses lscpu for obtaining CPU details.

#### 3. device_cpu.py

Focused on gathering CPU statistics.
Provides functions like get_cpu_stats() and compute_cpu_usage() to monitor CPU usage over time.

#### 4. device_gpu.py

Dedicated to GPU information retrieval.
Includes utility functions like has_command() to check for command availability, likely used in the context of GPU monitoring.

#### 5. device_memory.py

Extracts and reports memory-related information.
Function get_memory_info() parses /proc/meminfo to obtain detailed memory stats, converting values to GB for readability.
Usage
To use these scripts, simply clone the repository and run the desired script with Python. Make sure you have the necessary dependencies installed, such as jtop for some scripts.


```JavaScript
git clone [repository-url]
cd [repository-directory]
python [script-name].py
```
## Dependencies

```
Python 3.x
```
Various Python libraries as required by scripts (e.g., jtop, requests).
Contributing
Contributions to this project are welcome. Please adhere to the standard practices for submitting issues and pull requests.

