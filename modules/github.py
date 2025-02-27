import argparse
import requests
import time

try:
    import modules.utils as utils
except ModuleNotFoundError:
    import utils

DEBUG = False

class FindGitEmail:
    def __init__(self, username):
        self.git_username = username
        self.apiURL = "https://api.github.com"

    def get(self):
        return self.__checkUserExists()

    def __checkUserExists(self):
        response = requests.get(self.apiURL + "/users/" + self.git_username)
        response_json = response.json()

        if response.status_code == 200:
            start_time = time.time()
            emails = self.__getEmail()
            execution_time = "{:.2f}s".format(time.time() - start_time)
            return {'found': True, 'execution_time': execution_time, 'email': emails}
        elif str(response_json["message"]).startswith("API"):
            return {'found': False, 'error_message': str(response_json["message"] + " Documentation URL: " + response_json["documentation_url"])}
        else:
            return {'found': False, 'error_message': "Provided GitHub username: " + self.git_username + " does not exist."}

    def __getEmail(self):
        email_sources = {}

        reposURL = self.apiURL + "/users/" + self.git_username + "/repos"
        repos = requests.get(reposURL).json()

        for repo in repos:
            repo_name = repo["name"]
            if repo["fork"] is False:
                commitsURL = self.apiURL + "/repos/" + self.git_username + "/" + repo_name + "/commits"
                commits = requests.get(commitsURL).json()

                for commit in commits:
                    try:
                        if commits["message"] == "Git Repository is empty.":
                            continue
                    except:
                        try:
                            commit_email = commit["commit"]["author"]["email"]
                            commit_name = commit["author"]["login"]
                        except TypeError as e:
                            continue

                        if commit_email not in email_sources:
                            email_sources[commit_email] = []
                        email_sources[commit_email].append(f'Repo: https://www.github.com/{self.git_username}/{repo_name}, User: {commit_name}')

        if len(email_sources) != 0:
            return email_sources

        commitsURL = self.apiURL + "/users/" + self.git_username + "/events/public"
        payloads = requests.get(commitsURL).json()

        for payload in payloads:
            if payload["type"] == "PushEvent":
                data = payload["payload"]
                payload_email = str(data["commits"][0]["author"]["email"])
                payload_name = str(data["actor"]["login"])
                if payload_email not in email_sources:
                    email_sources[payload_email] = []
                email_sources[payload_email].append(f'Public Commit, User: {payload_name}')

        return email_sources

def find(username):
    finder_response = FindGitEmail(username).get()
    return finder_response

def get_email(username):

    response = find(username)

    if response['found'] is False:
        if "API rate limit exceeded for" in response['error_message']:
            utils.print_negative("GitHub api limit reached", indent=1)
        else:
            pass
        return

    email_sources = response['email']
    
    if response['found']:
        email_sources = {email: sources for email, sources in email_sources.items() if any(f'User: {username}' in source for source in sources)}
        
        # remove all users.noreply.github.com emails
        email_sources = {email: sources for email, sources in email_sources.items() if not email.endswith('users.noreply.github.com')}
        
        num_found_emails = len(email_sources)

        if num_found_emails == 0:
            utils.print_neutral(f"No emails found for GitHub user: {username}", indent=1)
            return

        utils.print_found(f"Found {num_found_emails} email{'s' if num_found_emails != 1 else ''} for GitHub user: {username}", indent=1)

        emails = []
        for email, sources in email_sources.items():
            utils.print_result(f"Email: {email}", indent=2)
            emails.append(email)

        return emails

        

def get_stats(username):
    r = requests.get(f"https://api.github.com/users/{username}")

    if r.status_code == 404:
        utils.print_neutral(f"No stats found for {username}", indent=1)
        return
    
    elif r.status_code == 403:
        utils.print_negative(f"GitHub api limit reached", indent=1)
        return

    elif r.status_code == 200:
        utils.print_found(f"Found stats for {username}", indent=1)

    data = r.json()

    if data['name'] is not None:
        utils.print_result(f"Name: {data['name']}", indent=2)

    if data['bio'] is not None:
        utils.print_result("Bio: " + data['bio'].strip('\\r').strip('\n'), indent=2)

    if data['company'] is not None:
        utils.print_result(f"Company: {data['company']}", indent=2)

    if data['location'] is not None:
        utils.print_result(f"Location: {data['location']}", indent=2)

    if data['blog'] is not None and data['blog'] != "":
        utils.print_result(f"Blog: {data['blog']}", indent=2)

    if data['twitter_username'] is not None:
        utils.print_result(f"Twitter: {data['twitter_username']}", indent=2)

    if data['public_repos'] is not None:
        utils.print_result(f"Public Repos: {data['public_repos']}", indent=2)

    return {
        "name": data['name'],
        "bio": data['bio'],
        "company": data['company'],
        "location": data['location'],
        "blog": data['blog'],
        "twitter_username": data['twitter_username'],
        "public_repos": data['public_repos']
    }