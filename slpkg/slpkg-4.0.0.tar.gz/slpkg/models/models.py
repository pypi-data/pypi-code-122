#!/usr/bin/python3
# -*- coding: utf-8 -*-

# models.py file is part of slpkg.

# Copyright 2014-2022 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# Slpkg is a user-friendly package manager for Slackware installations

# https://gitlab.com/dslackw/slpkg

# Slpkg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import sqlite3
from progress.bar import Bar
from slpkg.__metadata__ import MetaData as _meta_


class Database:

    def __init__(self, table_name, text_file):
        self.lib_path = _meta_.lib_path
        self.table_name = table_name
        self.text_file = text_file
        self.db = _meta_.db
        self.con = sqlite3.connect(f"{self.lib_path}{self.db}")
        self.cur = self.con.cursor()

    def table_exists(self):
        """Checking if the table exists
        """
        self.cur.execute("""SELECT count(name)
                            FROM sqlite_master
                            WHERE type='table'
                            AND name='{}'""".format(self.table_name))
        return self.cur.fetchone()[0]

    def create_sbo_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS {}
                         (name text, location text, files text, version text,
                          download text, download64 text, md5sum text,
                          md5sum64 text, requires text, short_desc text)
                         """.format(self.table_name))
        self.con.commit()

    def insert_sbo_table(self):
        """Grabbing data line by line and inserting them into the database
        """
        self.sbo = [
            "SLACKBUILD NAME:",
            "SLACKBUILD LOCATION:",
            "SLACKBUILD FILES:",
            "SLACKBUILD VERSION:",
            "SLACKBUILD DOWNLOAD:",
            "SLACKBUILD DOWNLOAD_x86_64:",
            "SLACKBUILD MD5SUM:",
            "SLACKBUILD MD5SUM_x86_64:",
            "SLACKBUILD REQUIRES:",
            "SLACKBUILD SHORT DESCRIPTION:"
        ]

        sbo_file = self.open_file(f"{self.lib_path}sbo_repo/SLACKBUILDS.TXT")

        bar = Bar("Creating sbo database", max=len(sbo_file),
                  suffix="%(percent)d%% - %(eta)ds")

        cache = []  # init cache

        for i, line in enumerate(sbo_file, 1):

            for s in self.sbo:
                if line.startswith(s):
                    line = line.replace(s, "").strip()
                    cache.append(line)

            if (i % 11) == 0:
                values = [
                    (cache[0], cache[1], cache[2], cache[3], cache[4],
                     cache[5], cache[6], cache[7], cache[8], cache[9]),
                ]
                self.cur.executemany("""INSERT INTO {} VALUES
                                    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""".format(
                                        self.table_name), values)
                self.con.commit()
                cache = []  # reset cache after 11 lines
            bar.next()
        bar.finish()
        self.con.close()

    def open_file(self, file):
        with open(file, "r", encoding="utf-8") as f:
            return f.readlines()
