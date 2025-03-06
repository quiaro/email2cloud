import os
import json

def load_config(config_file):
    """Loads configuration from a JSON file."""
    if not os.path.exists(config_file):
        print(f"Error: Configuration file {config_file} not found.")
        exit(1)

    with open(config_file, "r") as file:
        return json.load(file)