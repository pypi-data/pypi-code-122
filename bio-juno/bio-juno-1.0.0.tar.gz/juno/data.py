#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 29 10:07:25 2022

@author: hunglin
"""
import re
import requests
import pickle
import subprocess
import pandas as pd
from pathlib import Path
from pysradb.search import SraSearch
from requests.adapters import HTTPAdapter

from juno.config import DATA_DIR, TOOL_DIR, _post_install


class Assembly:

    refseq_url = "https://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/assembly_summary_refseq.txt"

    def __init__(self):
        self.dataframe = self.__get_dataframe()

    def get_assembly_summary(self):
        s = requests.Session()
        s.mount("https://", HTTPAdapter(max_retries=5))
        req = s.get(url=self.refseq_url, timeout=60)
        if req.ok:
            asm_sum = req.text
            rows = asm_sum.split("\n")
            cols = rows[1].strip("# ").split("\t")
            rows = [row.split("\t") for row in rows if not row.startswith("#") and row]

            return {
                "columns": dict([(i, col) for i, col in zip(range(len(cols)), cols)]),
                "rows": rows,
            }

    def __get_dataframe(self):
        df_f = DATA_DIR / "assembly_summary.pkl"
        if not df_f.is_file():
            asm_sum = self.get_assembly_summary()
            df = pd.DataFrame(data=asm_sum["rows"], columns=asm_sum["columns"].values())
            with open(df_f, "wb") as f:
                pickle.dump(df, f)
        else:
            with open(df_f, "rb") as f:
                df = pickle.load(f)
        return df.dropna()

    def search(self, organism):
        df = self.dataframe
        regex = re.compile(organism, re.IGNORECASE)
        filter_df = df[df["organism_name"].str.match(regex)]
        filter_df = filter_df.sort_values(by="refseq_category", axis=0, ascending=False)
        return filter_df

    def download(self, accession, out_dir):
        out_dir = Path(out_dir)
        out_dir.mkdir(exist_ok=True)
        selected_rows = self.dataframe[
            self.dataframe["assembly_accession"] == accession
        ]
        if selected_rows.shape[0]:
            ftp_path = selected_rows.iloc[0]["ftp_path"]
            filename = f"{ftp_path.split('/')[-1]}_genomic.fna.gz"
            full_url = f"{ftp_path}/{filename}"
            s = requests.Session()
            s.mount("https://", HTTPAdapter(max_retries=5))
            req = s.get(url=full_url, timeout=60)
            outfile = out_dir / filename
            with open(outfile, "wb") as f:
                for chunk in req.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
            return outfile

    def update_assembly(self):
        df_f = DATA_DIR / "assembly_summary.pkl"
        df_f.unlink(missing_ok=True)
        self.dataframe = self.__get_dataframe()


class SRA:
    def __init__(self):
        self.faster_dump = TOOL_DIR / "fasterq-dump"
        if subprocess.call([self.faster_dump, "-h"], stdout=subprocess.DEVNULL):
            _post_install()

    @staticmethod
    def search(organism, platform="oxford nanopore"):
        sradb = SraSearch(
            organism=organism, platform=platform, source="GENOMIC", verbosity=2
        )
        sradb.search()
        return sradb.df

    def download(self, run_accession, out_dir):
        cmd = [self.faster_dump, "-O", out_dir, run_accession]
        p = subprocess.run(cmd)
        if p.returncode:
            raise Exception(f"Failed to download {run_accession}")
            return
        else:
            return out_dir
