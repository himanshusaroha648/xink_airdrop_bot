Xink Airdrop Bot

A simple and efficient bot to automate daily check-ins for Xink airdrops. This script supports multiple accounts and ensures smooth operation.

Features

✅ Multiple Accounts Support – Use multiple tokens for different accounts.
✅ Automatic Daily Check-in – The bot automatically collects daily points.
✅ Proxy Support (Optional) – Use proxies for enhanced privacy.
✅ Smooth & Fast Execution – Well-optimized script for seamless performance.

Installation

Follow the steps below to install and run the script in Termux:

1. Clone the Repository

git clone https://github.com/himanshusaroha648/xink_airdrop_bot.git
cd xink_airdrop_bot

2. Install Dependencies

pip install requests
node index.js
3. Configure Your Files

accounts.json (Authorization Tokens)

Add your tokens in JSON format:

[
  {"token": "Bearer YOUR_TOKEN_1"},
  {"token": "Bearer YOUR_TOKEN_2"}
]

proxies.txt (Optional)

If you are using proxies, add them in the following format:

ip:port:username:password  
ip2:port2:username2:password2

Usage

Run the script using the following command:

python check_in.py

Notes

Ensure your accounts.json file contains valid authorization tokens.

If you are using proxies, verify that proxies.txt is correctly formatted.

The script runs automatically for all accounts listed in accounts.json.
