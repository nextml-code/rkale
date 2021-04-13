import os
from functools import lru_cache
from pathlib import Path

import toml
from rkale.exceptions import ConfigError, DataRootError, DatasetError


@lru_cache()
def global_configuration():
    return load_configuration(Path.home() / ".config/rkale/rkale.conf")


@lru_cache()
def project_configuration(working_dir):
    config_path = find("pyproject.toml", working_dir)
    config = load_configuration(config_path)
    if "tool" in config and "rkale" in config["tool"]:
        return config["tool"]["rkale"]
    raise ConfigError(f"No rkale section found in {config_path}")


def get_datasets(working_dir):
    config = project_configuration(working_dir)
    if "dataset" in config:
        return config["dataset"]
    raise DatasetError("No dataset defined in rkale config")


def get_repository_paths(working_dir):
    data_root = Path(global_configuration()["data"]["root"])
    return {
        dataset["name"]: get_path(data_root, dataset["name"])
        for dataset in get_datasets(working_dir)
    }


def get_path(root, name):
    resolved_path = Path(root.expanduser() / name).resolve()
    try:
        resolved_path.relative_to(root.expanduser().resolve())
        if resolved_path != root:
            return resolved_path
    except ValueError:
        pass
    raise DataRootError(f"Path {resolved_path} is outiside data root {root}")


def find(name, path):
    if os.path.exists(name) and os.path.isfile(name):
        return os.path.join(path, name)

    for root, dirs, files in os.walk(path, topdown=False):
        if name in files:
            return os.path.join(root, name)
    raise FileNotFoundError(f"Could not find file {name} in path {path}")


def load_configuration(path):
    with open(path) as f:
        value = toml.load(f)
        return value
