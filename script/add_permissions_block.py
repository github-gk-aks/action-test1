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
            # Check if 'jobs:' block exists
            jobs_index = find_jobs_index(data, on_index)

            if jobs_index is not None:
                # Insert 'permissions' block after 'on:' and before 'jobs:' block
                data.insert(jobs_index, 'permissions', 'write-all')
                with open(file_path, 'w') as file:
                    yaml.dump(data, file)

                print(f"Added permissions block after 'on:' and before 'jobs:' block in {file_path}")
            else:
                print("No 'jobs:' block found after 'on:'. Skipping...")
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

def find_jobs_index(data, on_index):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'jobs':
                return on_index + 1
            elif isinstance(value, (list, dict)):
                index = find_jobs_index(value, on_index)
                if index is not None:
                    return index
    return None

if __name__ == "__main__":
    file_path = sys.argv[1]
    add_permissions_block(file_path)
