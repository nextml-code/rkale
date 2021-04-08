from rkale.checked_operations import handle_copy, handle_sync
from rkale.config import global_configuration, project_configuration


def handle_pcopy(working_dir, force=False, upstream=False):
    return _apply_to_datasets(handle_copy, working_dir, force=force, upstream=upstream)


def handle_psync(working_dir, force=False, upstream=False):
    return _apply_to_datasets(handle_sync, working_dir, force=force, upstream=upstream)


def _apply_to_datasets(func, working_dir, force=False, upstream=False):
    global_config = global_configuration()
    project_config = project_configuration(working_dir)
    data_root = global_config["data"]["root"]

    for dataset in project_config["datasets"]:
        remote = dataset["remote"]
        if "aliases" in global_config and remote in global_config["aliases"]:
            remote = global_config["aliases"][remote]

        source, destination = get_destinations(
            data_root, remote, dataset["name"], upstream
        )
        func(source, destination, force=force)


def get_destinations(data_root, remote, dataset, upstream):
    dest1 = f"{data_root}/{dataset}"
    dest2 = f"{remote}:/{dataset}"
    return (dest1, dest2) if upstream else (dest2, dest1)
