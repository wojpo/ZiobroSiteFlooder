import requests
import random
import string
import time
import logging

logging.basicConfig(
    filename='log.txt',
    filemode='a',
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

CHARACTERS = string.ascii_letters + string.digits
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
]

HEADERS_BASE = {
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://testnr.org/numer/",
}

CAPTCHA_URL = "https://testnr.org/numer/api/generate-captcha"
CHECK_URL = "https://testnr.org/numer/api/validate-numer"


def generate_number_and_phone():
    number = ''.join(random.choices(CHARACTERS, k=32))
    phone = ''.join(random.choices(string.digits, k=9))
    return number, phone

def build_headers():
    headers = HEADERS_BASE.copy()
    headers["User-Agent"] = random.choice(USER_AGENTS)
    return headers

def get_captcha(session, headers):
    response = session.post(CAPTCHA_URL, json={}, headers=headers)
    if response.status_code == 429:
        logging.warning("Too many CAPTCHA requests! Waiting 120 seconds...")
        time.sleep(120)
        return None, None
    elif response.status_code != 200:
        logging.error(f"CAPTCHA request failed: HTTP {response.status_code}")
        return None, None

    data = response.json()
    return data.get("token"), data.get("code")

def validate_number(session, headers, number, phone, captcha_token, captcha_code):
    payload = {
        "numer": number,
        "phone": phone,
        "captchaToken": captcha_token,
        "captchaCode": captcha_code
    }

    response = session.post(CHECK_URL, json=payload, headers=headers)
    if response.status_code != 200:
        logging.error(f"Validation request failed: HTTP {response.status_code}")
        return None

    return response.json()

def main_loop():
    success_counter = 0
    error_counter = 0

    while True:
        try:
            session = requests.Session()
            number, phone = generate_number_and_phone()
            headers = build_headers()

            captcha_token, captcha_code = get_captcha(session, headers)
            if not captcha_token or not captcha_code:
                error_counter += 1
                continue

            result = validate_number(session, headers, number, phone, captcha_token, captcha_code)
            if not result:
                error_counter += 1
                continue

            success_counter += 1
            msg = f"[{success_counter}] SUCCESS - {result}"
            print(msg)
            logging.info(msg)

            time.sleep(random.uniform(8, 30))

        except requests.exceptions.RequestException as e:
            error_counter += 1
            logging.error(f"[Network error] {e}")

        except Exception as e:
            error_counter += 1
            logging.exception(f"[Unexpected error] {e}")

if __name__ == "__main__":
    main_loop()
