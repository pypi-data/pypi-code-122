import concurrent.futures
import json
from pathlib import Path

import click

import sync_back
from sync_back.utils import (
    assign_slice_to_disk,
    rsync_data,
    walk,
    compute_files_size,
    compute_disk_size,
    group_folders_together,
    assign_slice_to_disk,
    move_data_around,
    StorageDisk,
)
from sync_back.progress_bar import job_progress

@click.group(invoke_without_command=True)
@click.option("--debug/--no-debug", default=False)
@click.option("--version", is_flag=True, default=False)
@click.pass_context
def cli(ctx, debug, version):
    """
    Do something with the debug flag... eventually
    """
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug
    
    job_progress.console.log(f"bsync {sync_back.__version__} All rights reserved.")
    job_progress.console.log(f"This software comes WITHOUT any warrenties. Use at your own risk.")


@cli.command()
@click.pass_context
def list(ctx):
    if ctx.obj["DEBUG"]:
        job_progress.console.log("Debugging...")
    job_progress.console.log("List files in a bsync backup")


@cli.command()
@click.pass_context
@click.option(
    "-s",
    "--slice",
    type=int,
    # Grow folder groups to a minimum of 1GB before storage
    # default=1_000_000_000,
    default=1_000_000,
    help=(
        "Smallest size a folder group can take on it's own (as long as there "
        "are enough files of sufficient size to accomidate it."
    ),
)
@click.argument("src", nargs=1)
@click.argument("dst", nargs=-1)
def backup(ctx, slice, src, dst):
    """
    Take a single source directory and copy it to n places.
    """
    # TODO: Do something with debugging at some point... maybe?
    if ctx.obj["DEBUG"]:
        # job_progress.console.log(f"Split into: {slice} containers.")
        job_progress.console.log(f"Source is: {src}")
        job_progress.console.log(f"{Path(src).absolute()}")
        # job_progress.console.log(f"Dest.  is: {dst}")

    src = Path(src).absolute()  # Convert user-input source to absolute path
    all_files = [x for x in walk(directory=str(src))]  # [FileObject(...), ...]
    disk_sizes = [compute_disk_size(x) for x in dst]  # [62767923200, ...]

    assert sum(disk_sizes) > compute_files_size(all_files=all_files) * 1.2, (
        "You are trying to store more" "data than there is available space."
    )

    job_progress.console.log("Grouping folders together")

    sorted_disks = assign_slice_to_disk(
        all_slices=group_folders_together(all_files=all_files, slice=slice),
        all_disks=[
            StorageDisk(path=path, capacity=size, restore_path=src)
            for path, size in zip([Path(p).absolute() for p in dst], disk_sizes)
        ],
    )

    ############################################################################
    # Fancy UI stuff
    ############################################################################

    jobs = {}
    for idx, disk in enumerate(sorted_disks):
        disk.get_used()
        jobs[idx] = job_progress.add_task(
            description=f"{disk.path}",
            total=len(disk.slices),
        )

    with job_progress:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:

            {
                pool.submit(move_data_around, disk, src, idx): idx
                for idx, disk in enumerate(sorted_disks)
            }

    job_progress.console.log("Backing up files to disks")


@cli.command()
@click.pass_context
@click.argument("src", nargs=-1)
def restore(ctx, src):
    job_progress.console.log("Restoring files from backup :thumbs_up:")

    for folder in src:
        source_folder = Path(folder).absolute()
        with open(source_folder / ".bsync") as f:
            data = json.load(f)
        dest_folder = Path(data["restore_path"]).absolute()

        job_progress.console.log(f'Copy data from: {source_folder}')
        job_progress.console.log(f'Copy data to: {dest_folder}')

        rsync_data(source_path=source_folder, destination_path=dest_folder)

if __name__ == "__main__":
    cli()
