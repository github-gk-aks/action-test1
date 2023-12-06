import sys
from ruamel.yaml import YAML, comments
from ruamel.yaml.scalarstring import DoubleQuotedScalarString as dq

def add_permissions_block(file_path):
    yaml = YAML()
    yaml.indent(offset=2)  # Set the indentation offset

    with open(file_path, 'r') as file:
        data = yaml.load(file)

    permissions_block = comments.CommentedMap()
    permissions_block['permissions'] = dq('write-all')

    # Check if 'on' block exists
    if 'on' in data:
        # Insert 'permissions' block after 'on' block
        index_on = list(data).index('on') + 1
        data.insert(index_on, ('', permissions_block))
        data.insert(index_on + 1, comments.CommentedMap())
        data.insert(index_on + 2, comments.CommentedMap())

        with open(file_path, 'w') as file:
            yaml.dump(data, file)
        
        print(f"Added permissions block to {file_path}")
    else:
        print(f"'on:' block not found in {file_path}. Skipping...")

if __name__ == "__main__":
    file_path = sys.argv[1]
    add_permissions_block(file_path)
