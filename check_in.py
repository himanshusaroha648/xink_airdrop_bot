import requests
import json
import time
from datetime import datetime
from web3 import Web3
from eth_account.messages import encode_defunct
from cryptography.fernet import Fernet  # For encryption

# Config
API_URL = "https://api.x.ink/v1/check-in"
WALLETS_FILE = "wallets.json"
PROXIES_FILE = "proxies.txt"
WEB3_RPC = "https://mainnet.infura.io/v3/YOUR_INFURA_KEY"  # Or any RPC

# Load Encryption Key (Generate once using Fernet.generate_key())
KEY = b'YOUR_FERNET_KEY'  
cipher = Fernet(KEY)

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

def decrypt_private_key(encrypted_key):
    return cipher.decrypt(encrypted_key.encode()).decode()

def get_wallet_signature(wallet_address, private_key):
    w3 = Web3(Web3.HTTPProvider(WEB3_RPC))
    message = encode_defunct(text="Login to Xink Airdrop")
    signed = w3.eth.account.sign_message(message, private_key)
    return signed.signature.hex()

def check_in(wallet, proxy, index, total):
    private_key = decrypt_private_key(wallet["encryptedPrivateKey"])
    signature = get_wallet_signature(wallet["walletAddress"], private_key)
    
    headers = {
        "Authorization": f"Wallet {wallet['walletAddress']}:{signature}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."
    }
    proxies = {"http": proxy, "https": proxy} if proxy else None

    try:
        ip = proxy.split('@')[1].split(':')[0] if proxy else "No Proxy"
        print(f"{get_time()} [IP] {ip}")

        print(f"{get_time()} [Wallet] {wallet['walletAddress']}")
        response = requests.post(API_URL, headers=headers, proxies=proxies, timeout=10)

        if response.status_code == 200:
            print(f"{get_time()} [Status] Check-in ✅\n")
        else:
            print(f"{get_time()} [Status] Failed ❌ (Code: {response.status_code})\n")

    except Exception as e:
        print(f"{get_time()} [Error] {str(e)}\n")

def main():
    wallets = load_wallets()
    proxies = load_proxies()

    print(f"\n{get_time()} Bot Started | Wallets: {len(wallets)} | Proxies: {len(proxies) if proxies else 0}")
    print("=" * 50 + "\n")

    for i, wallet in enumerate(wallets, 1):
        proxy = proxies[i % len(proxies)] if proxies else None
        check_in(wallet, proxy, i, len(wallets))
        time.sleep(1)  # Avoid rate limits

    print(f"{get_time()} All tasks completed!")

if __name__ == "__main__":
    main()