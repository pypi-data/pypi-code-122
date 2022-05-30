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
from lazy_object_proxy import Proxy
from ...periodictable import ListElement


def _rules():
    from ...containers import QueryContainer
    rules = []

    # Oxo-acid salts. Me-[O,S,Se]-[P,S,Cl,Se,Br,I,Si]=O
    q = QueryContainer()
    q.add_atom(ListElement(['O', 'S', 'Se']), neighbors=2, hybridization=1)
    q.add_atom(ListElement(['C', 'N', 'P', 'S', 'Cl', 'Se', 'Br', 'I', 'Si']))
    q.add_atom('O')
    q.add_bond(1, 2, 1)
    q.add_bond(2, 3, 2)
    rules.append(q)

    # Thiophosphate salts.
    q = QueryContainer()
    q.add_atom(ListElement(['O', 'S', 'Se']), neighbors=2, hybridization=1)
    q.add_atom('P')
    q.add_atom(ListElement(['S', 'Se']))
    q.add_bond(1, 2, 1)
    q.add_bond(2, 3, 2)
    rules.append(q)

    # Phenole salts. Me-[O,S,Se]-Ar
    q = QueryContainer()
    q.add_atom(ListElement(['O', 'S', 'Se']), neighbors=2, hybridization=1)
    q.add_atom(ListElement(['C', 'N']), hybridization=4)
    q.add_bond(1, 2, 1)
    rules.append(q)

    # Nitrate. Me-O-[N+](=O)[O-]
    q = QueryContainer()
    q.add_atom('O', neighbors=2, hybridization=1)
    q.add_atom('N', charge=1)
    q.add_atom('O', charge=-1)
    q.add_atom('O')
    q.add_bond(1, 2, 1)
    q.add_bond(2, 3, 1)
    q.add_bond(2, 4, 2)
    rules.append(q)

    # halogenides and hydroxy
    q = QueryContainer()
    q.add_atom(ListElement(['O', 'F', 'Cl', 'Br', 'I']), neighbors=1, hybridization=1)
    rules.append(q)
    return rules


def _acids():
    from ... import smiles

    tmp = ['Cl', 'Br', 'I', 'O[N+](=O)[O-]', 'ON=O', 'OP(O)(O)=O', 'COP(O)(=O)OC',
           'OS(O)(=O)=O', 'CS(O)(=O)=O', 'OS(=O)(=O)C(F)(F)F', 'CC1=CC=C(C=C1)S(O)(=O)=O',
           'OC(O)=O', 'CC(O)=O', 'OC(=O)C(F)(F)F', 'OCC(O)=O', 'CC(O)C(O)=O', 'OC(=O)C(O)=O', 'OC(=O)C(Cl)Cl',
           'OC(=O)C=CC(O)=O', 'OC(C(O)C(O)=O)C(O)=O',
           'O[Cl](=O)(=O)=O']
    acs = set()
    for x in tmp:
        x = smiles(x)
        x.thiele()
        acs.add(x)
    return acs


acids = Proxy(_acids)
rules = Proxy(_rules)


__all__ = ['acids', 'rules']
