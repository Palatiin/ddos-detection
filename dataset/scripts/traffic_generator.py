# Project: DDoS Detection in Application Logs
# Author: Matus Remen (xremen01@stud.fit.vutbr.cz)
# Date: 2025-05-08
# Description: Benign traffic generator

import random
import time
from typing import Any, Optional

import requests
import structlog

from dataset.scripts.profiles import HEADERS_PROFILE
from dataset.scripts.ip import IPAddress


class TrafficGenerator:
    """
    Simulate user browsing an e-shop products, generating benign traffic.
    """

    def __init__(self, base_url: str, logger: Optional[Any] = structlog.get_logger(__name__)):
        self.log = logger
        self.base_url = base_url

    def get_headers_profile(self) -> tuple[str, dict]:
        return random.choice(list(HEADERS_PROFILE.items()))

    def view_product_list_page_action(self, offer_page_no: int) -> None:
        """Simulate user viewing product list."""
        viewing_time = max(1, random.normalvariate(10, 5))
        self.log.info(f"Viewing product list page no. {offer_page_no} for {viewing_time:.2f} seconds")
        time.sleep(viewing_time)

    def view_item_page_action(self, item_no: int) -> None:
        """Simulate user viewing product details."""
        viewing_time = max(3, random.normalvariate(12, 8))
        self.log.info(f"Viewing item no. {item_no} for {viewing_time:.2f} seconds")
        time.sleep(viewing_time)

    def generate(self) -> None:
        # Setup headers and IP address from the benign IP subnet
        profile_name, headers = self.get_headers_profile()
        ip_address = IPAddress.get_benign_ip_address()
        self.log.info(f"Selected IP address and profile: {ip_address}, {profile_name}")
        headers["X-Forwarded-For"] = ip_address
        headers["X-Label"] = 0  # 0 == benign, 1 == malicious

        # Simulate user browsing an e-shop products
        session = requests.Session()
        session.headers = headers

        for i in range(random.randint(1, 4)):
            # Load product list
            session.get(f"{self.base_url}/index.html?page={random.randint(1, 50)}")
            self.view_product_list_page_action(i)

            # View X items from the current product list
            for j in range(random.randint(0, 6)):
                session.get(f"{self.base_url}/item.html?itemId={random.randint(1, 1_000_000)}")
                self.view_item_page_action(j)
        
        session.close()

if __name__ == "__main__":
    TrafficGenerator("http://localhost:8080").generate()
