from pathlib import Path
from tinydb import TinyDB
from config import Config


class SoundFile:
    def __init__(self, channel_name, command_name=None):
        self.command_name = command_name
        self.config = Config(channel_name)
        if self.config.discord_id:
            self.guild_id = self.config.discord_id

        self.path = Path.parent / 'discordbot' / 'sounds'

        self.file_path = self.path / f'{self.title}'

        self.db_path = Path.parent / 'discordbot' / 'sounds' / f'sounds_{self.guild_id}.json'
        self.db = TinyDB(self.db_path)

        if self.guild_id:
            self.config.sounds = self.db_path
        else:
            self.config.sounds = None

        self.config.update_config()

