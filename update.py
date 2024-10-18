# This allows you to move a sensor and reassign its location
# Usage:
#    python update.py

import json
from os import path
from pathlib import Path

config_path = Path(path.dirname(__file__)) / 'config.json'
config = json.loads(config_path.read_text())

device = ''
location = '' 

while not device in config["devices"]:
    device = input(f"Which device ({', '.join(config['devices'])}) have you moved? ")

while not location in config["locations"]:
    location = input(f"Where did you move it? ({', '.join(config['locations'])}) ")
