import sys
from ruamel.yaml import YAML

def add_permissions_block(file_path):
    yaml = YAML()
    with open(file_path, 'r') as file:
        data = yaml.load(file)

    # Check if 'on' block exists
    if 'on' in data:
        # Insert 'permissions' block after 'on' block
        data['permissions'] = 'write-all'

        # Insert a blank line after 'permissions' block
        data['blank_key'] = ''

        with open(file_path, 'w') as file:
            yaml.dump(data, file)
        
        print(f"Added permissions block to {file_path}")
    else:
        print(f"'on:' block not found in {file_path}. Skipping...")

if __name__ == "__main__":
    file_path = sys.argv[1]
    add_permissions_block(file_path)
