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
        on_index = find_on_index(data)
        # Insert 'permissions' block at the top level
        #data.insert(0, 'permissions', 'write-all')
        if on_index is not None:
            data.insert(on_index + 1, 'permissions', 'write-all')

        with open(file_path, 'w') as file:
            yaml.dump(data, file)
        
        print(f"Added permissions block to {file_path}")
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
