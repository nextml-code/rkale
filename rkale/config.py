import os
from functools import lru_cache
from pathlib import Path

import toml
from rkale.exceptions import ConfigError, DataRootError, DatasetError


@lru_cache()
def global_configuration():
    return load_configuration(Path.home() / ".config/rkale/rkale.conf")


@lru_cache()
def project_configuration(working_dir=None):
    if working_dir is None:
        working_dir = os.getcwd()
    config_path = find("pyproject.toml", Path(working_dir))
    config = load_configuration(config_path)
    if "tool" in config and "rkale" in config["tool"]:
        return config["tool"]["rkale"]
    raise ConfigError(f"No rkale section found in {config_path}")


def rclone_flags():
    config = global_configuration()
    if "rclone" in config and "flags" in config["rclone"]:
        return config["rclone"]["flags"]
    return []


def datasets(working_dir=None):
    if working_dir is None:
        working_dir = os.getcwd()
    config = project_configuration(working_dir=working_dir)
    if "dataset" in config:
        return config["dataset"]
    raise DatasetError("No dataset defined in rkale config")


def dataset_paths(working_dir=None):
    if working_dir is None:
        working_dir = os.getcwd()
    data_root = Path(global_configuration()["data"]["root"])
    return {
        dataset["name"]: path(data_root, dataset["name"])
        for dataset in datasets(working_dir=working_dir)
    }


def path(root, name):
    resolved_path = Path(root.expanduser() / name).resolve()
    try:
        resolved_path.relative_to(root.expanduser().resolve())
        if resolved_path != root:
            return resolved_path
    except ValueError:
        pass
    raise DataRootError(f"Path {resolved_path} is outside data root {root}")


def find(name, root):
    while root != Path("/"):
        if (root / name).exists():
            return root / name
        root = root.parent
    raise FileNotFoundError(f"Could not find file {name} in path {root} or any of it's parent directories")


def load_configuration(path):
    with open(path) as f:
        value = toml.load(f)
        return value
