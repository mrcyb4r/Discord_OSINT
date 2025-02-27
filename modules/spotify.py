import requests
from bs4 import BeautifulSoup
import json
import modules.utils as utils

def get_access_token(spotifyid):
    r = requests.get(f"https://open.spotify.com/user/{spotifyid}/following")
    soup = BeautifulSoup(r.text, 'html.parser')
    script = soup.find("script", {"id": "session"})
    data = json.loads(script.string)
    return data['accessToken']

def get_user_stats(spotifyid):
    access_token = get_access_token(spotifyid)
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get(f"https://spclient.wg.spotify.com/user-profile-view/v3/profile/{spotifyid}?market=from_token", headers=headers)
    data = r.json()

    stats = []
    try:
        stats.append(f"Name: {data['name']}")
    except KeyError: pass
    try:
        stats.append(f"Followers: {data['followers_count']}")
    except KeyError: pass
    try: 
        stats.append(f"Following: {data['following_count']}")
    except KeyError: pass

    if len(stats) == 0:
        utils.print_neutral("No stats found.", indent=1)
        return
    
    utils.print_found(f"Found {len(stats)} user statistics.", indent=1)

    for stat in stats:
        utils.print_result(stat, indent=2)

    return stats

def get_user_followers(spotifyid):
    access_token = get_access_token(spotifyid)
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get(f"https://spclient.wg.spotify.com/user-profile-view/v3/profile/{spotifyid}/followers?market=from_token", headers=headers)
    data = r.json()

    followers = []
    for follower in data.get('profiles', []):
        followers.append({
            "name": follower['name'],
            "url": f"https://open.spotify.com/user/{follower['uri'].split(':')[-1]}"
        })

    if len(followers) == 0:
        utils.print_neutral("No followers found.", indent=1)
        return
    
    utils.print_found(f"Found {len(followers)} followers.", indent=1)

    max_length = 0
    for follower in followers:
        if len(follower['name']) > max_length:
            max_length = len(follower['name'])

    for follower in followers:
        utils.print_result(f"{follower['name']: <{max_length}} | {follower['url']}", indent=2)

    return followers