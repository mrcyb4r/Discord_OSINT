import argparse
import requests
import time

try:
    import modules.utils as utils
except ModuleNotFoundError:
    import utils

def get_user_info(data):
    stats = []

    try:
        for stat in data["metadata"]:
            stats.append(f"{stat.replace('_', ' ')}: {data['metadata'][stat]}")
    except KeyError:
        pass

    if len(stats) == 0:
        utils.print_neutral("No stats found.", indent=1)
        return
    
    utils.print_found(f"Found {len(stats)} user statistics.", indent=1)

    stats_list = []
    for stat in stats:
        utils.print_result(stat, indent=2)
        stats_list.append(stat)

    return stats_list

