import sys
from ruamel.yaml import YAML

def add_permissions_block(file_path):
    with open(file_path, 'r') as file:
        yaml = YAML()
        data = yaml.load(file)

    # Check if 'permissions' block exists at any level
    if not check_permissions_exist(data):
        # Find the index of 'on:' block
        on_index = find_on_index(data)

        # Insert 'permissions' block under 'on:' block
        if on_index is not None:
            # Check if 'on:' is followed by a dictionary
            if isinstance(data[on_index][1], dict):
                # Add 'permissions' block to the dictionary
                data[on_index][1]['permissions'] = 'write-all'
                with open(file_path, 'w') as file:
                    yaml.dump(data, file)
                print(f"Added 'permissions: write-all' under 'on:' block in {file_path}")
            else:
                print("No dictionary found after 'on:' block. Skipping...")
        else:
            print("No 'on:' block found. Skipping...")
    else:
        print(f"'permissions:' block already exists in {file_path}. Skipping...")

def check_permissions_exist(data):
    if isinstance(data, dict):
        if 'permissions' in data:
            return True
        for key, value in data.items():
            if check_permissions_exist(value):
                return True
    elif isinstance(data, list):
        for item in data:
            if check_permissions_exist(item):
                return True
    return False

def find_on_index(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'on':
                return key
            index = find_on_index(value)
            if index is not None:
                r
