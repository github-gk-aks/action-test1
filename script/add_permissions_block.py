import sys
from ruamel.yaml import YAML

def add_permissions_block(file_path):
    with open(file_path, 'r') as file:
        yaml = YAML()
        data = yaml.load(file)

    permissions_block = {
        'permissions': 'write-all'
    }

    # Check if 'on' block exists
    if 'on' in data:
        # Insert 'permissions' block after 'on' block
        index_on = list(data).index('on') + 1
        data.insert(index_on, 'permissions', 'write-all')

        # Insert a blank line after 'permissions' block
        index_permissions = list(data).index('permissions')
        data.insert(index_permissions + 1, 'blank_key:', '')

        with open(file_path, 'w') as file:
            yaml.dump(data, file)
        
        print(f"Added permissions block to {file_path}")
    else:
        print(f"'on:' block not found in {file_path}. Skipping...")

if __name__ == "__main__":
    file_path = sys.argv[1]
    add_permissions_block(file_path)
