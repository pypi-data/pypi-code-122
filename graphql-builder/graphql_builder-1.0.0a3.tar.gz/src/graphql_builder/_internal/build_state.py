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

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .builders import GraphQLOperationBuilder

__all__ = ("GraphQLBuildState",)


class GraphQLBuildState:
    def __init__(self, operation_builder: GraphQLOperationBuilder) -> None:
        self.current_cost = 0
        self.operation_builder = operation_builder
        self.last_unique_id = 0

    def get_unique_id(self) -> str:
        self.last_unique_id += 1
        return f"_{self.last_unique_id}"

    def should_end_call(self, cost: int) -> bool:
        self.current_cost += cost
        if self.operation_builder.MAX_COST is None:
            return False
        if self.current_cost > self.operation_builder.MAX_COST:
            self.current_cost = cost
            return True
        return False
