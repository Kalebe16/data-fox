from pathlib import Path
from typing import Iterable


def filter_paths(
    paths: Iterable[Path],
    show_hidden_dirs: bool = False,
    show_hidden_files: bool = False,
) -> list[Path]:
    filtered_paths = []
    for path in paths:
        if path.is_dir():
            if not show_hidden_dirs and str(path.name).startswith('.'):
                continue
            filtered_paths.append(path)
        elif path.is_file():
            if not show_hidden_files and str(path.name).startswith('.'):
                continue
            filtered_paths.append(path)
    return filtered_paths
