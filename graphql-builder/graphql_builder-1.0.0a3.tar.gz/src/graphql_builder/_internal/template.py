# Copyright 2021 Jakub Kuczys (https://github.com/jack1142)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
import string
from typing import Any, ChainMap

import simplejson

__all__ = ("GraphQLEnum", "GraphQLChainMap", "GraphQLTemplate")


class GraphQLEnum:
    __slots__ = ("name",)

    def __init__(self, name: str) -> None:
        self.name = name


class GraphQLChainMap(ChainMap[str, Any]):
    LITERAL_ONLY_KEYS = ("nested_call", "unique_id")

    def __getitem__(self, key: str) -> Any:
        key, _, value_format = key.partition(":")
        value = super().__getitem__(key)
        if value_format:
            if key in self.LITERAL_ONLY_KEYS and value_format != "literal":
                raise ValueError(f"{key!r} can only use the 'literal' format.")
        else:
            value_format = "literal" if key in self.LITERAL_ONLY_KEYS else "gql"

        if value_format == "gql":
            return simplejson.dumps(
                value, default=_graphql_json_default, separators=(",", ":")
            )
        elif value_format == "literal":
            return value
        else:
            raise ValueError(
                f"{value_format!r} is not a valid format specifier.\n"
                "Valid options are: 'gql', 'literal'"
            )


class GraphQLTemplate(string.Template):
    idpattern = r".^"
    braceidpattern = r"[_a-z][_a-z0-9]*(?::[_a-z][_a-z0-9]*)?"
    flags = re.IGNORECASE | re.ASCII

    def check_string_placeholders(self) -> None:
        self.substitute(_UniverseDict())


def _graphql_json_default(self, o: Any) -> simplejson.RawJSON:
    if isinstance(o, GraphQLEnum):
        return simplejson.RawJSON(o.name)
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")


class _UniverseDict(dict):
    def __missing__(self, key: str) -> str:
        return ""
