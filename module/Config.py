import json

CONFIG_FILE = 'resources/config.json'

with open(CONFIG_FILE) as config_file:
    config = json.load(config_file)


def write():
    with open(CONFIG_FILE) as config_file:
        json.dump(config, config_file)
