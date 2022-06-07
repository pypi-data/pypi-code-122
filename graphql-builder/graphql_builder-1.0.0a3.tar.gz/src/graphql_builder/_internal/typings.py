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

from typing import Any, Dict, Iterator, Optional, Protocol, TypeVar

from .build_state import GraphQLBuildState
from .template import GraphQLChainMap

__all__ = ("FieldBuilderT", "NestableFieldBuilderT")


class GraphQLFieldBuilderProtocol(Protocol):
    def __init__(self) -> None:
        ...

    def _append(self, substitutions: Dict[str, Any]) -> None:
        ...

    def iter_calls(
        self, build_state: GraphQLBuildState, parent_substitutions: GraphQLChainMap
    ) -> Iterator[Optional[str]]:
        ...


class GraphQLNestableFieldBuilderProtocol(Protocol):
    def __init__(self, substitutions: Dict[str, Any]) -> None:
        ...

    def iter_calls(
        self, build_state: GraphQLBuildState, parent_substitutions: GraphQLChainMap
    ) -> Iterator[Optional[str]]:
        ...


FieldBuilderT = TypeVar("FieldBuilderT", bound=GraphQLFieldBuilderProtocol)
NestableFieldBuilderT = TypeVar(
    "NestableFieldBuilderT", bound=GraphQLNestableFieldBuilderProtocol
)
