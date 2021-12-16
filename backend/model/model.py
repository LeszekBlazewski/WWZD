import torch
import numpy as np
from backend.model.bert import BertForMultiLabelSequenceClassification
from backend.model.model_inputs import InputExample, InputFeatures
from torch.utils.data import TensorDataset, DataLoader, SequentialSampler
from app import app


class Model:
    def __init__(
        self,
        tokenizer_instance: torch.Module,
        pretrained_model_instance: BertForMultiLabelSequenceClassification,
    ):
        # 1. set the appropriate parameters
        self.eval_batch_size = app.config.MODEL_BATCH_SIZE
        self.max_seq_length = app.config.MODEL_MAX_SEQUENCE_LENGTH
        self.label_list = app.config.LABEL_LIST

        # 2. Initialize the PyTorch model based on passed model and tokenizer instance
        self.tokenizer = tokenizer_instance
        self.model = pretrained_model_instance

        self.device = torch.device("cpu")
        self.model.to(self.device)

        # 3. Set the layers to evaluation mode
        self.model.eval()

    def pre_process(self, input):
        # Converting the input to features
        test_examples = [InputExample(guid=i, text_a=x) for i, x in enumerate(input)]
        test_features = self.convert_examples_to_features(
            test_examples, self.max_seq_length, self.tokenizer
        )

        all_input_ids = torch.tensor(
            [f.input_ids for f in test_features], dtype=torch.long
        )
        all_input_mask = torch.tensor(
            [f.input_mask for f in test_features], dtype=torch.long
        )
        all_segment_ids = torch.tensor(
            [f.segment_ids for f in test_features], dtype=torch.long
        )

        # Turn input examples into batches
        test_data = TensorDataset(all_input_ids, all_input_mask, all_segment_ids)
        test_sampler = SequentialSampler(test_data)
        self.test_dataloader = DataLoader(
            test_data, sampler=test_sampler, batch_size=self.eval_batch_size
        )

        return test_examples

    def post_process(self, result):
        """Convert the prediction output to the expected output."""
        # Generate the output format for every input string
        output = [
            {
                self.label_list[0]: p[0],
                self.label_list[1]: p[1],
                self.label_list[2]: p[2],
                self.label_list[3]: p[3],
                self.label_list[4]: p[4],
                self.label_list[5]: p[5],
            }
            for p in result
        ]

        return output

    def predict(self):
        """Predict the class probabilities using the BERT model."""
        all_logits = None
        all_pooled_outputs = None

        for _, batch in enumerate(self.test_dataloader):
            input_ids, input_mask, segment_ids = batch

            input_ids = input_ids.to(self.device)
            input_mask = input_mask.to(self.device)
            segment_ids = segment_ids.to(self.device)

            # Compute the logits
            with torch.no_grad():
                pooled_output, logits = self.model(input_ids, segment_ids, input_mask)
                logits = logits.sigmoid()

            # Save the logits
            if all_logits is None:
                all_logits = logits.detach().cpu().numpy()
                all_pooled_outputs = pooled_output.detach().cpu().numpy()
            else:
                all_logits = np.concatenate(
                    (all_logits, logits.detach().cpu().numpy()), axis=0
                )
                all_pooled_outputs = np.concatenate(
                    (all_pooled_outputs, pooled_output.detach().cpu().numpy()), axis=0
                )

        # Return the last layer outputs and predictions
        return (all_pooled_outputs, all_logits)

    def convert_examples_to_features(examples, max_seq_length, tokenizer):
        """Loads a data file into a list of `InputBatch`s."""

        features = []
        for (_, example) in enumerate(examples):
            tokens_a = tokenizer.tokenize(str(example.text_a))

            # Account for [CLS] and [SEP] with "- 2"
            if len(tokens_a) > max_seq_length - 2:
                tokens_a = tokens_a[: (max_seq_length - 2)]

            # The convention in BERT is:
            # (a) For sequence pairs:
            #  tokens:   [CLS] is this jack ##son ##ville ? [SEP] no it is not . [SEP]
            #  type_ids: 0   0  0    0    0     0       0 0    1  1  1  1   1 1
            # (b) For single sequences:
            #  tokens:   [CLS] the dog is hairy . [SEP]
            #  type_ids: 0   0   0   0  0     0 0
            #
            # Where "type_ids" are used to indicate whether this is the first
            # sequence or the second sequence. The embedding vectors for `type=0` and
            # `type=1` were learned during pre-training and are added to the wordpiece
            # embedding vector (and position vector). This is not *strictly* necessary
            # since the [SEP] token unambigiously separates the sequences, but it makes
            # it easier for the model to learn the concept of sequences.
            #
            # For classification tasks, the first vector (corresponding to [CLS]) is
            # used as as the "sentence vector". Note that this only makes sense because
            # the entire model is fine-tuned.
            tokens = ["[CLS]"] + tokens_a + ["[SEP]"]
            segment_ids = [0] * len(tokens)

            input_ids = tokenizer.convert_tokens_to_ids(tokens)

            # The mask has 1 for real tokens and 0 for padding tokens. Only real
            # tokens are attended to.
            input_mask = [1] * len(input_ids)

            # Zero-pad up to the sequence length.
            padding = [0] * (max_seq_length - len(input_ids))
            input_ids += padding
            input_mask += padding
            segment_ids += padding

            features.append(
                InputFeatures(
                    input_ids=input_ids, input_mask=input_mask, segment_ids=segment_ids
                )
            )
        return features
