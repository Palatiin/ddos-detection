# Project: DDoS Detection in Application Logs
# Author: Matus Remen (xremen01@stud.fit.vutbr.cz)
# Date: 2025-05-08
# Description: Benign traffic generator

import random
from typing import Any, Optional

import requests
import structlog

from dataset.scripts.profiles import HEADERS_PROFILE
from dataset.scripts.ip import IPAddress


class TrafficGenerator:
    def __init__(self, logger: Optional[Any] = structlog.get_logger(__name__)):
        self.log = logger

    def get_headers_profile(self) -> tuple[str, dict]:
        return random.choice(list(HEADERS_PROFILE.items()))

    def generate(self) -> None:
        # Setup headers and IP address from the benign IP subnet
        profile_name, headers = self.get_headers_profile()
        ip_address = IPAddress.get_benign_ip_address()
        self.log.info(f"Selected IP address and profile: {ip_address}, {profile_name}")
        headers["X-Forwarded-For"] = ip_address
        headers["X-Label"] = 0  # 0 == benign, 1 == malicious

        # session = requests.Session()


if __name__ == "__main__":
    TrafficGenerator().generate()
