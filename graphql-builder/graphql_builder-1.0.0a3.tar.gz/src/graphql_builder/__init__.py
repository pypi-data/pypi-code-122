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

"""Easy solution for dynamic generation of GraphQL operations."""

from ._internal.builders import (
    GraphQLFieldBuilder,
    GraphQLFieldBuilder as FieldBuilder,
    GraphQLNestableFieldBuilder,
    GraphQLNestableFieldBuilder as NestableFieldBuilder,
    GraphQLOperationBuilder,
    GraphQLOperationBuilder as OperationBuilder,
)
from ._internal.enums import GraphQLOperationType, GraphQLOperationType as OperationType
from ._internal.fields import (
    GraphQLField,
    GraphQLField as Field,
    GraphQLFieldBase,
    GraphQLFieldBase as FieldBase,
    GraphQLNestableField,
    GraphQLNestableField as NestableField,
)
from ._internal.template import (
    GraphQLEnum,
    GraphQLEnum as Enum,
    GraphQLTemplate,
    GraphQLTemplate as Template,
)

__version__ = "1.0.0a3"

__all__ = (
    # builders
    "GraphQLFieldBuilder",
    "FieldBuilder",
    "GraphQLNestableFieldBuilder",
    "NestableFieldBuilder",
    "GraphQLOperationBuilder",
    "OperationBuilder",
    # enums
    "GraphQLOperationType",
    "OperationType",
    # fields
    "GraphQLField",
    "Field",
    "GraphQLFieldBase",
    "FieldBase",
    "GraphQLNestableField",
    "NestableField",
    # template
    "GraphQLEnum",
    "Enum",
    "GraphQLTemplate",
    "Template",
)
