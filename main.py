import sys

import qbittorrentapi
import json
from ui import UI

print("Connecting to qBittorrent WebUI...")

with open('config.json') as json_file:
    config = json.load(json_file)
    host = config['host']
    username = config['username']
    password = config['password']

if not host:
    host = input("Enter host: ")
if not username:
    username = input("Enter username: ")
if not password:
    password = input("Enter password: ")

torrent_client = qbittorrentapi.Client(host=host, username=username, password=password)


try:
    torrent_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print("Failed to connect:", e)
    sys.exit(1)

ui = UI(torrent_client)
ui.run()
