#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
TOOL_DIR = Path(__file__).parent / "tools"


def _post_install():
    print("Setting vdb-config")
    vdb_config = TOOL_DIR / "vdb-config"
    p = os.system(
        f"echo 'Aexyo' | {vdb_config} -i --interactive-mode textual > /dev/null 2>&1 "
    )
    if p:
        raise Exception("Fail to config sra toolkit")
    else:
        config_file = f"{os.environ['HOME']}/.ncbi/user-settings.mkfg"
        with open(config_file, "a") as f:
            f.write('/LIBS/GUID = "347babaa-7242-4323-a9c9-e56c8d6d74ec"\n')
