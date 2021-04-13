# Rkale

## Install
#### Install Rkale:  
```bash
pip install rkale
```

## Configuration

### Global

`~/.config/rkale/rkale.conf`:
```toml
[data]
root = "path to root data folder"

[aliases]
wasabi="value to match remote in rclone.conf"
```
root = root folder.  
If alases are empty the remote name from the project config is used in the rclone lookup.

### Project
Add the rkale tool definition in the pyproject.toml file:  

`<project path>/pyproject.toml`:
```toml
  [[tool.rkale.dataset]]
  name = "dataset_1"
  remote = "remote_1"
  
  [[tool.rkale.dataset]]
  name = "dataset_2"
  remote = "remote_2"
  ```
The remote specified for the dataset must match a remote in the `rclone.conf` or an alias in the global rkale configuration.

### Project example
```
$ rkale psync
```
Syncs the datasets specified in the `<project path>/pyproject.toml` to be identical with their remotes.  
```
$ rkale psync --upstream
```
Syncs the remote datasets specified in the `<project path>/pyproject.toml` to be identical with their locals.  

### Global example
```rkale sync <source> <destination>```
Same as rclone but first checks the result of the operation requires user consent before executing.  
