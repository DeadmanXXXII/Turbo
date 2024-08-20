import requests
import random
import threading

# Define a list of random User-Agent strings
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1"
]

def generate_random_url(base_url):
    # Generate a random 8-digit number
    random_digits = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    # Replace the last 8 characters of the base URL
    return base_url[:-8] + random_digits

def send_request(url):
    random_url = generate_random_url(url)
    headers = {
        "User-Agent": random.choice(user_agents)
    }
    try:
        response = requests.get(random_url, headers=headers)
        print(f"Request: {random_url} - Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def thread_function(base_url, num_requests):
    for _ in range(num_requests):
        send_request(base_url)

if __name__ == "__main__":
    base_urls = [
        "https://turo.com/gb/en/drivers/15418658",
        "https://turo.com/gb/en/drivers/11023149",
        "https://turo.com/gb/en/drivers/7828042",
        "https://turo.com/gb/en/drivers/3474096"
    ]

    num_threads = 10  # Number of concurrent threads
    requests_per_thread = 100  # Number of requests per thread

    threads = []
    for base_url in base_urls:
        for _ in range(num_threads):
            thread = threading.Thread(target=thread_function, args=(base_url, requests_per_thread))
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()
