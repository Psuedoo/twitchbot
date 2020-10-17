import os
import json
from pathlib import Path

class Config:
    def __init__(self, channel_name):
        self.path = Path('.') / 'configs' / f'{channel_name}_config.json'
        
        if self.path.is_file():
            config_data = self.get_config()
        else:
            config_data = {}

        self.prefix = config_data.get('prefix', '!')
        self.channel_name = config_data.get('channel_name', channel_name)
        self.quotes = config_data.get('quotes', f'quotes/quotes_{channel_name}.json')
        self.shoutout_message = config_data.get('shoutout_message', 'Go check out this awesome person! ')
        self.discord_message = config_data.get('discord_message', 'Feel free to join the Discord to stay connected in between streams!: ')
        self.discord_invite_link = config_data.get('discord_invite_link', None)
        self.sounds = config_data.get('sounds', 'sounds directory based on channel name')
        
        if len(config_data) == 0:
            self.update_config()

    def to_json(self):
        property_dict = {
                "prefix": self.prefix,
                "channel_name": self.channel_name,
                "shoutout_message": self.shoutout_message,
                "discord_message": self.discord_message,
                "discord_invite_link": self.discord_invite_link,
                "commands": self.commands,
                "quotes": self.quotes,
                "sounds": self.sounds,
                }

        return json.dumps(property_dict, indent=2)


    def create_config(self):
        if self.path.is_file():
            print(f"{self.path} already exists.")
            return None

        else:
            print(f"Created {self.path}")
            self.update_config()
    
    def update_config(self):
        with open(self.path.absolute(), "w") as config_file:
            config_file.write(self.to_json())

    def get_config(self):
        try:
            with open(self.path.absolute()) as config_file:
                return json.load(config_file)
        except FileNotFoundError:
            self.update_config()
        


