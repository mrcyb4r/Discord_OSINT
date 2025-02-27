import requests
import json
import sys
import re
import argparse
from colorama import Fore, Style, init

init(autoreset=True)  # Initialize colorama for colored output

def extract_gmails(text):
    """Extract Gmail addresses from text using regex."""
    email_pattern = r"[a-zA-Z0-9._%+-]+@gmail\\.com"
    return re.findall(email_pattern, text)

def print_hacker_style(data):
    """Prints data in a hacker-style format."""
    print(Fore.GREEN + "=" * 50)
    print(Fore.RED + "🔥 Discord Profile Scanner 🔥".center(50))
    print(Fore.GREEN + "=" * 50)
    
    for key, value in data.items():
        if isinstance(value, list):
            value = ", ".join(value) if value else "N/A"
        print(Fore.CYAN + f"[+] {key}: " + Fore.YELLOW + str(value))
    print(Fore.GREEN + "=" * 50 + "\n")

def main(id, token):
    headers = {'authorization': token, 'referer': 'https://discord.com/'}
    print(Fore.YELLOW + f'🔍 Checking ID: {id}')
    
    r = requests.get(f"https://discord.com/api/v9/users/{id}/profile", headers=headers)
    
    if r.status_code == 401:
        print(Fore.RED + "❌ Invalid token!")
        sys.exit(1)
    if r.status_code == 404:
        print(Fore.RED + "❌ Invalid Discord ID!")
        sys.exit(1)
    
    data = r.json()
    user = data.get("user", {})
    
    discord_info = {
        "Discord ID": id,
        "Username": user.get("username", "N/A"),
        "Display Name": user.get("global_name", "N/A"),
        "Bio": user.get("bio", "N/A"),
        "Emails": []
    }
    
    # Extract Gmail addresses from bio
    if user.get("bio"):
        discord_info["Emails"].extend(extract_gmails(user.get("bio")))
    
    # Extract Gmail from connected accounts
    for account in data.get("connected_accounts", []):
        account_name = account.get("name", "")
        if "@gmail.com" in account_name:
            discord_info["Emails"].append(account_name)
    
    print_hacker_style(discord_info)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Discord Gmail Extractor")
    parser.add_argument("id", help="Discord User ID")
    parser.add_argument("token", help="Discord Authorization Token")
    args = parser.parse_args()
    
    main(args.id, args.token)
