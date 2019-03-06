from bs4 import BeautifulSoup
import requests
import os
import configparser
from config.config import Config

#g = git.cmd.Git(os.getcwd())
#g.pull()

offline_config = Config()
offline_config_data = offline_config.get_config_data()
offline_version = offline_config_data()
class Updater:
    def __init__(self):
        self.repo_url = 'https://raw.githubusercontent.com/anderswodenker/sams/master/version.html?token=AOIaPSFEkhdWQNkNCQvWV0uWwJ_T9xMAks5chXLTwA%3D%3D'
        self.version_url = os.getcwd() + "/version.html"
        self.old_version = ""


def update():
    url = 'https://raw.githubusercontent.com/anderswodenker/sams/master/version.html?token=AOIaPSFEkhdWQNkNCQvWV0uWwJ_T9xMAks5chXLTwA%3D%3D'

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    version = soup.find(id="version")

    return version.get_text()


print(update())