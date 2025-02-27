import requests
import json
import sys
import time
import argparse
from modules import utils

def get_token():
    """Load token from token.txt if not provided in CLI"""
    try:
        with open("token.txt", "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        print("❌ Error: token.txt file not found! Please create one with your Discord token.")
        sys.exit(1)

def get_user_info(user_id, token):
    """Fetch user profile data"""
    headers = {'Authorization': token}
    url = f"https://discord.com/api/v9/users/{user_id}/profile"

    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        return r.json()
    elif r.status_code == 404:
        print("❌ Invalid User ID! User not found.")
    elif r.status_code == 429:
        retry_time = int(r.headers.get("Retry-After", 5))
        print(f"⚠️ Rate limited! Waiting {retry_time} seconds before retrying...")
        time.sleep(retry_time)
        return get_user_info(user_id, token)
    else:
        print(f"⚠️ Error fetching user data: {r.status_code}")
    return None

def save_output(data, file_name):
    """Save output to JSON or TXT file"""
    if file_name.endswith(".json"):
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
    else:
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(json.dumps(data, indent=2))
    print(f"📁 Data exported to {file_name}")

def extract_user_data(user_data):
    """Extract and format all available user data"""
    user = user_data.get("user", {})
    profile = user_data.get("user_profile", {})
    
    extracted_data = {
        "Discord ID": user.get("id"),
        "Username": user.get("username"),
        "Display Name": user.get("global_name"),
        "Discriminator": user.get("discriminator"),
        "Bio": profile.get("bio", "N/A"),
        "Pronouns": profile.get("pronouns", "N/A"),
        "Avatar": f"https://cdn.discordapp.com/avatars/{user.get('id')}/{user.get('avatar')}.png" if user.get("avatar") else "N/A",
        "Banner": f"https://cdn.discordapp.com/banners/{user.get('id')}/{user.get('banner')}.png" if user.get("banner") else "N/A",
        "Accent Color": user.get("accent_color", "N/A"),
        "Badges": [badge["description"] for badge in user_data.get("badges", [])],
        "Connected Accounts": {
            account["type"]: account["name"] for account in user_data.get("connected_accounts", [])
        },
        "Mutual Servers": [guild["id"] for guild in user_data.get("mutual_guilds", [])],
        "Legacy Username": user_data.get("legacy_username", "N/A"),
        "Premium Type": user_data.get("premium_type", "No Nitro"),
    }
    
    return extracted_data

def main(id, file_name="output.json", token=None):
    """Main function to scrape Discord user information."""
    if not token:
        token = get_token()

    headers = {'Authorization': token}

    print(f"🔍 Checking ID: {id}")

    user_data = get_user_info(id, token)

    if user_data:
        formatted_data = extract_user_data(user_data)
        print("\n🔹 **Extracted Data:**")
        for key, value in formatted_data.items():
            print(f"➡️ {key}: {value}")

        save_output(formatted_data, file_name)
    else:
        print("❌ No data found for this ID.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("id", help="The Discord User ID to scrape")
    parser.add_argument("-f", "--file", help="The file name to export to", default="output.json")
    parser.add_argument("-t", "--token", help="The Discord token to use (Optional, will use token.txt if not provided)", default=None)
    args = parser.parse_args()

    output_file = args.file if args.file else "output.json"
    main(args.id, output_file, args.token)
