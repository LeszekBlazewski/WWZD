from pytorch_pretrained_bert.modeling import BertPreTrainedModel, BertModel
import torch


class BertForMultiLabelSequenceClassification(BertPreTrainedModel):
    def __init__(self, config, num_labels: int):
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
