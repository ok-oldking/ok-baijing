from pathlib import Path


def get_path(source_file, file):
    this_file = Path(source_file)
    root = this_file.parent.absolute()
    return Path.joinpath(root, file)
