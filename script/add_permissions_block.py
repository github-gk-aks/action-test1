import sys
from ruamel.yaml import YAML

def add_permissions_block(file_path):
    with open(file_path, 'r') as file:
        yaml = YAML()
        data = yaml.load(file)
    
    if 'permissions' not in data:
        data.insert(data.keys().index('on') + 1, 'permissions', 'write-all')

        with open(file_path, 'w') as file:
            yaml.dump(data, file)

        print(f"Added permissions block to {file_path}")
    else:
        print(f"Permissions block already exists in {file_path}. Skipping...")

if __name__ == "__main__":
    file_path = sys.argv[1]
    add_permissions_block(file_path)
