try:
    import modules.utils as utils
except ModuleNotFoundError:
    import utils

def get_links_in_bio(bio):
    links = utils.get_links(bio)
    links_list = []
    if len(links) > 0:
        utils.print_found(f"Found {len(links)} links in bio.", indent=1)
        for link in links:
            utils.print_result(link, indent=2)
            links_list.append(link)
    else:
        utils.print_neutral("No links found in bio.", indent=1)

    return links_list


def get_email_in_bio(bio):
    emails = utils.get_emails(bio)
    emails_list = []
    if len(emails) > 0:
        utils.print_found(f"Found {len(emails)} emails in bio.", indent=1)
        for email in emails:
            utils.print_result(email, indent=2)
            emails_list.append(email)
    else:
        utils.print_neutral("No emails found in bio.", indent=1)

    return emails_list