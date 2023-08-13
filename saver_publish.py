import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from git import Repo, Actor, GitCommandError


# Important config
GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"
REMOTE_URL = "YOUR_GITHUB_REPO_URL"
BASE_URL = "THE_URL_OF_THE_WEBSITE_YOU_WANT_TO_SAVE"
DIRECTORY = "THE_LOCAL_DIRECTORY_YOU_WANT_TO_SAVE_THE_WEBSITE_IN"
GIT_AUTHOR_NAME = "Mahmoud Sameh"
GIT_AUTHOR_EMAIL = "mahmoud.sameh0101@gmail.com"


if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)
os.chdir(DIRECTORY)
urls_done = set()


def relative_url(url):
    # true if the url links to somewhere on the website being saved
    if url.startswith("/"):
        return True
    else:
        return False


def download_static_file(path):
    # takes relative url of static file and saves it in corresponding dir
    # Create directory if it doesn't exist
    path_s = path.strip('/')
    os.makedirs(os.path.dirname(path_s), exist_ok=True)
    url = BASE_URL.strip('/')
    url = url + '/' + path_s
    print(url)
    # Download the file

    with open(path_s, 'wb') as f:
        content = requests.get(url).content
        f.write(content)

    # Check if the file is a JavaScript file
    if path_s.endswith('.js'):
        # Find all local links in the JavaScript file
        soup = BeautifulSoup(content, 'html.parser')
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            if href.startswith('/'):
                download_static_file(href)


def enter_url(url):
    print("Processing:", url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    path = urlparse(url).path.strip('/')

    # If there is no path then it's index page
    if not path:
        with open('index.html', 'w') as HTMLfile:
            HTMLfile.write(page.content.decode())
        print("index file created")
    elif not "/" in path:
        with open(path + ".html", 'w') as HTMLfile:
            HTMLfile.write(page.content.decode())
        print("file", path + ".html", "has been created")
    else:
        path_parts = path.split('/')
        folder = '/'.join(path_parts[:-1])
        file_name = path_parts[-1]

        if not os.path.exists(os.path.dirname(folder)):
            try:
                os.makedirs(folder)
            except:
                print("An error while creating dir happened")

        with open(f"{folder}/{file_name}.html", 'w') as HTMLfile:
            HTMLfile.write(page.content.decode())
        print(file_name + ".html", "has been created")

    # download associated resources
    links = soup.find_all("link")
    scripts = soup.find_all("script")
    imgs = soup.find_all("img")
    for link in links:
        href = link.get("href")
        if not href:
            continue
        if relative_url(href):
            download_static_file(href)
    for script in scripts:
        src = script.get("src")
        if not src:
            continue
        if relative_url(src):
            download_static_file(src)
    for img in imgs:
        src = img.get("src")
        if not src:
            continue
        if relative_url(src):
            download_static_file(src)

    anchors = soup.find_all("a")
    for anchor in anchors:
        new_url = anchor.get('href')
        if new_url.startswith('/'):
            new_url = new_url.strip('/')
            if new_url and not new_url in urls_done:
                urls_done.add(new_url)
                enter_url(BASE_URL + new_url)


enter_url(BASE_URL)
print("Done saving.")


# Pushing the saved files to github deployment
if input("Do you want to publish changes? ").lower() in ("yes", "y", "ye", "yeah"):
    try:
        repo = Repo(DIRECTORY)
        repo.git.add(update=True)
        author = Actor(GIT_AUTHOR_NAME, GIT_AUTHOR_EMAIL)
        commit_message = input("Your commit message: ")
        repo.index.commit(commit_message, author=author)
        print("Added and Committed everything successfully")

        origin = repo.remote('origin')
        origin.push(refspec='HEAD:refs/heads/main')
        print("Pushed changes successfully")
    except GitCommandError as e:
        print("Error occurred while pushing to remote repository:", e)