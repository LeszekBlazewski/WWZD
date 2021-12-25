import torch
import numpy as np
from .bert import BertForMultiLabelSequenceClassification
from .model_inputs import InputExample, InputFeature
from torch.utils.data import TensorDataset, DataLoader, SequentialSampler
from pytorch_pretrained_bert.tokenization import BertTokenizer
from ..flask_setup.flask import app


class Model:
    def __init__(
        self,
        tokenizer_instance: torch.Module,
        pretrained_model_instance: BertForMultiLabelSequenceClassification,
        eval_batch_size: int,
        max_seq_length: int,
        label_list: list[str],
        use_cpu: bool = True,
    ):
        # 1. set the appropriate parameters
        self.eval_batch_size = eval_batch_size
        self.max_seq_length = max_seq_length
        self.label_list = label_list
        self.use_cpu = use_cpu

        # 2. Initialize the PyTorch model based on passed model and tokenizer instance
        self.tokenizer = tokenizer_instance
        self.model = pretrained_model_instance

        if self.use_cpu:
            self.device = torch.device("cpu")
            self.model.to(self.device)
        else:
            self.model.cuda()

        # 3. Set the layers to evaluation mode
        self.model.eval()

    def _pre_process(self, input: list[str]):
        # Converting the input to features
        examples = [InputExample(guid=i, text_a=x) for i, x in enumerate(input)]
        features = self.convert_examples_to_features(
            examples, self.max_seq_length, self.tokenizer
        )

        all_input_ids = torch.tensor([f.input_ids for f in features], dtype=torch.long)
        all_input_mask = torch.tensor(
            [f.input_mask for f in features], dtype=torch.long
        )
        all_segment_ids = torch.tensor(
            [f.segment_ids for f in features], dtype=torch.long
        )

        # Turn input examples into batches
        data = TensorDataset(all_input_ids, all_input_mask, all_segment_ids)
        sampler = SequentialSampler(data)
        dataloader = DataLoader(data, sampler=sampler, batch_size=self.eval_batch_size)
        return dataloader

    def _post_process(self, result):
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

    def predict(self, input: list[str]):
        """Predict the class probabilities using the BERT model."""

        dataloader = self._pre_process(input)
        all_logits = None
        all_pooled_outputs = None

        for _, batch in enumerate(dataloader):
            input_ids, input_mask, segment_ids = batch

            if self.use_cpu:
                input_ids = input_ids.to(self.device)
                input_mask = input_mask.to(self.device)
                segment_ids = segment_ids.to(self.device)
            else:
                input_ids = input_ids.cuda()
                input_mask = input_mask.cuda()
                segment_ids = segment_ids.cuda()

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

        encoded_predictions = self._post_process(all_logits)
        # Return the last layer outputs and predictions
        return (all_pooled_outputs, encoded_predictions)

    def convert_examples_to_features(
        self, examples: list[InputExample], max_seq_length: int, tokenizer
    ) -> list[InputFeature]:
        """Loads a data file into a list of `InputBatch`s."""

        features: list[InputFeature] = []
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
                InputFeature(
                    input_ids=input_ids, input_mask=input_mask, segment_ids=segment_ids
                )
            )
        return features


tokenizer_instance = BertTokenizer.from_pretrained(
    app.config["BERT_MODEL_PATH"], do_lower_case=True
)

if app.config["USE_CPU"]:
    model_state_dict = torch.load(
        f"{app.config['BERT_MODEL_PATH']}/pytorch_model.bin", map_location="cpu"
    )
else:
    model_state_dict = torch.load(f"{app.config['BERT_MODEL_PATH']}/pytorch_model.bin")

pretrained_model_instance = BertForMultiLabelSequenceClassification.from_pretrained(
    app.config["BERT_MODEL_PATH"],
    num_labels=len(app.config["LABEL_LIST"]),
    state_dict=model_state_dict,
)

model = Model(
    tokenizer_instance,
    pretrained_model_instance,
    app.config["BATCH_SIZE"],
    app.config["MAX_SEQ_LENGTH"],
    app.config["LABEL_LIST"],
    app.config["USE_CPU"],
)
