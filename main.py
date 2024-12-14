import os
from dotenv import load_dotenv

from util import Github
from template.generate import generate_site
from template.fetch import fetch_github

def load_constants(year: int):
    load_dotenv()

    try:
        global ACCESS_TOKEN
        ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

        global USERNAME
        USERNAME = os.getenv("GITHUB_USERNAME")
    except Exception as e:
        print(f"You need to set the GITHUB_ACCESS_TOKEN and GITHUB_USERNAME environment variables: {e}")
        exit(1)

    global YEAR
    YEAR = year

    global TIMEZONE
    TIMEZONE = "Asia/Shanghai"

if __name__ == "__main__":
    load_constants(2024)

    github = Github(access_token=ACCESS_TOKEN, username=USERNAME, timezone=TIMEZONE)

    fetch_github(github, YEAR, skip_fetch=False)

    generate_site(YEAR)
