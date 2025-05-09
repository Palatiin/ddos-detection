import random
import string
import time
import threading
import structlog
from dataset.scripts.traffic_generator import TrafficGenerator


BASE_URL = "http://localhost:8080"


if __name__ == "__main__":
    while 1:
        # Create 10-20 threads (users) per minute, each running TrafficGenerator
        threads = []
        for i in range(random.randint(10, 20)):
            # Create a unique logger for each thread with thread ID
            thread_id = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            logger = structlog.get_logger().bind(tid=thread_id)
            traffic_gen = TrafficGenerator(BASE_URL, logger=logger)
            
            # Create a thread that runs the generate method of TrafficGenerator
            thread = threading.Thread(target=traffic_gen.generate, name=thread_id)
            threads.append(thread)
            
        for thread in threads:
            thread.start()
        
        time.sleep(60)
