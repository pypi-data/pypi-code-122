#  (C) Copyright IBM Corp. 2021.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import abc
from pyspark import SparkContext
from pyspark.sql import DataFrame,SQLContext

from IBMSparkPipelineModel import IBMSparkPipelineModel
from Wrapper import PythonJavaConversions

class Result(object):
    """
    The absract base class for Result. The `stage` field is a string representing
    the end stage of the DAG.
    """
    __metaclass__ = abc.ABCMeta

    stage = None

    @abc.abstractmethod
    def _populateResult(self, jlist):
        pass


class DataResult(Result):
    """
    The DataResult class extends from :class:`Result`. The `data` field is a DataFrame.
    """
    data = None
    _sc = SparkContext._active_spark_context

    @classmethod
    def _populateResult(cls, jlist):
        resultlist = [DataResult() for index in range(len(jlist))]
        for index in range(len(jlist)):
            resultlist[index].stage = str(jlist[index].stage())
            resultlist[index].data = DataFrame(jlist[index].data(), SQLContext.getOrCreate(cls._sc))
        return resultlist

    def show(self):
        """
        Prints the DataFrame field of DataResult class.

        :return: None
        """
        self.data.show()


class ModelResult(Result):
    """
    The ModelResult class extends from :class:`Result`. The `pipelineModel` field is an object of type
    :class:`pipeline.IBMSparkPipelineModel.IBMSparkPipelineModel`.
    """
    pipelineModel = None

    @classmethod
    def _populateResult(cls, jlist):
        resultlist = [ModelResult() for index in range(len(jlist))]
        for index in range(len(jlist)):
            resultlist[index].stage = str(jlist[index].stage())
            resultlist[index].pipelineModel = cls._from_java(jlist[index].pipelineModel())
        return resultlist

    @classmethod
    def _from_java(cls, java_stage):
        py_stages = [PythonJavaConversions._from_java_stage(s) for s in java_stage.stages()]
        # Create a new instance of this stage.
        py_stage = IBMSparkPipelineModel(py_stages)
        py_stage = PythonJavaConversions._resetUid(py_stage, java_stage.uid())
        return py_stage


class SinkResult(Result):
    """
    The SinkResult class extends from :class:`Result`. In case of a SinkResult, only the `stage`
    field is returned.
    """
    @classmethod
    def _populateResult(self, jlist):
        resultlist = [SinkResult() for index in range(len(jlist))]
        for index in range(len(jlist)):
            resultlist[index].stage = str(jlist[index].stage())
        return resultlist
