# Rkale

![Kale](kale.jpg)

## Install
#### Install Rkale:  
```bash
pip install rkale
```
For easy usage, add rkale as an alias in your -bashrc
```bash
echo "alias rkale='python -m rkale.rkale'" >> ~/.bashrc
```


## Configuration

### Global

`~/.config/rkale/rkale.toml`:
```toml
[data]
root = "path to root data folder"

[aliases]
wasabi="value to match remote in rclone.conf"
```
root = root folder 
If alases are empty the remote name from the project config is used in the rclone lookup.

### Project
`~/<project path>/rkale_project.toml`:
```toml
  [[datasets]]
  name = "dataset_1"
  remote = "remote_1"
  
  [[datasets]]
  name = "dataset_2"
  remote = "remote_2"
  ```
The remote specified for the dataset must match a remote in the `rclone.conf` or an alias in the global rkale configuration.

## Usage
```
$ rkale -h
usage: rkale.py [-h] [-f] [-u]
                {copy,sync,pcopy,psync} [destinations [destinations ...]]

positional arguments:
  {copy,sync,pcopy,psync}
                        operation
  destinations          Soruce and destination, specified for sync/copy

optional arguments:
  -h, --help            show this help message and exit
  -f, --force           Run operation without checks
  -u, --upstream        reverse order for psync/pcopy
```
### Project example
```
$ rkale psync
```
Syncs the datasets specified in the `~/<project path>/rkale_project.toml` to be identical with their remotes
```
$ rkale psync --upstream
```
Syncs the remote datasets specified in the `~/<project path>/rkale_project.toml` to be identical with the local

### Global example
Same as rclone but first checks the result of the operation requires user consent before executing
