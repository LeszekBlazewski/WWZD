from typing import TypedDict


class BertConfig(TypedDict):
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
