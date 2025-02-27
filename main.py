import requests
import re
import json
import argparse
import sys

def extract_gmail(bio):
    match = re.search(r'[\w\.-]+@[\w\.-]+', bio)
    return match.group(0) if match else "No Gmail Found"

def main(user_id, token, file_name):
    headers = {'Authorization': token, 'Referer': 'https://discord.com/'}
    response = requests.get(f"https://discord.com/api/v9/users/{user_id}/profile", headers=headers)
    
    if response.status_code == 401:
        print("❌ Invalid token!")
        sys.exit(1)
    elif response.status_code == 404:
        print("❌ Invalid Discord ID!")
        sys.exit(1)
    
    user_data = response.json()
    
    username = user_data['user']['username']
    display_name = user_data['user'].get('global_name', 'None')
    discriminator = user_data['user']['discriminator']
    bio = user_data.get('user_profile', {}).get('bio', 'No Bio')
    gmail = extract_gmail(bio)
    avatar = f"https://cdn.discordapp.com/avatars/{user_id}/{user_data['user']['avatar']}.png" if user_data['user']['avatar'] else "N/A"
    banner = f"https://cdn.discordapp.com/banners/{user_id}/{user_data['user']['banner']}.png" if user_data['user']['banner'] else "N/A"
    badges = [badge['description'] for badge in user_data.get('badges', [])]
    connected_accounts = {acc['type']: acc['name'] for acc in user_data.get('connected_accounts', [])}
    mutual_servers = [server['id'] for server in user_data.get('mutual_guilds', [])]
    nitro_status = "✅ Active" if user_data['premium_type'] > 0 else "❌ No Nitro"
    account_created = user_data['user'].get('created_at', 'Unknown')
    
    output = f"""
███████████████████████████████████████████████████
█                                                 █
█  🔍 Scanning Discord ID: {user_id}           █
█                                                 █
███████████████████████████████████████████████████

💀 **Username:** {username}#{discriminator}
💀 **Display Name:** {display_name}
💀 **Bio:** {bio}
💀 **Gmail Found:** ✉️ {gmail}
💀 **Badges:** {badges}
💀 **Mutual Servers:** {mutual_servers}
💀 **Connected Accounts:** {connected_accounts}
💀 **Profile Picture:** {avatar}
💀 **Banner:** {banner}
💀 **Nitro Status:** {nitro_status}
💀 **Account Created On:** 🗓️ {account_created}

███████████████████████████████████████████████████
█  🛠️  Process Completed! Stay Anonymous! ☠️  █
███████████████████████████████████████████████████
"""
    
    print(output)
    with open(file_name, "w") as f:
        json.dump(user_data, f, indent=2)
    print(f"📁 Data exported to {file_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("id", help="The Discord ID to scrape")
    parser.add_argument("-t", "--token", help="Your Discord API token", required=True)
    parser.add_argument("-f", "--file", help="Output file name", default="output.json")
    args = parser.parse_args()
    
    main(args.id, args.token, args.file)
