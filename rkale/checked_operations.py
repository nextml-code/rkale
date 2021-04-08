from rkale.utils import check, check_paths, read, sync


def handle_copy(source, destination, force=False):
    check_paths(source, destination)

    print(f"comparing destinations {source}, {destination}...")
    with check(source, destination) as (_, dst_out):
        missing_dst = read(dst_out)
        if missing_dst:
            if not force:
                print(f"{len(missing_dst)} new files will be added to {destination}")
                answer = input("Are you sure you want to continue? [y/N] ")
                if answer not in ["y", "yes"]:
                    return

            print(f"Copying files to {destination}...")
            sync(source, destination, files_from=dst_out, progress=True)
        else:
            print("Source and destination match, no files to copy")


def handle_sync(source, destination, force=False):
    check_paths(source, destination)

    print(f"comparing destinations {source}, {destination}...")
    with check(source, destination) as (src_out, dst_out):
        missing_src, missing_dst = read(src_out), read(dst_out)
        if not force and missing_src:
            print(
                f"WARNING! {len(missing_src)} files will be removed from {destination}"
            )

        if not force and missing_dst:
            print(f"{len(missing_dst)} new files will be added to {destination}")

        if missing_src or missing_dst:
            if not force:
                answer = input("Are you sure you want to continue? [y/N] ")
                if answer not in ["y", "yes"]:
                    return

            if missing_src:
                print(f"Removing files from {destination}...")
                sync(source, destination, files_from=src_out, progress=False)

            if missing_dst:
                print(f"Copying files to {destination}...")
                sync(source, destination, files_from=dst_out, progress=True)
        else:
            print("Source and destination match, no files to sync")
