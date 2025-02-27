import argparse
import requests
import time
import re
import whois

try:
    import modules.utils as utils
except ModuleNotFoundError:
    import utils

def whois_lookup(domain):
    domain = whois.whois(domain)

    if domain is None:
        utils.print_neutral("No information found.")
        return

    utils.print_found("Found domain information:", indent=1)

    for key, value in domain.items():
        if key == "name_servers":
            utils.print_result(f"{key}:")
            for ns in value:
                utils.print_result(f"  - {ns}")
        elif key == "emails":
            utils.print_result(f"{key}:")
            for email in value:
                utils.print_result(f"  - {email}")
        elif key == "updated_date" or key == "creation_date" or key == "expiration_date":
            utils.print_result(f"{key}:")
            for date in value:
                utils.print_result(f"  - {date}")
        else:
            utils.print_result(f"{key}: {value}", indent=2)

whois_lookup("xera.ca")