# -*- coding : utf-8 -*-
# @Time   : 2021/11/27 23:45
# @Author : goodli
# @File   : mnist_evaluation.py
# @Project: Valley 山谷

from valley.utils.plugin import PluginType, reg_plugin
from .base import DatasetEvaluator
from valley.config import configurable
import torch
import torch.distributed as dist

class MNISTEvaluator(DatasetEvaluator):

    def __init__(self):
        self.correct_pred = 0
        self.correct_pred_tensor = 0 #torch.tensor(0).to("cuda")

        #self.batch_len = 0
        self.sample_len = 0
        self.sample_len_tensor = 0 #torch.tensor(0).to("cuda")


    def reset(self):
        #self.correct_pred = 0
        self.correct_pred_tensor = torch.tensor(0, dtype=torch.int).to("cuda")

        #self.batch_len = 0
        self.sample_len_tensor = torch.tensor(0, dtype=torch.int).to("cuda")

    def process(self, inputs, outputs):
        batch_pred = outputs.argmax(dim=1, keepdim=True)
        batch_target = inputs

        self.correct_pred_tensor += batch_pred.eq(batch_target.view_as(batch_pred)).sum()
        self.sample_len_tensor   += torch.tensor(outputs.shape[0], dtype=torch.int).to("cuda")
      
        return ""

    def evaluate(self):

        dist.all_reduce(self.correct_pred_tensor, op=dist.ReduceOp.SUM)
        dist.all_reduce(self.sample_len_tensor,   op=dist.ReduceOp.SUM)

        self.correct_pred = self.correct_pred_tensor.item()
        self.sample_len = self.sample_len_tensor.item()

        acc = 100.0 * self.correct_pred / self.sample_len
        self.reset()

        return {"acc": acc}


@reg_plugin(PluginType.EVALUATOR, "MNISTEvaluator")
class ClassifierEvalWrapper(MNISTEvaluator):
    @configurable
    def __init__(self, in_data1, in_data2, out_data, *args, **kwargs):
        super(ClassifierEvalWrapper, self).__init__()

        self.in_data1 = in_data1
        self.in_data2 = in_data2
        self.out_data = out_data

    @classmethod
    def from_config(cls, cfg):
        return {"in_data1": "predict", #cfg.EVALUATOR.in_data1,
                "in_data2": "label",   #cfg.EVALUATOR.in_data2,
                "out_data": "EVALUATE_STRING"         #cfg.EVALUATOR.out_data
                }

    def process(self, in_batch, out_batch):
        out_batch = out_batch[self.in_data1].to("cuda")  # get classify results
        in_batch = in_batch[self.in_data2].to("cuda")  # get classify groundtruth

        eval_result = super().process(in_batch, out_batch)
        return {self.out_data: eval_result}

    def evaluate(self):
        eval_result = super().evaluate()
        return {self.out_data: eval_result}
