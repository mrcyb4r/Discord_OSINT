import argparse
import requests
import time
import json
import re
import random

try:
    import modules.utils as utils
except ModuleNotFoundError:
    import utils

def get_channel_links(channel_id):
    try:
        # Initial request to get the channel page content
        response = requests.get(f"https://www.youtube.com/channel/{channel_id}")
        response.raise_for_status()  # Check for request errors

        # Extract ytInitialData JSON using regex
        match = re.search(r'var ytInitialData = ({.*?});</script>', response.text)
        if not match:
            utils.print_negative("Failed to extract channel data.")
            return []

        data = json.loads(match.group(1))

        # Navigate through the JSON structure to find the channel links. This path may need adjustments.
        tabs = data.get('contents', {}).get('twoColumnBrowseResultsRenderer', {}).get('tabs', [])
        for tab in tabs:
            if 'tabRenderer' in tab:
                tabRenderer = tab['tabRenderer']
                if tabRenderer.get('title', '') == 'About':
                    links_section = tabRenderer.get('content', {}).get('sectionListRenderer', {}).get('contents', [])[0].get('itemSectionRenderer', {}).get('contents', [])[0].get('channelAboutFullMetadataRenderer', {}).get('primaryLinks', [])
                    links = [link['navigationEndpoint']['urlEndpoint']['url'] for link in links_section if 'navigationEndpoint' in link and 'urlEndpoint' in link['navigationEndpoint']]
                    utils.print_found(f"Found {len(links)} links.", indent=1)
                    for link in links:
                        utils.print_info(link, indent=2)
                    return links
        utils.print_neutral("No links on channel found.", indent=1)
        return []

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def get_channel_stats(id):

    r = requests.get("https://www.youtube.com/channel/" + id)
    
    # match var ytInitialData = {<data>};
    # data is a json object
    data = r.text.split("var ytInitialData = ")[1].split(";</script>")[0]

    # find continuationCommand in data using regex
    continuationCommand = re.search(r'continuationCommand":\{"token":"(.*?)"', data).group(1)

    data = json.loads(data)

    resolved_url = "https://www.youtube.com" + data['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['endpoint']['browseEndpoint']['canonicalBaseUrl']

    utils.print_found(resolved_url, indent=1)

    json_data = {
        'context': {
            'client': {
                'clientName': 'WEB',
                'clientVersion': '2.20240210.05.00',
                
                'originalUrl': 'https://www.youtube.com/channel/UCFk_bBOML-hsy7C90P6_zRQ',
                'mainAppWebInfo': {
                    'graftUrl': 'https://www.youtube.com/channel/UCFk_bBOML-hsy7C90P6_zRQ'
                },
            }
        },
        'continuation': continuationCommand,
    }

    response = requests.post(
        'https://www.youtube.com/youtubei/v1/browse',
        json=json_data,
    )

    stats = []

    try:
        total_videos = response.json()['onResponseReceivedEndpoints'][0]['appendContinuationItemsAction']['continuationItems'][0]['aboutChannelRenderer']['metadata']['aboutChannelViewModel']['videoCountText']
        stats.append(f"Total videos: {total_videos.split(' ')[0]}")
    except KeyError:
        pass

    try:
        total_views = response.json()['onResponseReceivedEndpoints'][0]['appendContinuationItemsAction']['continuationItems'][0]['aboutChannelRenderer']['metadata']['aboutChannelViewModel']['viewCountText']
        stats.append(f"Total views: {total_views.split(' ')[0]}")
    except KeyError:
        pass

    try:
        total_subscribers = response.json()['onResponseReceivedEndpoints'][0]['appendContinuationItemsAction']['continuationItems'][0]['aboutChannelRenderer']['metadata']['aboutChannelViewModel']['subscriberCountText']
        stats.append(f"Total subscribers: {total_subscribers.split(' ')[0]}")
    except KeyError:
        pass
    
    try:
        joined = response.json()['onResponseReceivedEndpoints'][0]['appendContinuationItemsAction']['continuationItems'][0]['aboutChannelRenderer']['metadata']['aboutChannelViewModel']['joinedDateText']['content']
        stats.append(f"Joined: {joined.split('Joined ')[1]}")
    except KeyError:
        pass

    try:
        country = response.json()['onResponseReceivedEndpoints'][0]['appendContinuationItemsAction']['continuationItems'][0]['aboutChannelRenderer']['metadata']['aboutChannelViewModel']['country']
        stats.append(f"Country: {country}")
    except KeyError:
        pass

    if len(stats) == 0:
        utils.print_neutral("No channel stats found.", indent=1)
        return
    
    utils.print_found(f"Found {len(stats)} channel statistics.", indent=1)

    stats_list = []
    for stat in stats:
        utils.print_result(stat, indent=2)
        stats_list.append(stat)

    return stats_list


def get_yt_api():

    keys = [
        "AIzaSyD6xmCCs6zcZlQSILK1MN9oTsnGLIJ8mC8",
        # "AIzaSyCofN8CoeszlCiDeLwl-6BZYPunOOZETt4"
    ]

    return random.choice(keys)

def get_description_links(channel_id, pageToken='', links=None):
    if links is None:
        links = []

    key = get_yt_api()

    unparsing_url = f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&maxResults=50&key={key}&alt=json&pageToken={pageToken}"

    res = requests.get(unparsing_url)
    data = res.json()

    if res.status_code == 403:
        utils.print_negative("Youtube API limit reached", indent=1)
        return links

    for item in data["items"]:
        link = re.search(r'(www|http:|https:)+[^\s]+[\w]', item["snippet"]["description"])
        if link:
            links.append(link.group())

    if "nextPageToken" in data:
        next_page_token = data["nextPageToken"]
        return get_description_links(channel_id, next_page_token, links)
    else:
        if len(links) == 0:
            utils.print_neutral("No links in description found.", indent=1)
            return links
        
        utils.print_found(f"Found {len(set(links)   )} links in video descriptions.")
        for link in set(links):
            utils.print_result(link, indent=2)

        return links

def get_description_emails(channel_id, pageToken='', emails=[]):
    key = get_yt_api()

    unparsing_url = f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&maxResults=50&key={key}&alt=json&pageToken={pageToken}"

    res = requests.get(unparsing_url)
    data = res.json()

    if res.status_code == 403:
        utils.print_negative("Youtube API limit reached", indent=1)
        return emails

    for item in data["items"]:
        email = re.search(r'[\w\.-]+@[\w\.-]+', item["snippet"]["description"])
        if email:
            emails.append(email.group())

    if "nextPageToken" in data:
        next_page_token = data["nextPageToken"]
        return get_description_emails(channel_id, next_page_token, emails)
    else:
        if len(emails) == 0:
            utils.print_neutral("No emails in descriptions found.", indent=1)
            return emails
        
        utils.print_found(f"Found {len(emails)} emails in video descriptions.")
        for email in emails:
            utils.print_result(email, indent=2)

        return emails