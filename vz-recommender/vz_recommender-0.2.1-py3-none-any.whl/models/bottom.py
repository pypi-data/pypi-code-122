from typing import *

import torch
from torch import nn

from .bst import BST
from .txt import ContextTransformer, SequenceTransformerHistory


class BSTBottom(BST):
    def __init__(self, deep_dims, seq_dim, seq_embed_dim, deep_embed_dims, seq_hidden_size,
                 num_wide=0, num_shared=0, context_head_kwargs=None, sequence_transformer_kwargs=None,
                 item_embedding_weight=None, shared_embeddings_weight=None):
        super().__init__(deep_dims, seq_dim, seq_embed_dim, deep_embed_dims, seq_hidden_size,
                         num_wide, num_shared, context_head_kwargs, sequence_transformer_kwargs,
                         item_embedding_weight, shared_embeddings_weight)

    def forward(self, deep_in, seq_in, vl_in, wide_in=None, shared_in=None):
        """
        Args:
            deep_in: list, a list of Tensor of shape [batch_size, 1].
            seq_in: Tensor, shape [batch_size, seq_len].
            vl_in: Tensor, shape [batch_size].
            wide_in: list, a list of Tensor of shape [batch_size, 1] (default=None).
            shared_in: list, a list of Tensor of shape [batch_size, 1] (default=None).

        Return:
            out: Tensor, shape [batch_size, seq_dim].
        """
        ctx_out = self.context_head(deep_in=deep_in, wide_in=wide_in, shared_in=shared_in)
        seq_out = self.sequence_transformer(seq_in=seq_in, vl_in=vl_in)
        outs = torch.cat([seq_out, ctx_out], dim=1)
        outs = self.dense1(outs)
        outs = self.act1(outs)
        outs = self.dense2(outs)

        return outs


class TxT(nn.Module):
    def __init__(self, ctx_nums, seq_num, cross_size=200, is_candidate_mode=True,
                 context_transformer_kwargs=None, sequence_transformer_kwargs=None):
        super().__init__()
        context_transformer_kwargs = context_transformer_kwargs if context_transformer_kwargs else {}
        sequence_transformer_kwargs = sequence_transformer_kwargs if sequence_transformer_kwargs else {}
        self.is_candidate_mode = is_candidate_mode
        self.features_dim = cross_size
        self.context_transformer = ContextTransformer(
            ctx_nums=ctx_nums,
            cross_size=cross_size,
            **context_transformer_kwargs,
        )
        self.sequence_transformer = SequenceTransformerHistory(
            seq_num=seq_num,
            cross_size=cross_size,
            **sequence_transformer_kwargs,
        )
        if is_candidate_mode:
            # self.candidate_dense = nn.Linear(
            #     in_features=self.sequence_transformer.seq_embed_size,
            #     out_features=cross_size
            # )
            pass

    def forward(self, ctx_in, seq_in, vl_in, candidate_in, seq_history=None):
        """
        :param ctx_in: list, a list of Tensor of shape [batch_size, 1]
        :param seq_in: Tensor, shape [batch_size, seq_len]
        :param vl_in: Tensor, shape [batch_size]
        :param candidate_in: Tensor, shape [batch_size]
        :param seq_history: Tensor, shape [batch_size, history_len]
        :return:
        """

        ctx_out = self.context_transformer(ctx_in=ctx_in)
        seq_out = self.sequence_transformer(seq_in=seq_in, vl_in=vl_in, seq_history=seq_history)
        outs = torch.mul(seq_out, ctx_out)
        if self.is_candidate_mode:
            candidate_embed = self.sequence_transformer.seq_embedding(candidate_in)
            outs = torch.concat([outs, candidate_embed], dim=1)
        return outs
