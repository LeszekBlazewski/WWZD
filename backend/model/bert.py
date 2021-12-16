from typing import _TypedDict
from pytorch_pretrained_bert.modeling import BertPreTrainedModel, BertModel
import torch


class BertConfig(_TypedDict):
    attention_probs_dropout_prob: float
    hidden_act: str
    hidden_dropout_prob: float
    hidden_size: int
    initializer_range: float
    intermediate_size: int
    max_position_embeddings: int
    num_attention_heads: int
    num_hidden_layers: int
    type_vocab_size: int
    vocab_size: int


class BertForMultiLabelSequenceClassification(BertPreTrainedModel):
    def __init__(self, config: BertConfig, num_labels: int):
        super().__init__(config)
        self.bert = BertModel(config)
        self.dropout = torch.nn.Dropout(config.hidden_dropout_prob)
        self.classifier = torch.nn.Linear(config.hidden_size, num_labels)
        self.apply(self.init_bert_weights)

    def forward(self, input_ids, token_type_ids=None, attention_mask=None):
        _, pooled_output = self.bert(
            input_ids, token_type_ids, attention_mask, output_all_encoded_layers=False
        )
        pooled_output = self.dropout(pooled_output)
        logits = self.classifier(pooled_output)
        return (pooled_output, logits)
