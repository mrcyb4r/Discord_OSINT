import requests
import json
import sys
import re
from modules import utils
from modules import steam, github, youtube, spotify, general, twitter, twitch, playstation
import argparse

def extract_emails(text):
    """Extracts email addresses from text using regex."""
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}"
    return re.findall(email_pattern, text)

def main(id, file_name='', token="token_here", export_json=False, export_txt=True):
    headers = {
        'authorization': token,
        'referer': 'https://discord.com/'
    }
    
    print(f'🔍 Checking ID: {id}')
    r = requests.get(f"https://discord.com/api/v9/users/{id}/profile", headers=headers)
    
    if r.status_code == 401:
        print("❌ Invalid token!")
        sys.exit(1)
    if r.status_code == 404:
        print("❌ Invalid Discord ID!")
        sys.exit(1)
    
    data = r.json()
    user = data.get("user", {})
    
    discord_info = {
        "Discord ID": id,
        "Username": user.get("username", "N/A"),
        "Display Name": user.get("global_name", "N/A"),
        "Discriminator": user.get("discriminator", "N/A"),
        "Bio": user.get("bio", "N/A"),
        "Pronouns": data.get("user_profile", {}).get("pronouns", "N/A"),
        "Avatar": f"https://cdn.discordapp.com/avatars/{id}/{user.get('avatar', '')}.png" if user.get("avatar") else "N/A",
        "Banner": f"https://cdn.discordapp.com/banners/{id}/{user.get('banner', '')}.png" if user.get("banner") else "N/A",
        "Accent Color": user.get("accent_color", "N/A"),
        "Badges": data.get("badges", []),
        "Connected Accounts": {},
        "Mutual Servers": [guild.get("id") for guild in data.get("mutual_guilds", [])],
        "Legacy Username": data.get("legacy_username", "N/A"),
        "Premium Type": data.get("premium_type", "N/A"),
        "Emails": []
    }
    
    # Extract emails from bio
    if user.get("bio"):
        discord_info["Emails"].extend(extract_emails(user.get("bio")))
    
    # Extract connected accounts
    for account in data.get("connected_accounts", []):
        account_type = account.get("type")
        account_name = account.get("name")
        account_id = account.get("id")
        
        if account_type and account_name:
            discord_info["Connected Accounts"][account_type] = {
                "name": account_name,
                "url": f"https://{account_type}.com/{account_id}" if account_type not in ["epicgames", "riotgames"] else "N/A"
            }
            
            # Extract emails from connected accounts
            if "email" in account_name:
                discord_info["Emails"].append(account_name)
    
    print("\n🔹 **Extracted Data:**")
    for key, value in discord_info.items():
        if key == "Connected Accounts":
            print(f"➡️ {key}:")
            for acc_type, details in value.items():
                print(f"    🔗 {acc_type}: {details['name']} ({details['url']})")
        else:
            print(f"➡️ {key}: {value}")
    
    print(f"📁 Data exported to {file_name}")
    
    # Export results to file
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(discord_info, f, indent=4)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("id", help="The Discord ID to scrape")
    parser.add_argument("-f", "--file", help="The file name to export to", default="output.json")
    parser.add_argument("-t", "--token", help="The Discord token to use", required=True)
    args = parser.parse_args()
    
    main(args.id, args.file, args.token, args.file.endswith(".json"), not args.file.endswith(".json"))
