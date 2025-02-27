import requests
import json
import sys
import re
import argparse
from colorama import Fore, Style

def extract_emails(text):
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}"
    return re.findall(email_pattern, text)

def print_hacker_banner(discord_id):
    banner = f"""
{Fore.RED}███████████████████████████████████████████████████
█                                                 █
█  {Fore.GREEN}🔍 SCANNING DISCORD ID: {discord_id} {Fore.RED}   █
█                                                 █
███████████████████████████████████████████████████
{Style.RESET_ALL}"""
    print(banner)

def print_hacker_footer():
    footer = f"""
{Fore.RED}███████████████████████████████████████████████████
█  🛠️  {Fore.GREEN}Process Completed! Stay Anonymous! ☠️  {Fore.RED} █
███████████████████████████████████████████████████
{Style.RESET_ALL}"""
    print(footer)

def main(discord_id, token):
    headers = {
        'authorization': token,
        'referer': 'https://discord.com/'
    }
    
    print_hacker_banner(discord_id)
    
    response = requests.get(f"https://discord.com/api/v9/users/{discord_id}/profile", headers=headers)
    
    if response.status_code == 401:
        print(Fore.RED + "❌ Invalid token!" + Style.RESET_ALL)
        sys.exit(1)
    if response.status_code == 404:
        print(Fore.RED + "❌ Invalid Discord ID!" + Style.RESET_ALL)
        sys.exit(1)
    
    data = response.json()
    user = data.get("user", {})
    
    username = user.get("username", "N/A")
    display_name = user.get("global_name", "N/A")
    bio = user.get("bio", "N/A")
    emails = extract_emails(bio) if bio else []
    
    print(Fore.GREEN + f"💀 **Username:** {username}#{user.get('discriminator', '0000')}")
    print(f"💀 **Display Name:** {display_name}")
    print(f"💀 **Bio:** \"{bio}\"")
    
    if emails:
        print(Fore.CYAN + f"💀 **Gmail Found:** ✉️ {emails[0]}")
    else:
        print(Fore.CYAN + "💀 **Gmail Found:** ✉️ None")
    
    mutual_guilds = data.get("mutual_guilds", [])
    if mutual_guilds:
        print(Fore.MAGENTA + f"💀 **Mutual Servers:** 🏴‍☠️ " + ", ".join([guild['id'] for guild in mutual_guilds]))
    else:
        print(Fore.MAGENTA + "💀 **Mutual Servers:** 🏴‍☠️ None")
    
    print_hacker_footer()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Discord OSINT Tool")
    parser.add_argument("discord_id", help="Target Discord user ID")
    parser.add_argument("-t", "--token", required=True, help="Discord API token")
    args = parser.parse_args()
    
    main(args.discord_id, args.token)
