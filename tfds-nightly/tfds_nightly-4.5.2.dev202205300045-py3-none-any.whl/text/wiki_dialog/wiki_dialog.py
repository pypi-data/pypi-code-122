# coding=utf-8
# Copyright 2022 The TensorFlow Datasets Authors.
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

"""Dialog Inpainting WikiDialog TFDS datasets."""

import json
import os
from typing import Any, Dict, Tuple, Sequence

import tensorflow as tf
import tensorflow_datasets.public_api as tfds

_DESCRIPTION = """\
WikiDialog is a large dataset of synthetically generated information-seeking
conversations. Each conversation in the dataset contains two speakers grounded
in a passage from English Wikipedia: one speaker’s utterances consist of exact
sentences from the passage; the other speaker is generated by a large language
model.
"""

# TODO(vzhao): Adds citation.
_CITATION = ''

_BASE_DOWNLOAD_URL = 'https://storage.googleapis.com/gresearch/dialog-inpainting/'


def _parse_json(text: str) -> Tuple[int, Dict[str, Any]]:
  """Parses query json object."""
  # Adds a hash key for each example.
  key = hash(text.encode())
  data = json.loads(text)
  return key, data


class WikiDialogConfig(tfds.core.BuilderConfig):
  """BuilderConfig for WikiDialog dataset."""

  def __init__(self, name: str, base_download_url: str, **kwargs):
    """BuilderConfig for WikiDialog.

    Args:
      name: string, the name for the config.
      base_download_url: Path to jsonl files.
      **kwargs: keyword arguments forwarded to super.
    """
    super(WikiDialogConfig, self).__init__(name=name, **kwargs)

    self.base_download_url = base_download_url


class WikiDialog(tfds.core.GeneratorBasedBuilder):
  """DatasetBuilder for WikiDialog from dialog inpainter."""
  VERSION = tfds.core.Version('1.0.0')
  RELEASE_NOTES = {
      '1.0.0': 'Initial release.',
  }
  BUILDER_CONFIGS = [
      WikiDialogConfig(
          'OQ',
          base_download_url=os.path.join(_BASE_DOWNLOAD_URL, 'WikiDialog_OQ'),
          description='WikiDialog generated from the dialog inpainter finetuned on OR-QuAC and QReCC. `OQ` stands for OR-QuAC and QReCC.',
      ),
  ]

  def _info(self) -> tfds.core.DatasetInfo:
    """Returns the dataset metadata."""
    return tfds.core.DatasetInfo(
        builder=self,
        description=_DESCRIPTION,
        features=tfds.features.FeaturesDict({
            'title':
                tfds.features.Text(),
            'pid':
                tfds.features.Text(),
            'passage':
                tfds.features.Text(),
            'sentences':
                tfds.features.Sequence(tfds.features.Text()),
            'utterances':
                tfds.features.Sequence(tfds.features.Text()),
            'author_num':
                tfds.features.Sequence(
                    tfds.features.Tensor(shape=[], dtype=tf.int32)),
        }),
        homepage=None,
        citation=_CITATION,
    )

  def _generate_examples(self, filepaths: Sequence[str]):
    beam = tfds.core.lazy_imports.apache_beam
    return (beam.Create([os.fspath(f) for f in filepaths])
            | beam.io.ReadAllFromText()
            | beam.Map(_parse_json))

  def _split_generators(self, dl_manager: tfds.download.DownloadManager):
    """Returns SplitGenerators."""
    base_download_url = self.builder_config.base_download_url
    download_urls = {
        'train': [
            os.path.join(base_download_url,
                         f'data_train.jsonl-{i:05}-of-00099.gz')
            for i in range(99)
        ],
        'validation': [
            os.path.join(base_download_url, 'data_validation.jsonl.gz')
        ],
    }
    filepaths = dl_manager.download(download_urls)

    splits = {
        'train': self._generate_examples(filepaths['train']),
        'validation': self._generate_examples(filepaths['validation']),
    }
    return splits
