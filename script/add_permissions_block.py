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
        index = list(data).index('on') + 1
        data.insert(index, 'permissions', 'write-all')

        # Add a start comment to create a blank line before 'permissions' block
        comment = "\n"  # newline character
        data.yaml_set_start_comment(comment, 'permissions')

        with open(file_path, 'w') as file:
            yaml.dump(data, file)
        
        print(f"Added permissions block to {file_path}")
    else:
        print(f"'on:' block not found in {file_path}. Skipping...")

if __name__ == "__main__":
    file_path = sys.argv[1]
    add_permissions_block(file_path)
