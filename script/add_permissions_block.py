import sys
from ruamel.yaml import YAML

def add_permissions_block(file_path):
    with open(file_path, 'r') as file:
        yaml = YAML()
        data = yaml.load(file)

    permissions_block = {
        'permissions': 'write-all'
    }

    # Check if 'on' block and 'permissions' block exist
    if 'on' in data and 'permissions' not in data:
        # Insert 'permissions' block after 'on' block
        index = list(data).index('on') + 1
        data.yaml_set_comment_before_after_key('permissions', before='\n')
        data.insert(index, 'permissions', 'write-all')
        
        with open(file_path, 'w') as file:
            yaml.dump(data, file)
        
        print(f"Added permissions block to {file_path}")
    elif 'permissions' in data:
        print(f"'permissions:' block already exists in {file_path}. Skipping...")
    else:
        print(f"'on:' block not found in {file_path}. Skipping...")

if __name__ == "__main__":
    file_path = sys.argv[1]
    add_permissions_block(file_path)
