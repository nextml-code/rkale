from rkale.utils import check_files, check_paths, read, sync


def get_input(verbose_info):
    answer = input(
        "Are you sure you want to continue? [ls/y/N] (ls to expand changes) "
    )
    if answer == "ls":
        print(verbose_info)
        answer = input("Are you sure you want to continue? [y/N] ")
    return answer in ["y", "yes"]


def get_answers(operation, checks, paths, force=False):
    answers = []
    for check, (source, destination) in zip(checks, paths):
        missing_src, missing_dst = read(check.src_out), read(check.dst_out)
        if check.stderr:
            print(check.stderr)
            answers.append(False)
        elif force:
            answers.append(True)
        else:
            verbose_info = []
            print(f"\nChanges to be applied to {destination}:")
            if missing_dst:
                print(f"{len(missing_dst)} new files will be added")
                verbose_info.extend(["Files to be added:\n", *missing_dst])
            if operation == "sync" and missing_src:
                print(f"WARNING! {len(missing_src)} files will be removed")
                verbose_info.extend(["Files to be removed:\n", *missing_src])

            if (operation == "sync" and missing_src) or missing_dst:
                answers.append(get_input("".join(verbose_info)))
            else:
                print(f"Source and destination match, no files to {operation}")
                answers.append(False)
    return answers


def handle_copy(paths, force=False):
    check_paths(paths)
    with check_files(paths) as checks:
        answers = get_answers("copy", checks, paths, force=force)
        for answer, check, (source, destination) in zip(answers, checks, paths):
            if answer:
                print(f"Copying files to {destination}...")
                sync(source, destination, files_from=check.dst_out, progress=True)


def handle_sync(paths, force=False):
    check_paths(paths)
    with check_files(paths) as checks:
        answers = get_answers("sync", checks, paths, force=force)
        for answer, check, (source, destination) in zip(answers, checks, paths):
            if answer:
                if read(check.src_out):
                    print(f"Removing files from {destination}...")
                    sync(source, destination, files_from=check.src_out, progress=False)
                if read(check.dst_out):
                    print(f"Copying files to {destination}...")
                    sync(source, destination, files_from=check.dst_out, progress=True)
