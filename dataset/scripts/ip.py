# Project: DDoS Detection in Application Logs
# Author: Matus Remen (xremen01@stud.fit.vutbr.cz)
# Date: 2025-05-08
# Description: IP address generator utility

import random


class IPAddress:
    @staticmethod
    def get_benign_ip_address() -> str:
        # 172.16.0.0/13 - benign subnet
        # Host min: 172.16.0.1, Host max: 172.23.255.254
        while True:
            ip_address = f"172.{random.randint(16, 23)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
            if ip_address != "172.24.0.0" and ip_address != "172.23.255.255":
                break
        return ip_address

    @staticmethod
    def get_malicious_ip_address() -> str:
        # 172.24.0.0/13 - malicious subnet
        # Host min: 172.24.0.1, Host max: 172.31.255.254
        while True:
            ip_address = f"172.{random.randint(24, 31)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
            if ip_address != "172.24.0.0" and ip_address != "172.31.255.255":
                break
        return ip_address
