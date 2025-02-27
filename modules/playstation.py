import bs4
import sys
import cloudscraper

try:
    import modules.utils as utils
except ModuleNotFoundError:
    import utils

requests = cloudscraper.create_scraper()

def get_profile_stats(psn_id):
    r = requests.get(f"https://psnprofiles.com/{psn_id}")

    soup = bs4.BeautifulSoup(r.text, "html.parser")

    stats = soup.find("meta", attrs={"name": "Description"})["content"].split(" • ")[1:]

    new_stats = []
    for stat in stats:
        if stat.startswith("Level"):
            new_stats.append(f"Level: {stat.split(' ')[1]}")
        elif stat.endswith("Trophies"):
            new_stats.append(f"Trophies: {stat}")
        elif stat.endswith("Games"):
            new_stats.append(f"Games: {stat}")

    stats = new_stats

    nav = soup.find("ul", {"class": "navigation"})
    last = nav.find_all("li")[-1]
    last_link = last.find("a")["href"]

    if last.text == "Forum Profile":
        stats.append(f"Forum Profile: {last_link}")

    if len(stats) == 0:
        utils.print_neutral("No stats found.", indent=1)
        return
    else:
        utils.print_found(f"Found {len(stats)} user statistics.", indent=1)

    for stat in stats:
        utils.print_result(stat, indent=2)

    
    return stats

if __name__ == "__main__":
    get_profile_stats(sys.argv[1])