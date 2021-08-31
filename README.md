# rkale

## Install

Install rkale in your project using poetry:

```bash
poetry add rkale
```

Use pip if you want a global installation:

```bash
pip install rkale
```

## Configuration

### Global

`~/.config/rkale/rkale.conf`:
```toml
[data]
root = "path to data folder where datasets are stored"

[aliases]
wasabi = "optional alias for remote in rclone.conf"

[rclone] # global flags for rclone
flags = ["--transfers 32", "--checkers 32"]
```

If aliases are empty the remote name from the project config is used in the
rclone lookup.

### Project
Configure project datasets in the pyproject.toml file:

`<project path>/pyproject.toml`:
```toml
[[tool.rkale.dataset]]
name = "dataset_1"
remote = "remote_1"

[[tool.rkale.dataset]]
name = "dataset_2"
remote = "remote_2"
```

The remote specified for the dataset must match a remote in the `rclone.conf`
or an alias in the global rkale configuration.

## Usage

### Python interface

```python
from rkale.config import dataset_paths


def dataset_path():
    return dataset_paths()["dataset_1"]
```

### Syncing datasets

Syncs the local datasets to be identical to the remote

```bash
rkale psync
```

Syncs the remote datasets to be identical to the local

```bash
rkale psync --upstream
```

Same as rclone sync but checks differences first and asks for confirmation

```bash
rkale sync <source> <destination>
```
