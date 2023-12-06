import ruamel.yaml
import sys

def add_permissions_block(file_path):
    yaml = ruamel.yaml.YAML()
    yaml.indent(offset=2)

    with open(file_path, 'r') as f:
        content = yaml.load(f)

    if 'on' in content and isinstance(content['on'], dict):
        content['permissions'] = 'write-all'

    yaml.explicit_start = True
    with open(file_path, 'w') as f:
        yaml.dump(content, f)

if __name__ == "__main__":
    file_path = sys.argv[1]
    add_permissions_block(file_path)
