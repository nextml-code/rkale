import os
from functools import lru_cache
from pathlib import Path

import toml


def get_repository_paths(working_dir):
    data_root = global_configuration()["data"]["root"]
    datasets = project_configuration(working_dir)["datasets"]
    return {dataset["name"]: Path(data_root) / dataset["name"] for dataset in datasets}


@lru_cache()
def global_configuration():
    return load_configuration(Path.home() / ".config/rkale/rkale.conf")


@lru_cache()
def project_configuration(working_dir):
    return load_configuration(find("rkale_project.toml", working_dir))


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
        raise Exception("Could not find file {name} in path {path}")


def load_configuration(path):
    with open(path) as f:
        value = toml.load(f)
        return value
