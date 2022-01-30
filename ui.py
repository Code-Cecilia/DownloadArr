import subprocess
import sys

from misc import *


class UI:

    def __init__(self, torrent_client):
        self.torrent_client = torrent_client
        self.cls()
        self.title_screen()
        self.input_options = {
            "Add torrent": self.add_torrent,
            "Remove torrent": self.remove_torrent,
            "List torrents": self.list_torrents,
            "Modify torrent": self.modify_torrent,
            "Get info for torrent": self.get_info_for_torrent,
            "Exit": self.exit_prog
        }

    def run(self):
        while True:
            choice = self.get_input()
            self.cls()
            self.input_options[list(self.input_options)[choice - 1]]()

    def title_screen(self):
        self.cls()
        print("""Welcome to the Torrent Manager\n""")

    def cls(self):
        if sys.platform == "win32":
            subprocess.call("cls", shell=True, stderr=subprocess.DEVNULL)
        else:
            subprocess.call("clear", shell=True, stderr=subprocess.DEVNULL)

    def exit_prog(self):
        self.cls()
        sys.exit()

    def get_input(self, options=None):
        if not options:
            options = self.input_options
        for i, option in enumerate(options):
            print(f"{i + 1}. {option}")
        try:
            choice = int(input("\nEnter a the choice: "))
            if choice not in range(1, len(options) + 1):
                raise ValueError
            return choice
        except ValueError:
            print("\nInvalid choice")
            self.cls()
            self.get_input()

    def add_torrent(self):
        input_torrents = input("Enter the magnet URI: ")
        save_path = input("Enter the save path (leave for default): ")
        if not save_path:
            save_path = None
            print(f"Using default save path...")

        self.torrent_client.torrents_add(urls=input_torrents, save_path=save_path)
        input("\nTorrent added! Press any key to continue: ")
        self.cls()

    def remove_torrent(self):
        torrents = self.torrent_client.torrents_info()
        if not torrents:
            print("\nNo torrents found\n")
            input("Press any key to continue: ")
            self.cls()
            return
        print("Select the torrent to delete.\n")
        choice = self.get_input([t['name'] for t in torrents])
        torrent_to_modify = torrents[choice - 1]
        torrent_hash = torrent_to_modify['hash']
        self.cls()
        self.torrent_client.torrents_delete(torrent_hashes=torrent_hash)
        input("\nDone! Press any key to continue:")
        self.cls()

    def list_torrents(self):
        torrents = self.torrent_client.torrents_info()
        if not torrents:
            print("\nNo torrents found\n")
            input("Press any key to continue:")
            self.cls()
            return
        for i, torrent in enumerate(torrents):
            print(f"{i + 1}. {torrent['name']} | State: {camel_to_sentence(torrent['state'], {'DL': 'Download'})} | "
                  f"{torrent['progress']*100:.2f}% downloaded")
        print("\n")

        input("Press any key to continue: ")
        self.cls()

    def get_info_for_torrent(self):
        torrents = self.torrent_client.torrents_info()
        if not torrents:
            print("\nNo torrents found\n")
            input("Press any key to continue: ")
            self.cls()
            return
        print("Select the torrent to get info for.\n")
        choice = self.get_input([t['name'] for t in torrents])
        torrent_to_get_info_for = torrents[choice - 1]
        self.cls()

        print(f"Info for: {torrent_to_get_info_for['name']}")
        print("\n")
        print(f"Content Path: {torrent_to_get_info_for['content_path']}")
        print(f"Seeders: {torrent_to_get_info_for['num_seeds']} | Leechers: {torrent_to_get_info_for['num_leechs']}")
        print(f"State: {camel_to_sentence(torrent_to_get_info_for['state'], {'DL': 'Download'})}")
        downloaded, total_size = bytes_to_nearest(torrent_to_get_info_for['downloaded']), bytes_to_nearest(torrent_to_get_info_for['total_size'])
        print(f"Progress: {downloaded} downloaded of {total_size} ({torrent_to_get_info_for['progress']*100:.2f}%)")
        print(f"Download speed: {bytespersec_to_megabytespersec(torrent_to_get_info_for['dlspeed']):.2f} MB/s")
        print(f"Upload speed: {bytespersec_to_megabytespersec(torrent_to_get_info_for['upspeed']):.2f} MB/s")
        print(f"Completion ETA: {pretty_time_remaininf(torrent_to_get_info_for['eta'])}")
        print("")  # leave some gap because magnet uri will be a long string,
        # and printing it separately will look a bit nicer
        print(f"Magnet URI: {torrent_to_get_info_for['magnet_uri']}")

        print("\n")
        input("Press any key to continue: ")
        self.cls()

    def modify_torrent(self):
        torrents = self.torrent_client.torrents_info()
        if not torrents:
            print("\nNo torrents found\n")
            input("Press any key to continue: ")
            self.cls()
            return
        print("Select the torrent to modify.\n")
        choice = self.get_input([t['name'] for t in torrents])
        torrent_to_modify = torrents[choice - 1]
        torrent_hash = torrent_to_modify['hash']
        self.cls()

        print(f"Modifying: {torrent_to_modify['name']}")
        print(f"Current state: {camel_to_sentence(torrent_to_modify['state'], {'DL': 'Download'})}")
        print("")
        choices = {
            "Pause": self.torrent_client.torrents_pause,
            "Resume": self.torrent_client.torrents_resume,
            "Delete": self.torrent_client.torrents_delete,
        }
        choice = self.get_input(choices)
        if choice == 3:  # if we are deleting the torrent, ask if you want to keep the downloaded files
            delete_files = input("Do you want to DELETE the downloaded files? (y/n): ")
            if delete_files.lower() == "y":
                self.torrent_client.torrents_delete(torrent_hashes=torrent_hash, delete_files=True)
            else:
                self.torrent_client.torrents_delete(torrent_hashes=torrent_hash)
        else:
            choices[list(choices)[choice-1]](torrent_hashes=torrent_hash)
        input("Done! Press any key to continue:")
        self.cls()
