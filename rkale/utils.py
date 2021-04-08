import os
import re
import shutil
import subprocess
import tempfile
from contextlib import contextmanager

from tqdm import tqdm


def read(file_path):
    if os.path.exists(file_path):
        return open(file_path, "r").readlines()
    return []


@contextmanager
def check(source, destination):
    dirpath = tempfile.mkdtemp()
    src_out, dst_out, error_out = (
        f"{dirpath}/src_missing",
        f"{dirpath}/dst_missing",
        f"{dirpath}/error",
    )
    result = subprocess.run(
        f"rclone check {source} {destination}"
        + f" --missing-on-src {src_out}"
        + f" --missing-on-dst {dst_out} --error {error_out}",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    errors = read(error_out)
    if errors:
        raise Exception(
            "\n".join(
                [
                    f"Got {len(errors)} when comparing destinations",
                    "Caused by files:",
                    *errors,
                ]
            )
        )

    if not read(src_out) and not read(dst_out) and result.returncode == 1:
        raise Exception(result.stderr.decode("utf-8"))

    try:
        yield src_out, dst_out
    finally:
        shutil.rmtree(dirpath)


def check_paths(*args):
    for path in args:
        split_path = path.split(":")

        # path is local
        if len(split_path) == 1:
            if split_path[0].rstrip(".").rstrip("/") == os.path.expanduser("~"):
                raise Exception(f"Local {path} is a root path")
        else:
            if split_path[1].rstrip(".").rstrip("/") == "":
                raise Exception(f"Remote {path} is a root path")


def get_destinations(args):
    destinations = [arg for arg in args if not arg.startswith("-")]
    if len(destinations) != 2:
        raise Exception("Source and destination not specified")
    return destinations[0], destinations[1]


def sync(source, destination, files_from=None, progress=False):
    args = []
    if files_from is not None:
        args.append(f"--files-from {files_from}")
    if progress:
        args.append("--progress")

    comand = " ".join(["rclone", "sync", source, destination, *args])
    process = subprocess.Popen(comand, shell=True, stdout=subprocess.PIPE)

    if progress:
        pbar = tqdm(total=len(read(files_from)))

        while True:
            line = process.stdout.readline()
            if line:
                line = line.decode("utf-8")
                update = re.findall(
                    r"^Transferred.* ([0,1-9][0-9]*) / [0,1-9][0-9]*", line
                )
                if update:
                    pbar.update(int(update[0]) - pbar.n)
            else:
                pbar.close()
                break
