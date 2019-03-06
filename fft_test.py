import requests
import os
import configparser
from config.config import Config

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


print(online_version)
print(offline_version)



