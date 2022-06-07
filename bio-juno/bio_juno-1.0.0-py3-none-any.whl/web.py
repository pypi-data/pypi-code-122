#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 29 19:58:46 2022

@author: hunglin
"""
import sys
import time
import tarfile
import tempfile
from pathlib import Path
from collections import OrderedDict

sys.path.insert(0, str(Path(__file__).parent.parent))
import streamlit as st
from random import sample
from st_aggrid import GridOptionsBuilder, AgGrid
from st_aggrid.shared import GridUpdateMode

from juno.data import Assembly, SRA
from juno.simulator import Simulator


@st.cache
def get_assembly_summary():
    assembly = Assembly()
    return assembly


@st.cache
def get_sra_metadata(organism, platform):
    df = SRA.search(organism=organism, platform=platform)
    return df


class APP:
    def __init__(self):
        self.pages = OrderedDict()

    def home(self):
        st.title("Juno: reads data generator")
        st.write(
            """
Juno have two methods to generate reads fastq.  
1. Download the real fastq submitted to NCBI SRA from the contributors
2. Simulate the "fake" fastq   

If you want to develope genomic tools but has no real data, juno can generate the read fastq for your testing.
            """
        )
        st.subheader("Feedback")
        st.write(
            "If you have any questions or idea for Juno, welcome to comment in the follwing.\ne.g. add options for metagenomic data"
        )
        with st.form("feedback"):
            person = st.text_input("Your mail address (Optional)", max_chars=100)
            comment = st.text_area("Comment (Required)", max_chars=5000)

            submitted = st.form_submit_button("Submit")
            if submitted:
                if comment:
                    feedback_path = Path(__file__).parent / "data/feedback.txt"
                    person = person if person else "anonymous"
                    with open(f"{feedback_path}", "a") as f:
                        f.write(
                            f"""{person}:
{time.asctime()}
{comment}
==============================
"""
                        )
                    st.success("Submitted to Juno's author")
                else:
                    st.error("The comment is required")
        st.subheader("Contact")
        st.write(
            "If you have any questions, welcome to contact us: hunglin59638@gmail.com "
        )

    def read_simulator(self):
        st.title("Reads simulator")
        st.subheader("NCBI RefSeq Assembly Summary")
        assembly = get_assembly_summary()
        df = assembly.dataframe

        if not st.session_state.get("init_organism"):
            st.session_state["init_organism"] = sample(set(df["organism_name"]), 1)[0]

        org = st.sidebar.text_input(
            label="Organism", value=st.session_state["init_organism"]
        )

        depth = st.sidebar.number_input(
            label="Expected depth", min_value=10, max_value=1000, value=200, step=100
        )
        platform = st.sidebar.selectbox(
            label="Sequencing platform", options=["Nanopore", "Pacbio"]
        )

        filter_df = assembly.search(org).head(100)
        gb = GridOptionsBuilder.from_dataframe(filter_df)
        gb.configure_pagination()
        gb.configure_side_bar()
        gb.configure_selection(
            selection_mode="single", use_checkbox=True, pre_selected_rows=(0,)
        )
        gb.configure_default_column(
            groupable=True,
            value=True,
            enableRowGroup=True,
            aggFunc="sum",
            editable=False,
        )
        gridOptions = gb.build()
        select_row = AgGrid(
            filter_df,
            gridOptions=gridOptions,
            enable_enterprise_modules=True,
            theme="dark",
            allow_unsafe_jscode=True,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
        )
        if select_row["selected_rows"]:
            st.write("Selected genome assembly: ")
            st.json(select_row["selected_rows"][0])
            accession = select_row["selected_rows"][0]["assembly_accession"]
            if st.button("Run"):
                sm = Simulator()
                with tempfile.TemporaryDirectory() as tmp_dir:
                    with st.spinner("Waiting for simulating reads"):
                        reference = assembly.download(accession, str(tmp_dir))

                        file = sm.generate(
                            reference, str(tmp_dir), platform=platform, depth=depth
                        )

                    with open(file, "rb") as f:
                        st.download_button(
                            "Download reads fastq",
                            f,
                            file_name=f"{accession}_reads.fastq.gz",
                        )

    def sra(self):
        st.title("Downloading reads from SRA database")
        st.subheader("SRA Accessions Summary")
        org = st.sidebar.text_input(label="Organism", value="Bacillus subtilis")
        platform = st.sidebar.selectbox(
            label="Platform", options=["Oxford Nanopore", "Pacbio SMRT", "Illumina"]
        )
        df = get_sra_metadata(org, platform)
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination()
        gb.configure_side_bar()
        if df.shape[0]:
            gb.configure_selection(
                selection_mode="single", use_checkbox=True, pre_selected_rows=(0,)
            )
        gb.configure_default_column(
            groupable=True,
            value=True,
            enableRowGroup=True,
            aggFunc="sum",
            editable=False,
        )
        gridOptions = gb.build()
        select_row = AgGrid(
            df,
            gridOptions=gridOptions,
            enable_enterprise_modules=True,
            theme="dark",
            allow_unsafe_jscode=True,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
        )
        if select_row["selected_rows"]:
            st.write("Selected SRA project: ")
            st.json(select_row["selected_rows"][0])
            if st.button("Run"):
                run_accession = select_row["selected_rows"][0]["run_1_accession"]
                with tempfile.TemporaryDirectory() as tmp_dir:
                    sra = SRA()
                    with st.spinner("Waiting for dowloaing reads from SRA"):
                        sra_dir = sra.download(
                            run_accession=run_accession,
                            out_dir=Path(tmp_dir) / run_accession,
                        )
                        out_tarfile = Path(tmp_dir) / f"{run_accession}.tar.gz"
                        with tarfile.open(out_tarfile, "w:gz") as tf:
                            tf.add(sra_dir)

                    with open(out_tarfile, "rb") as f:
                        st.download_button(
                            "Download SRA reads", f, file_name=out_tarfile.name
                        )

    def add_page(self, title, func):

        self.pages[title] = func

    def run(self):
        self.add_page(title="Home", func=self.home)
        self.add_page(title="Read Simulator", func=self.read_simulator)
        self.add_page(title="SRA", func=self.sra)
        # Drodown to select the page to run
        selection = st.sidebar.selectbox(
            "App Navigation",
            list(self.pages.keys()),
        )
        # run the app function
        self.pages[selection]()


if __name__ == "__main__":
    app = APP()
    app.run()
