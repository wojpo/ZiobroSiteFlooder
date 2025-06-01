import requests
import random
import string
import time
from datetime import datetime

characters = string.ascii_letters + string.digits
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
]

headers_base = {
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://testnr.org/numer/",
}

captcha_url = "https://testnr.org/numer/api/generate-captcha"
check_url = "https://testnr.org/numer/api/validate-numer"

success_counter = 0
error_counter = 0

def log_to_file(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")

while True:
    try:
        session = requests.Session()

        numer = ''.join(random.choices(characters, k=32))
        phone = ''.join(random.choices(string.digits, k=9))

        headers = headers_base.copy()
        headers["User-Agent"] = random.choice(user_agents)

        captcha_response = session.post(captcha_url, json={}, headers=headers)
        if captcha_response.status_code == 429:
            msg = "Too many CAPTCHA requests! Waiting 120 seconds..."
            print(msg)
            log_to_file(msg)
            time.sleep(120)
            continue
        elif captcha_response.status_code != 200:
            msg = f"CAPTCHA request failed: HTTP {captcha_response.status_code}"
            print(msg)
            log_to_file(msg)
            error_counter += 1
            continue

        captcha_data = captcha_response.json()
        captcha_token = captcha_data.get("token")
        captcha_code = captcha_data.get("code")
        if not captcha_token or not captcha_code:
            msg = "Missing CAPTCHA token or code"
            print(msg)
            log_to_file(msg)
            error_counter += 1
            continue

        payload = {
            "numer": numer,
            "phone": phone,
            "captchaToken": captcha_token,
            "captchaCode": captcha_code
        }

        check_response = session.post(check_url, json=payload, headers=headers)
        if check_response.status_code != 200:
            msg = f"Validation request failed: HTTP {check_response.status_code}"
            print(msg)
            log_to_file(msg)
            error_counter += 1
            continue

        response_data = check_response.json()
        success_counter += 1

        print(f"[{success_counter}] SUCCESS - {response_data}")

        log_to_file(f"{success_counter} {response_data}")

        time.sleep(random.uniform(8, 30))

    except requests.exceptions.RequestException as e:
        error_counter += 1
        msg = f"[Network error] {e}"
        print(msg)
        log_to_file(msg)

    except Exception as e:
        error_counter += 1
        msg = f"[Unexpected error] {e}"
        print(msg)
        log_to_file(msg)
