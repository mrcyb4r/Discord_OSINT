import requests
import json
import sys
import argparse
from modules import utils, steam, github, youtube, spotify, general, twitter, twitch, playstation

def main(id, file_name='', token="token here", export_json=False, export_txt=True):
    headers = {
        'authorization': token,
        'referer': 'https://discord.com/'
    }
    
    r = requests.get(f"https://discord.com/api/v9/users/{id}/profile", headers=headers)
    
    if r.status_code == 401:
        utils.print_negative("Invalid token")
        sys.exit(1)
    if r.status_code == 404:
        utils.print_negative("Invalid ID")
        sys.exit(1)
    
    data = r.json()
    user = data.get("user", {})
    username = user.get("username", "N/A")
    display_name = user.get("global_name", "N/A")
    bio = user.get("bio", "N/A")
    email = user.get("email", "Not Found")  # Fetch email if available
    phone = user.get("phone", "Not Found")  # Fetch phone if available
    avatar = user.get("avatar", "N/A")
    banner = user.get("banner", "N/A")
    accent_color = user.get("accent_color", "N/A")
    nitro = "✅ Active" if user.get("premium_type", 0) != 0 else "❌ Not Active"
    
    # Account Creation Date
    snowflake = int(id)
    timestamp = (snowflake >> 22) + 1420070400000
    account_created = utils.convert_unix(timestamp)
    
    # Connected Accounts
    connected_accounts = {acc["type"]: acc["name"] for acc in data.get("connected_accounts", [])}
    
    # Badges
    badges = user.get("badges", [])
    
    # Mutual Servers
    mutual_servers = [guild["id"] for guild in data.get("mutual_guilds", [])]
    
    # Output Format
    output_data = f"""
███████████████████████████████████████████████████
█                                                 █
█  🔍 Scanning Discord ID: {id}                  █
█                                                 █
███████████████████████████████████████████████████

💀 **Username:** {username}
💀 **Display Name:** {display_name}
💀 **Bio:** {bio}
💀 **Gmail Found:** ✉️ {email}
💀 **Phone:** 📱 {phone}
💀 **Badges:** {badges}
💀 **Mutual Servers:** {mutual_servers}
💀 **Connected Accounts:** {connected_accounts}
💀 **Profile Picture:** {'[Click Here](https://cdn.discordapp.com/avatars/' + id + '/' + avatar + '.png)' if avatar != 'N/A' else 'N/A'}
💀 **Banner:** {'[Click Here](https://cdn.discordapp.com/banners/' + id + '/' + banner + '.png)' if banner != 'N/A' else 'N/A'}
💀 **Nitro Status:** {nitro}
💀 **Account Created On:** 🗓️ {account_created}

███████████████████████████████████████████████████
█  🛠️  Process Completed! Stay Anonymous! ☠️  █
███████████████████████████████████████████████████
    """
    
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(output_data)
    
    print(output_data)
    print(f"📁 Data exported to {file_name}")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("id", help="The Discord ID to scrape")
    parser.add_argument("-f", "--file", help="The file name to export to", default="output.txt")
    parser.add_argument("-t", "--token", help="The Discord token to use", required=True)
    args = parser.parse_args()
    
    main(args.id, args.file, args.token)
