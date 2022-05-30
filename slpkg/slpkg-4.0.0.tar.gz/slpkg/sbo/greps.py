#!/usr/bin/python3
# -*- coding: utf-8 -*-

# greps.py file is part of slpkg.

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
from slpkg.utils import Utils
from slpkg.__metadata__ import MetaData as _meta_


class SBoGrep(Utils):
    """Grabs data from sbo database
    """
    def __init__(self, name):
        self.name = name
        self.meta = _meta_
        self.db = self.meta.db
        self.arch64 = "x86_64"
        self.sbo_db = f"{self.meta.lib_path}{self.db}"
        self.con = sqlite3.connect(self.sbo_db)
        self.cur = self.con.cursor()

    def _names_grabbing(self):
        """Generator that collecting all packages names
        """
        names = self.cur.execute("SELECT name FROM sbo").fetchall()
        for n in names:
            yield n[0]

    def names(self):
        """Alias method convert generator and return
        a list
        """
        return list(self._names_grabbing())

    def source(self):
        """Grabs sources downloads links
        """
        source, source64 = self.cur.execute("""SELECT download, download64
                                               FROM sbo
                                               WHERE name = '{}'""".format(
                                                   self.name)).fetchone()
        return self._sorting_arch(source, source64)

    def requires(self):
        """Grabs package requirements
        """
        requires = self.cur.execute("""SELECT requires
                                       FROM sbo
                                       WHERE name = '{}'""".format(
                                           self.name)).fetchone()
        return requires[0].split()

    def version(self):
        """Grabs package version
        """
        version = self.cur.execute("""SELECT version
                                      FROM sbo
                                      WHERE name = '{}'""".format(
                                      self.name)).fetchone()
        return version[0]

    def checksum(self):
        """Grabs checksum string
        """
        md5sum, md5sum64, = [], []
        mds5, md5s64 = self.cur.execute("""SELECT md5sum, md5sum64
                                           FROM sbo
                                           WHERE name = '{}'""".format(
                                               self.name)).fetchone()
        if mds5:
            md5sum.append(mds5)
        if md5s64:
            md5sum64.append(md5s64)
        return self._sorting_arch(md5sum, md5sum64)

    def description(self):
        """Grabs package description
        """
        desc = self.cur.execute("""SELECT short_desc
                                   FROM sbo
                                   WHERE name = '{}'""".format(
                                       self.name)).fetchone()
        return desc[0]

    def files(self):
        """Grabs files
        """
        files = self.cur.execute("""SELECT files
                                    FROM sbo
                                    WHERE name = '{}'""".format(
                                        self.name)).fetchone()
        return files[0]

    def _sorting_arch(self, arch, arch64):
        """Returns sources by arch
        """
        if self.meta.arch == self.arch64 and arch64:
            return arch64
        return arch
