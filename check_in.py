import requests
import json
import time
from datetime import datetime
from web3 import Web3
from eth_account.messages import encode_defunct
from eth_account import Account

# Config
API_URL = "https://api.x.ink/v1/check-in"
WALLETS_FILE = "wallets.json"
PROXIES_FILE = "proxies.txt"
RPC_URL = "https://bsc-dataseed.binance.org/"
MAX_RETRIES = 3

def get_time():
    return datetime.now().strftime("[%d/%m/%Y %H:%M:%S]")

def load_wallets():
    try:
        with open(WALLETS_FILE) as f:
            wallets = json.load(f)
            # Validate private keys
            for wallet in wallets:
                Account.from_key(wallet["privateKey"])
            return wallets
    except ValueError as e:
        print(f"{get_time()} ❌ Invalid wallet format: {str(e)}")
        exit()

def load_proxies():
    try:
        with open(PROXIES_FILE) as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def check_proxy(proxy):
    try:
        test_url = "http://httpbin.org/ip"
        proxies = {
            "http": proxy,
            "https": proxy
        }
        response = requests.get(test_url, proxies=proxies, timeout=10)
        return response.status_code == 200
    except:
        return False

def check_in(wallet, proxy):
    for attempt in range(MAX_RETRIES):
        try:
            # Initialize Web3
            w3 = Web3(Web3.HTTPProvider(RPC_URL))
            
            # Sign message
            message = encode_defunct(text="Login to Xink Airdrop")
            signed = w3.eth.account.sign_message(message, wallet["privateKey"])
            
            # Prepare request
            headers = {
                "Authorization": f"Wallet {wallet['walletAddress']}:{signed.signature.hex()}",
                "User-Agent": "Mozilla/5.0"
            }
            
            proxies_config = {
                "http": proxy,
                "https": proxy
            } if proxy else None
            
            # Show info
            ip = proxy.split('@')[1].split(':')[0] if proxy else "No Proxy"
            print(f"{get_time()} [Attempt {attempt+1}] [IP] {ip} | [Wallet] {wallet['walletAddress'][:10]}...")
            
            # API call
            response = requests.post(
                API_URL,
                headers=headers,
                proxies=proxies_config,
                timeout=15
            )
            
            if response.status_code == 200:
                print(f"{get_time()} ✅ Success")
                return True
            else:
                print(f"{get_time()} ⚠️ API Error: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"{get_time()} ⚠️ Attempt {attempt+1} failed: {str(e)}")
            time.sleep(2)
    
    return False

def main():
    wallets = load_wallets()
    raw_proxies = load_proxies()
    
    # Test proxies
    working_proxies = []
    if raw_proxies:
        print(f"\n{get_time()} 🔍 Testing {len(raw_proxies)} proxies...")
        for proxy in raw_proxies:
            if check_proxy(proxy):
                working_proxies.append(proxy)
                print(f"{get_time()} ✔️ Working proxy: {proxy.split('@')[1].split(':')[0]}")
            else:
                print(f"{get_time()} ❌ Bad proxy: {proxy.split('@')[1].split(':')[0]}")
    
    print(f"\n{get_time()} 🚀 Starting {len(wallets)} wallets with {len(working_proxies)} working proxies")
    print("="*60)
    
    success_count = 0
    for i, wallet in enumerate(wallets, 1):
        proxy = working_proxies[i % len(working_proxies)] if working_proxies else None
        if check_in(wallet, proxy):
            success_count += 1
        time.sleep(1)
    
    print(f"\n{get_time()} ✅ Completed: {success_count}/{len(wallets)} successful")

if __name__ == "__main__":
    main()