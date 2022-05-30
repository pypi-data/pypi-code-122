# -*- coding: utf-8 -*-
#
#  Copyright 2022 Ramil Nugmanov <nougmanoff@protonmail.com>
#  This file is part of chython.
#
#  chython is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, see <https://www.gnu.org/licenses/>.
#
from itertools import count
from re import compile, findall, search
from .parser import parser
from .tokenize import smarts_tokenize
from ...containers import QueryContainer
from ...periodictable import QueryElement


cx_radicals = compile(r'\^[1-7]:[0-9]+(?:,[0-9]+)*')
cx_hh = compile(r'atomProp(:[0-9]+\.(?:hyb|het)\.[0-9]+)+')
hybridization = {'4': 4, '3': 1, '2': 2, '1': 3}


def smarts(data: str):
    """
    Parse SMARTS string.

    * stereo ignored.
    * only D, a, h, r and !R atom primitives supported.
    * bond order list and not bond supported.
    * [not]ring bond supported only in combination with explicit bonds, not bonds and bonds orders lists.
    * mapping, charge and isotopes supported.
    * list of elements supported.
    * A - treats as any element. <A> primitive (aliphatic) ignored.
    * M - treats as any metal..
    * <&> logic operator unsupported.
    * <;> logic operator is mandatory except for charge, isotope, stereo marks. however preferable.
    * CXSMARTS radicals supported.
    * hybridization and heteroatoms count in CXSMARTS atomProp notation as <hyb> and <het> keys supported.

    For example::

        [C;r5,r6;a]-;!@[C;h1,h2] |^1:1,atomProp:1.hyb.24:1.het.0| - aromatic C member of 5 or 6 atoms ring
        connected with non-ring single bond to aromatic or SP2 radical C with 1 or 2 hydrogens.

    """
    smr, *cx = data.split()

    hyb = {}
    het = {}
    if cx and cx[0].startswith('|') and cx[0].endswith('|'):
        radicals = [int(x) for x in findall(cx_radicals, cx[0]) for x in x[3:].split(',')]

        if hh := search(cx_hh, cx[0]):
            for x in hh.group().split(':')[1:]:
                i, h, v = x.split('.')
                i = int(i)
                if h == 'hyb':
                    hyb[i] = [hybridization[x] for x in v]
                else:
                    het[i] = [int(y) for y in v]
    else:
        radicals = []

    data = parser(smarts_tokenize(smr), False)[0]

    for x in radicals:
        data['atoms'][x]['is_radical'] = True
    for i, v in hyb.items():
        data['atoms'][i]['hybridization'] = v
    for i, v in het.items():
        data['atoms'][i]['heteroatoms'] = v

    g = QueryContainer()

    mapping = {}
    free = count(max(a['mapping'] for a in data['atoms']) + 1)
    for i, a in enumerate(data['atoms']):
        mapping[i] = n = a.pop('mapping') or next(free)
        e = a.pop('element')
        if it := a.pop('isotope'):
            if isinstance(e, int):
                e = QueryElement.from_atomic_number(e)(it)
            else:
                e = QueryElement.from_symbol(e)(it)
        g.add_atom(e, n, **a)

    for n, m, b in data['bonds']:
        g.add_bond(mapping[n], mapping[m], b)
    return g


__all__ = ['smarts']
