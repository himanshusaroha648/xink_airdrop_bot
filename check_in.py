import requests
import json
import time
from datetime import datetime

# Configuration
API_URL = "https://api.x.ink/v1/check-in"
ACCOUNTS_FILE = "accounts.json"
PROXIES_FILE = "proxies.txt"

def get_time():
    return datetime.now().strftime("[%d/%m/%Y %H:%M:%S]")

def load_accounts():
    with open(ACCOUNTS_FILE) as f:
        return json.load(f)

def load_proxies():
    try:
        with open(PROXIES_FILE) as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return None

def check_in(account, proxy, index, total):
    headers = {
        "authorization": account["token"],
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None

    try:
        # Show proxy IP
        ip = proxy.split(':')[0] if proxy else "No Proxy"
        print(f"{get_time()} [IP Using] {ip}")

        # Check-in request
        print(f"{get_time()} [Processing] Daily checkin...")
        response = requests.post(API_URL, headers=headers, proxies=proxies, timeout=10)
        
        if response.status_code == 200:
            print(f"{get_time()} [Status] Checkin successful\n")
        else:
            print(f"{get_time()} [Status] Failed (Code: {response.status_code})\n")

    except Exception as e:
        print(f"{get_time()} [Error] {str(e)}\n")

def main():
    accounts = load_accounts()
    proxies = load_proxies()
    
    print(f"\n{get_time()} Bot Started | Accounts: {len(accounts)} | Proxies: {len(proxies) if proxies else 0}")
    print("=" * 50 + "\n")

    for i, account in enumerate(accounts, 1):
        proxy = proxies[i % len(proxies)] if proxies else None
        check_in(account, proxy, i, len(accounts))
        time.sleep(1)  # Avoid rate limits

    print(f"{get_time()} All tasks completed!")

if __name__ == "__main__":
    main()
