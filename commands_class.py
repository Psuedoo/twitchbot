import os
from config import Config
from tinydb import TinyDB, Query
from pathlib import Path

class Command:
    def __init__(self, channel):
        self.config = Config(channel)
        self.db_path = Path.cwd() / 'commands' / f'commands_{self.config.channel_name}.json'
        self.db = TinyDB(self.db_path)

    def add_command(self, command_name, command_response):
        # Adds command to db  
        pass

    def delete_command(self, command_name):
        # Deletes command from db
        pass

    def get_commands(self):
        # Returns list or dict of commands from db
        pass

    def get_command(self, command_name):
        # Returns single command from db
        pass



