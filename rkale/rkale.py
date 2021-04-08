import argparse
import os

from rkale.checked_operations import handle_copy, handle_sync
from rkale.project_operations import handle_pcopy, handle_psync

CHECKED_OPERATIONS = ["copy", "sync"]
PROJECT_OPERATIONS = {"pcopy": handle_pcopy, "psync": handle_psync}


def rkale(working_dir, operation, destinations=[], force=False, upstream=False):
    if operation in CHECKED_OPERATIONS:
        if len(destinations) != 2:
            raise Exception("Source and destination not specified correctly")
        source, destination = destinations
        if operation == "sync":
            handle_sync(source, destination, force=force)
        else:
            handle_copy(source, destination, force=force)
    elif operation in PROJECT_OPERATIONS.keys():
        PROJECT_OPERATIONS[operation](working_dir, force=force, upstream=upstream)
    else:
        raise Exception("Unrecognized operation")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        choices=["copy", "sync", "pcopy", "psync"], help="operation", dest="operation"
    )
    parser.add_argument(
        nargs="*",
        default=[],
        dest="destinations",
        help="Soruce and destination, specified for sync/copy",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        dest="force",
        help="Run operation without checks",
    )
    parser.add_argument(
        "-u",
        "--upstream",
        action="store_true",
        dest="upstream",
        help="reverse order for psync/pcopy",
    )
    args = parser.parse_args()
    try:
        rkale(
            os.getcwd(),
            args.operation,
            destinations=args.destinations,
            force=args.force,
            upstream=args.upstream,
        )
    except Exception as e:
        print(str(e).rstrip("\n"))


if __name__ == "__main__":
    main()
