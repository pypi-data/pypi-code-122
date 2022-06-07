#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 15:36:59 2022

@author: hunglin
"""
import os
import logging
import argparse
from pathlib import Path

from . import __version__
from juno import web
from juno.simulator import Simulator
from juno.data import SRA, Assembly


def get_argument():
    def check_file(path):
        if not path:
            raise TypeError("Please input path")
        else:
            path = Path(path)
            if not path.exists():
                raise argparse.ArgumentTypeError("No such as a file or directory")
            else:
                return path
        raise TypeError("Please input path")

    def parse_dir(path):
        if not path:
            raise TypeError("Please input path")

        path = Path(path)
        if path.exists():
            raise FileExistsError("The directory path is exist")
        else:
            path.mkdir()
        return path

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Juno: read data generator",
    )
    parser.add_argument(
        "--version", "-v", action="version", version=f"%(prog)s {__version__}"
    )

    subcmd = parser.add_subparsers(
        dest="subcmd", description="subcommands", metavar="SUBCOMMAND"
    )

    sra = subcmd.add_parser("sra", help="Download reads from SRA database")
    sra.add_argument("--accession", "-a", help="SRA run accession, e.g. SRR19400588")
    sra.add_argument(
        "--out_dir", "-o", help="Output directory", type=parse_dir, required=True
    )

    simulator = subcmd.add_parser("simulate", help="Simulate reads by reference genome")
    sm_input = simulator.add_mutually_exclusive_group()
    sm_input.add_argument(
        "--accession", "-a", help="RefSeq assembly accession, e.g. GCF_002004995.1"
    )
    sm_input.add_argument(
        "--reference", "-r", help="Reference genome by fasta format", type=check_file
    )
    simulator.add_argument("--out_dir", "-o", help="Output directory", type=parse_dir)
    simulator.add_argument(
        "--depth",
        "-d",
        help="depth of coverage (default: %(default)s)",
        default=20.0,
        type=float,
    )
    simulator.add_argument(
        "--platform",
        "-p",
        help="Sequencing platform (default: %(default)s)",
        choices=["nanopore", "pacbio"],
        default="nanopore",
    )
    simulator.add_argument(
        "--compressed", "-c", help="using gzip to compress", action="store_true"
    )
    simulator.add_argument(
        "--update",
        "-u",
        help="Update local RefSeq assembly summary",
        action="store_true",
    )
    args = parser.parse_args()

    return args


def main():
    logging.getLogger().handlers.clear()
    logger = logging.getLogger(name="juno")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        fmt="[%(asctime)s] %(name)s: %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    args = get_argument()
    if args.subcmd == "sra":
        logger.info(f"Downloading read fastq of {args.accession}")
        sra = SRA()
        reads = sra.download(run_accession=args.accession, out_dir=args.out_dir)
        logger.info(f"Downloading reads to {reads}")

    elif args.subcmd == "simulate":
        assembly = Assembly()
        if args.update:
            logger.info("Updating local RefSeq assembly summary")
            assembly.update_assembly()
            logger.info("Finished")
            exit(0)
        if args.accession:
            reference = assembly.download(args.accession, args.out_dir)
        else:
            reference = args.reference
        sm = Simulator()
        reads = sm.generate(
            reference,
            out_dir=args.out_dir,
            depth=args.depth,
            platform=args.platform,
            compressed=args.compressed,
        )
        logger.info(f"Saving reads to {reads}")
    else:
        if args._get_kwargs()[0][1] is None:
            os.system(
                f"streamlit run --browser.serverAddress 0.0.0.0 --theme.base dark --server.maxMessageSize 2048 {web.__file__}"
            )


if __name__ == "__main__":
    main()
