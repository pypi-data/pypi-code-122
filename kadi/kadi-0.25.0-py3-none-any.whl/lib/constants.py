# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


ONE_KB = 1000  # Amount of bytes (decimal interpretation).
ONE_MB = 1000 * ONE_KB
ONE_GB = 1000 * ONE_MB
ONE_TB = 1000 * ONE_GB


ONE_KIB = 1024  # Amount of bytes (binary interpretation).
ONE_MIB = 1024 * ONE_KIB
ONE_GIB = 1024 * ONE_MIB
ONE_TIB = 1024 * ONE_GIB


ONE_MINUTE = 60  # Amount of seconds.
ONE_HOUR = 60 * ONE_MINUTE
ONE_DAY = 24 * ONE_HOUR
ONE_WEEK = 7 * ONE_DAY


# Preferred MIME type for CSV files.
MIMETYPE_CSV = "text/csv"
# Default MIME type for unspecified binary files.
MIMETYPE_DEFAULT = "application/octet-stream"
# Custom MIME type for flow files to define workflows.
MIMETYPE_FLOW = "application/x-flow+json"
# Preferred MIME type for JSON files.
MIMETYPE_JSON = "application/json"
# Custom MIME type for tool files to be used within workflows.
MIMETYPE_TOOL = "application/x-tool+xml"
# Preferred MIME type for XML files.
MIMETYPE_XML = "application/xml"


# URL from which the latest released Kadi version is retrieved.
URL_PYPI = "https://pypi.org/pypi/kadi/json"
# URLs where the documentation is hosted.
URL_RTD_STABLE = "https://kadi4mat.readthedocs.io/en/stable"
URL_RTD_LATEST = "https://kadi4mat.readthedocs.io/en/latest"


# Local storage type for uploads and files, which is used as default.
STORAGE_TYPE_LOCAL = "local"


# Active state value for all stateful models.
MODEL_STATE_ACTIVE = "active"


# All API versions that are currently available. Defined here, as these are also used in
# places where no application context is available.
API_VERSIONS = ["1.0"]
