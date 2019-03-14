import requests
import os
import configparser
from config.config import Config
import subprocess
import git
from threading import Thread

#g = git.cmd.Git(os.getcwd())
#g.pull()

# offline config
off_config = configparser.ConfigParser()
on_config = configparser.ConfigParser()


def get_off_config_data():
    off_config.read('/var/www/upload/config/version.ini')
    return off_config


def get_on_config_data():
    url = 'https://raw.githubusercontent.com/anderswodenker/sams/master/config/version.ini'
    r = requests.get(url)
    with open('/var/www/upload/config/online_config.ini', 'wb') as f:
        f.write(r.content)
    on_config.read('/var/www/upload/config/online_config.ini')
    return on_config


offline_version = get_off_config_data()
online_version = get_on_config_data()
online_version = float(online_version['DEFAULT']['version'])
offline_version = float(offline_version['DEFAULT']['version'])


def pull():
    process = subprocess.Popen(["git", "pull", "origin", "master"], stdout=subprocess.PIPE)
    output = process.communicate()[0]


def add():
    add = subprocess.Popen(["git", "add", "."], stdout=subprocess.PIPE)
    output = add.communicate()[0]


def commit():
    commit = subprocess.Popen(["git", "commit", "-a", "-m", "update"], stdout=subprocess.PIPE)
    output = commit.communicate()[0]


thread_pull = Thread(target=pull)
thread_add = Thread(target=add)
thread_commit = Thread(target=commit)

if online_version > offline_version:
    print("update available")
    thread_pull.start()
    thread_pull.join()
    print("pull done")
    thread_add.start()
    thread_add.join()
    print("add done")
    thread_commit.start()
    thread_commit.join()
    print("done!")