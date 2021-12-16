from types import UnionType


class InputExample(object):
    """A single test example for simple sequence classification."""

    def __init__(self, guid: int, text_a: str):
        self.guid = guid
        self.text_a = text_a


class InputFeatures(object):
    """A single set of features of data."""

    def __init__(
        self,
        input_ids: UnionType[str, list[str]],
        input_mask: list[int],
        segment_ids: list[int],
    ):
        self.input_ids = input_ids
        self.input_mask = input_mask
        self.segment_ids = segment_ids
