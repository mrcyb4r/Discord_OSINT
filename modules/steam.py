import requests
from bs4 import BeautifulSoup

try:
    import modules.utils as utils
except ModuleNotFoundError:
    import utils


def get_steam_names(steamid, steamname):
    r = requests.get(f"https://steamcommunity.com/profiles/{steamid}/ajaxaliases/")

    # merge the two lists
    names = r.json()

    if len(names) == 0:
        utils.print_neutral("No previous names found.", indent=1)
        return
    else:
        utils.print_found(f"Found {len(names)} previous names.", indent=1)

    max_length = 0
    for name in names:
        if len(name['newname']) > max_length:
            max_length = len(name['newname'])


    names_list = []
    for name in names:
        utils.print_result(f"{name['newname']: <{max_length}} | {name['timechanged']}", indent=2)
        names_list.append(name['newname'])

    return names_list

def get_steam_friends(steamid, steamname):
    r = requests.get(f"https://steamcommunity.com/profiles/{steamid}/friends/")

    soup = BeautifulSoup(r.text, 'html.parser')

    # friends are all divs with the data tag 'data-search'
    friends = soup.find_all("div", {"data-search": True})

    if len(friends) == 0:
        utils.print_neutral("No friends found.", indent=1)
        return
    else:
        utils.print_found(f"Found {len(friends)} friends.", indent=1)

    max_length = 0
    for friend in friends:
        if len(friend['data-search'].split(' ; ')[0]) > max_length:
            max_length = len(friend['data-search'].split(' ; ')[0])

    friends_list = []
    for friend in friends:
        utils.print_result(f"{friend['data-search'].split(' ; ')[0]: <{max_length}} | https://steamcommunity.com/profiles/{friend['data-steamid']}", indent=2)
        friends_list.append({"name": friend['data-search'].split(' ; ')[0], "url": f"https://steamcommunity.com/profiles/{friend['data-steamid']}"})

    return friends_list