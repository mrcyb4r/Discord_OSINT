import requests
try:
    import modules.utils as utils
except ModuleNotFoundError:
    import utils

def get_twitch_stats(username):
    r = requests.get(f"https://api.ivr.fi/v2/twitch/user?login={username}")

    if r.json() == []:
        utils.print_neutral(f"No stats found for {username}", indent=1)
        return []
    
    data = r.json()[0]

    stats = {
        "banned": data["banned"],
        "display name": data["displayName"],
        "bio": data["bio"],
        "followers": data["followers"],
        "created at": data["createdAt"],
        "updated at": data["updatedAt"]
    }

    if len(stats) == 0:
        utils.print_neutral("No stats found.", indent=1)
        return
    
    utils.print_found(f"Found {len(stats)} user statistics.", indent=1)

    stats_list = []
    for stat in stats:
        utils.print_result(f"{stat}: {stats[stat]}", indent=2)
        stats_list.append(f"{stat}: {stats[stat]}")
        
    return stats_list

def get_twitch_mods_vips(username):
    r = requests.get(f"https://api.ivr.fi/v2/twitch/modvip/{username}")

    mods = r.json()["mods"]
    vips = r.json()["vips"]

    # combine the two lists
    friends = mods + vips

    if len(friends) == 0:
        utils.print_neutral("No mods or vips found.", indent=1)
        return
    
    utils.print_found(f"Found {len(friends)} mods and vips.", indent=1)

    print(friends)

    max_length = 0
    for friend in friends:
        if friend['login'] == None:
            friends.remove(friend)
        else:
            if len(friend['login']) > max_length:
                max_length = len(friend['login'])

    friends_list = []
    for friend in friends:
        utils.print_result(f"{friend['login']: <{max_length}} | {friend['login']}", indent=2)
        friends_list.append({"name": friend['login'], "url": f"https://twitch.tv/{friend['login']}"})

    return friends_list

if __name__ == "__main__":
    get_twitch_stats("xqc")