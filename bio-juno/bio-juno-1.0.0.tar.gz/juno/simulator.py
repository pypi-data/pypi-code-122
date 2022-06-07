#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 13:52:28 2022

@author: hunglin
"""
import re
import gzip
import shutil
import tempfile
import subprocess
from pathlib import Path
from juno.config import TOOL_DIR, DATA_DIR


class Simulator:

    pbsim = TOOL_DIR / "pbsim"

    def generate(
        self, reference, out_dir, depth=200.0, platform="nanopore", compressed=True
    ):
        out_dir = Path(out_dir)
        with tempfile.TemporaryDirectory() as tmp_dir:
            prefix = Path(tmp_dir) / f"{Path(tmp_dir).name}"
            cmd = [
                self.pbsim,
                "--prefix",
                prefix,
                "--id-prefix",
                "read",
                "--depth",
                str(depth),
            ]
            if platform.lower() == "pacbio":
                difference_ratio = "6:50:54"
                model = "P6C4"
            elif platform.lower() == "nanopore":
                difference_ratio = "23:31:46"
                model = "R94"
            cmd.extend(
                [
                    "--difference-ratio",
                    difference_ratio,
                    "--hmm_model",
                    DATA_DIR / f"{model}.model",
                ]
            )

            if self.is_gz_file(reference):
                tmp_ref = Path(tmp_dir) / Path(reference).name.rstrip(".fna.gz")
                with gzip.open(reference, "rb") as f_in, open(tmp_ref, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
                reference = tmp_ref
            cmd.append(reference)
            p = subprocess.run(cmd)
            if p.returncode:
                return

            output_name = Path(reference).name.rstrip(".tar.gz")
            output_file = out_dir / (
                f"{output_name}.fastq.gz" if compressed else f"{output_name}.fastq"
            )
            fastq_files = [
                file
                for file in prefix.parent.iterdir()
                if re.match(f"{prefix.name}_[0-9]+\.fastq", file.name)
            ]
            return self.merge_to_one(
                fastq_files=fastq_files, output_file=output_file, compressed=compressed
            )

    @staticmethod
    def merge_to_one(fastq_files, output_file, compressed=True):
        handle = gzip.open(output_file, "wb") if compressed else open(output_file, "w")
        with handle as f_out:
            for file in fastq_files:
                with open(file, "rb" if compressed else "rt") as f_in:
                    shutil.copyfileobj(f_in, f_out)
        return output_file

    @staticmethod
    def is_gz_file(file):
        with open(file, "rb") as f:
            return f.read(2) == b"\x1f\x8b"
