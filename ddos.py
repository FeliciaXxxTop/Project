from gevent import monkey
monkey.patch_all()

import gevent
from gevent.pool import Pool
import requests
import time
import random

def fetch_proxies():
    # Proxy fetching function (optional)
    urls = [
        "https://api.proxyscrape.com/v2/?request=displayproxies",
        "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
        # More URLs can be added as needed
    ]
    proxies = []
    for url in urls:
        try:
            response = requests.get(url)
            proxies.extend(response.text.split())
        except requests.RequestException as e:
            print(f"Failed to fetch proxies from {url}: {e}")
    print(f"Found {len(proxies)} proxies")
    return proxies

def send_request(url, proxies=None):
    # Send request function with optional proxy
    if proxies:
        proxy = random.choice(proxies)
        proxies_dict = {"http": proxy, "https": proxy}
    else:
        proxies_dict = None
    try:
        response = requests.get(url, proxies=proxies_dict, timeout=10)
        print(f"Request sent, status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")

def start_load_test(url, requests_per_second, concurrent_requests):
    # Load test function
    proxies = fetch_proxies()
    pool = Pool(concurrent_requests)
    start_time = time.time()

    for _ in range(requests_per_second):
        pool.spawn(send_request, url, proxies)
        gevent.sleep(1 / requests_per_second)

    pool.join()
    end_time = time.time()
    print(f"Completed load test in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    target_url = input("Enter the target URL: ")
    requests_per_second = int(input("Enter the number of requests per second: "))
    concurrent_requests = int(input("Enter the number of concurrent requests: "))

    start_load_test(target_url, requests_per_second, concurrent_requests)
