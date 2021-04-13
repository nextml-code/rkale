import argparse
import os

from rkale.operations import handle_copy, handle_sync
from rkale.project_operations import handle_pcopy, handle_psync

OPERATIONS = {
    "copy": handle_copy,
    "sync": handle_sync,
    "pcopy": handle_pcopy,
    "psync": handle_psync,
}


def main():
    working_dir = os.getcwd()
    parser = argparse.ArgumentParser()

    base_parser = argparse.ArgumentParser(add_help=False)
    base_parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        dest="force",
        help="Run operation without checks",
    )

    subparsers = parser.add_subparsers(title="operation", dest="operation")
    global_parser = subparsers.add_parser(
        "copy", aliases=["sync"], parents=[base_parser]
    )
    global_parser.add_argument("source")
    global_parser.add_argument("destination")
    global_parser.set_defaults(
        func=lambda args: OPERATIONS[args.operation](
            [(args.source, args.destination)], force=args.force
        )
    )

    project_parser = subparsers.add_parser(
        "pcopy", aliases=["psync"], parents=[base_parser]
    )
    project_parser.add_argument(
        "-u",
        "--upstream",
        action="store_true",
        dest="upstream",
        help="Apply changes upstream",
    )
    project_parser.set_defaults(
        func=lambda args: OPERATIONS[args.operation](
            working_dir, force=args.force, upstream=args.upstream
        )
    )

    args = parser.parse_args()
    try:
        func = args.func
        func(args)
    except AttributeError:
        parser.error("too few arguments")
    except Exception as e:
        print(str(e).rstrip("\n"))


if __name__ == "__main__":
    main()
