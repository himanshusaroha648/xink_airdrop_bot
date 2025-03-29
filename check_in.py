import requests
import json
import time
from datetime import datetime
from web3 import Web3
from eth_account.messages import encode_defunct

# Config
API_URL = "https://api.x.ink/v1/check-in"  # Replace with your API
WALLETS_FILE = "wallets.json"
PROXIES_FILE = "proxies.txt"
RPC_URL = "https://bsc-dataseed.binance.org/"  # Use any RPC

# Helper Functions
def get_time():
    return datetime.now().strftime("[%d/%m/%Y %H:%M:%S]")

def load_wallets():
    with open(WALLETS_FILE) as f:
        return json.load(f)

def load_proxies():
    try:
        with open(PROXIES_FILE) as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return None

def sign_message(private_key, message):
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    message = encode_defunct(text=message)
    signed = w3.eth.account.sign_message(message, private_key)
    return signed.signature.hex()

def check_in(wallet, proxy):
    try:
        # Prepare headers
        signature = sign_message(wallet["privateKey"], "Login to Xink Airdrop")
        headers = {
            "Authorization": f"Wallet {wallet['walletAddress']}:{signature}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        
        # Set proxy
        proxies = {"http": proxy, "https": proxy} if proxy else None
        
        # Show IP
        ip = proxy.split('@')[1].split(':')[0] if proxy else "No Proxy"
        print(f"{get_time()} [IP] {ip} | [Wallet] {wallet['walletAddress']}")

        # API call
        response = requests.post(API_URL, headers=headers, proxies=proxies, timeout=10)
        
        if response.status_code == 200:
            print(f"{get_time()} ✅ Success\n")
        else:
            print(f"{get_time()} ❌ Failed (Code: {response.status_code})\n")

    except Exception as e:
        print(f"{get_time()} ⚠️ Error: {str(e)}\n")

def main():
    wallets = load_wallets()
    proxies = load_proxies()
    
    print(f"\n{get_time()} 🚀 Bot Started | Wallets: {len(wallets)} | Proxies: {len(proxies) if proxies else 0}")
    print("=" * 60)
    
    for i, wallet in enumerate(wallets, 1):
        proxy = proxies[i % len(proxies)] if proxies else None
        check_in(wallet, proxy)
        time.sleep(1)  # Avoid API rate limits
    
    print(f"{get_time()} ✅ All tasks completed!")

if __name__ == "__main__":
    main()
