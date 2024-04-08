import os

import yaml

from ok.util.path import ensure_dir_for_file


def read_yaml_file(file_path) -> dict | None:
    if not os.path.exists(file_path):
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data
    except yaml.YAMLError:
        return None


async def write_yaml_file(file_path, data):
    try:
        ensure_dir_for_file(file_path)
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data, f, default_flow_style=False, allow_unicode=True)
        return True
    except Exception as e:
        print(f"Error writing to YAML file: {e}")
        return False
