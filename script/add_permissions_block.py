import sys
from ruamel.yaml import YAML

def add_permissions_block(file_path):
    with open(file_path, 'r') as file:
        yaml = YAML()
        data = yaml.load(file)

    permissions_block = {
        'permissions': 'write-all'
    }

    # Check if 'permissions' block exists at any level
    if not check_permissions_exist(data):
        # Find the index of 'on:' block
        on_index = find_on_index(data)

        # Insert 'permissions' block after 'on:' block
        if on_index is not None:
            if isinstance(data[on_index][1], dict):  # Check if 'on:' is followed by a dictionary
                # Insert 'permissions' block under 'on:' block
                data[on_index][1].yaml_add_eol_comment("permissions: write-all", key='on', column=0)
                with open(file_path, 'w') as file:
                    yaml.dump(data, file)
                print(f"Added permissions block under 'on:' in {file_path}")
            else:
                # Create a new dictionary for 'on:' block with 'permissions' block
                new_on_block = {'permissions': 'write-all', 'trigger': data[on_index][1]}
                data[on_index][1] = new_on_block
                with open(file_path, 'w') as file:
                    yaml.dump(data, file)
                print(f"Modified 'on:' block by adding 'permissions' block in {file_path}")
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
        if 'on' in data:
            return data.yaml_add_eol_comment("permissions: write-all", key='on', column=0)
        for key, value in data.items():
            index = find_on_index(value)
            if index is not None:
                return index
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            index = find_on_index(item)
            if index is not None:
                return index
    return None



if __name__ == "__main__":
    file_path = sys.argv[1]
    add_permissions_block(file_path)
