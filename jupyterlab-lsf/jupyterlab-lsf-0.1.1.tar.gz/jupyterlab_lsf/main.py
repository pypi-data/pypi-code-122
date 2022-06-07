"""Utility to run jupyter server through LSF."""
from os.path import join
import json
import os
import subprocess
import re
import shutil
import time

import click


@click.command()
@click.option(
    "--port",
    "-p",
    default=8888,
    help="Port number, unique by server user",
    show_default=True,
)
@click.option(
    "--walltime", "-w", default=240, help="LSF job wall time (minutes)", show_default=True
)
@click.option("--nodes", "-n", default=2, help="LSF job nodes", show_default=True)
@click.option(
    "--memory", "-m", default=32, help="LSF job per node memory (Gb)", show_default=True
)
@click.option(
    "--watch",
    default=4,
    help="Waiting seconds to watch for notebook job status",
    show_default=True,
)
@click.option(
    "--htslib-path",
    "-s",
    default="/work/isabl/ref/homo_sapiens/GRCh37d5/htslib/htslib-1.9",
    help="htslib path",
    show_default=True,
)
def submit_notebook_to_lsf(port, walltime, nodes, memory, watch, htslib_path):
    """Submits jupyter server in an lsf host and map its port."""
    if not shutil.which("jupyter"):
        raise Exception("`jupyter` command not found. Please install")
    user = os.getenv("USER", "papaemmelab-user")
    jupyter_dir = join(os.getenv("HOME"), ".jupyter")
    os.makedirs(jupyter_dir, exist_ok=True)
    jupyter_logs = join(jupyter_dir, "logs.txt")
    jupyter_cmd = join(jupyter_dir, "cmd.sh")

    # Create jupyter Server command
    with open(jupyter_cmd, "wt", encoding="utf-8") as f:
        f.write("#!/bin/bash\n\n")
        f.write(f"export LD_LIBRARY_PATH={htslib_path}:$LD_LIBRARY_PATH\n\n")
        f.write(f'jupyter lab --no-browser --port {port} --NotebookApp.token=""')

    # Submit to lsf
    lsf_cmd = [
        "bsub",
        "-W",
        str(walltime),
        "-n",
        str(nodes),
        "-M",
        str(memory),
        "-R",
        f'"rusage[mem={memory}]"',
        "-J",
        f'{user}-notebook"',
        "-o",
        jupyter_logs,
        "bash",
        jupyter_cmd,
    ]
    jobid = subprocess.check_output(lsf_cmd).decode("utf-8")
    jobid = re.findall("<(.*?)>", jobid)[0]
    click.echo(f"🚀 Submitted on job {jobid}")

    job_check_cmd = ["bjobs", "-json", jobid]
    job_status = "PEND"
    host = None
    while job_status == "PEND":
        click.echo(f"🔍 Checking job {jobid} status every {watch} seconds: {job_status}")
        time.sleep(watch)
        jobs_info = subprocess.check_output(job_check_cmd).decode("utf-8")
        job_info = [
            job for job in json.loads(jobs_info)["RECORDS"] if job["JOBID"] == jobid
        ]
        if job_info:
            job_status = job_info[0]["STAT"]
        else:
            job_status = "EXIT"

    if job_status == "RUN" and job_info:
        host = job_info[0]["EXEC_HOST"].split("*")[1]
    else:
        click.echo(f"Job {jobid} status: {job_status}")
        return

    # Try clearing port
    try:
        clear_port_cmd = ["lsof", f"-ti:{port}"]
        port_processed = subprocess.check_output(clear_port_cmd).decode("utf-8")
        if port_processed:
            kill_port_process_cmd = ["kill", "-9", port]
            subprocess.check_output(kill_port_process_cmd)
            click.echo(f"🧹 Clearing open port {port}...")
    except Exception: # pylint: disable=broad-except
        pass

    # Forward port from host
    map_port_cmd = ["ssh", "-Y", "-N", "-L", f"localhost:{port}:localhost:{port}", host]
    click.secho(f"💻 Browse to http://localhost:{port}", fg="magenta")
    click.secho(
        f"📙 Port {port} forwarded from host {host}... [Click cmd+c to kill]",
        fg="yellow",
    )
    subprocess.check_output(map_port_cmd).decode("utf-8")


if __name__ == "__main__":
    submit_notebook_to_lsf() # pylint: disable=no-value-for-parameter
