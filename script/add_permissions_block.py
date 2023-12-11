import sys
from ruamel.yaml import YAML

def add_permissions_block(file_path):
    with open(file_path, 'r') as file:
        yaml = YAML()
        data = yaml.load(file)

    permissions_block = {
        'permissions': 'write-all'
    }

    # Check if 'on:' block exists
    if 'on' in data:
        # Check if 'on:' is followed by a dictionary
        if isinstance(data['on'], dict):
            # Insert 'permissions' block after 'on:' block
            data['on'].insert(data['on'].ca.items[0][1], 'permissions', 'write-all')
        else:
            # Create a new dictionary for 'on:' block with 'permissions' block
            new_on_block = {'permissions': 'write-all', 'trigger': data['on']}
            data['on'] = new_on_block

        with open(file_path, 'w') as file:
            yaml.dump(data, file)

        print(f"Added permissions block after 'on:' in {file_path}")
    else:
        print("No 'on:' block found. Skipping...")

if __name__ == "__main__":
    file_path = sys.argv[1]
    add_permissions_block(file_path)
