import os
from ruamel.yaml import YAML
from glob import glob
from fnmatch import fnmatch

def add_permissions_block(file_path):
    with open(file_path, 'r') as f:
        content = YAML().load(f)

    # Check if 'on' block exists and if 'permissions' block is not present in jobs
    if 'on' in content and ('jobs' not in content or 'permissions' not in content['jobs']):
        # Insert a blank line after 'on' block
        content.insert(content.index['on'] + 1, ' ', ' ')
        # Add a blank line and insert 'permissions' block after 'on' block
        content['permissions'] = 'write-all'

        # Iterate over the items in content and insert 'permissions' after 'on'
        new_content = []
        for key, value in content.items():
            new_content.append((key, value))
            if key == 'on':
                new_content.append(('', ''))
                new_content.append(('permissions', 'write-all'))
                new_content.append(('', ''))

        with open(file_path, 'w') as f:
            YAML().dump(dict(new_content), f)

def process_workflow_files():
    # Get a list of all .yml files in the .github/workflows directory
    workflow_files = glob('.github/workflows/*.yml')

    # Patterns for files to be excluded
    exclude_patterns = ['token-permission.yml', 'add-license-file.yml']

    for file_path in workflow_files:
        # Extracting only the file name from the full path
        file_name = os.path.basename(file_path)
        
        # Check if the file should be excluded
        if any(fnmatch(file_name, pattern) for pattern in exclude_patterns):
            print(f"Skipping {file_path}")
            continue

        add_permissions_block(file_path)

if __name__ == "__main__":
    process_workflow_files()
