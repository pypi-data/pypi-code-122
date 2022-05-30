# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""Utilities for preprocessing sequence data.

Deprecated: `tf.keras.preprocessing.sequence` APIs are not recommended for new
code. Prefer `tf.keras.utils.timeseries_dataset_from_array` and
the `tf.data` APIs which provide a much more flexible mechanisms for dealing
with sequences. See the [tf.data guide](https://www.tensorflow.org/guide/data)
for more details.

"""

import sys as _sys

from keras.preprocessing.sequence import TimeseriesGenerator
from keras.preprocessing.sequence import make_sampling_table
from keras.preprocessing.sequence import skipgrams
from keras.utils.data_utils import pad_sequences