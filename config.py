import os
import json
from pathlib import Path

class Config:
    def __init__(self, channel_name):
        self.path = Path.cwd() / 'configs' / f'{channel_name}_config.json'
        
        if self.path.is_file():
            config_data = self.get_config()
        else:
            config_data = {}

        self.prefix = config_data.get('prefix', '!')
        self.channel_name = config_data.get('channel_name', channel_name)
        self.shoutout_message = config_data.get('shoutout_message', 'Go check out this awesome person! ')
        self.discord_id = config_data.get('discord_id', None)
        self.discord_message = config_data.get('discord_message', 'Feel free to join the Discord to stay connected in '
                                                                  'between streams!: ')
        self.discord_invite_link = config_data.get('discord_invite_link', None)
        self.commands = Path.cwd() / 'commands' / f'commands_{channel_name}.json'
        self.quotes = Path.cwd() / 'quotes' / f'quotes_{channel_name}.json'
        self.sounds = Path.cwd().parent / 'discordbot - testing' / 'sounds' / f'sounds_{self.discord_id}.json'
        
        #if len(config_data) == 0:
        self.update_config()

    def to_json(self):
        property_dict = {
                "prefix": self.prefix,
                "channel_name": self.channel_name,
                "shoutout_message": self.shoutout_message,
                "discord_id": self.discord_id,
                "discord_message": self.discord_message,
                "discord_invite_link": self.discord_invite_link,
                "commands": str(self.commands),
                "quotes": str(self.quotes),
                "sounds": str(self.sounds),
                }

        return json.dumps(property_dict, indent=2)

    def update_config(self):
        with open(self.path.absolute(), "w") as config_file:
            config_file.write(self.to_json())

    def get_config(self):
        try:
            with open(self.path.absolute()) as config_file:
                return json.load(config_file)
        except FileNotFoundError:
            self.update_config()
            self.get_config()
        


