# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# © Copyright IBM Corp. 2021, 2022  All Rights Reserved.
# US Government Users Restricted Rights -Use, duplication or disclosure restricted by 
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------


from enum import Enum

RANGE_BUFFER_CONSTANT = 0.05
CATEGORICAL_UNIQUE_THRESHOLD = 0.8
MAX_DISTINCT_CATEGORIES = 100000
CATEGORY_PROPORTION_THRESHOLD = 0.1  # 1/10th of full training data

# DDM constants
DDM_LABEL_COLUMN = "ddm_label"
PROBABILITY_DIFFERENCE = "probability_diff"

# Model Drift Error Bounds
DRIFT_RANGE_BUFFER_UPPER_BOUND = 0.02
DRIFT_RANGE_BUFFER_LOWER_BOUND = -0.07

class ConstraintKind(Enum):
    SINGLE_COLUMN = "single_column"
    TWO_COLUMN = "two_column"


class ColumnType(Enum):
    NUMERIC_DISCRETE = "numeric_discrete"
    NUMERIC_CONTINUOUS = "numeric_continuous"
    CATEGORICAL = "categorical"


class ConstraintName(Enum):
    NUMERIC_RANGE_CONSTRAINT = "numeric_range_constraint"
    CATEGORICAL_DISTRIBUTION_CONSTRAINT = "categorical_distribution_constraint"
    CAT_CAT_DISTRIBUTION_CONSTRAINT = "catcat_distribution_constraint"
    CAT_NUM_RANGE_CONSTRAINT = "catnum_range_constraint"


class DriftTableColumnType(Enum):
    STRING = "string"
    FLOAT = "float"
    BOOLEAN = "boolean"
    TIMESTAMP = "timestamp"
