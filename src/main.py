# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-only
# Copyright (c) 2026 Real World Tester

import sys
import psutil
import requests
from colorama import init, Fore, Style

# 터미널 색상 초기화
init()

def get_system_info():
    print(Fore.CYAN + "=== Fosslight CI/CD Real App Test ===" + Style.RESET_ALL)
    
    # 1. 메모리 정보 (psutil 사용)
    mem = psutil.virtual_memory()
    print(f"Memory Total: {mem.total / (1024**3):.2f} GB")
    print(f"Memory Used:  {mem.percent}%")

    # 2. 외부 IP 정보 (requests 사용)
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        ip = response.json()['ip']
        print(Fore.GREEN + f"Public IP: {ip}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + "IP Check Failed" + Style.RESET_ALL)

if __name__ == "__main__":
    get_system_info()
    print(Fore.YELLOW + "\n[Info] This app is licensed under GPL-3.0" + Style.RESET_ALL)