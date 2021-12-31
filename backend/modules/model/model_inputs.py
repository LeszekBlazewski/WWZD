from __future__ import annotations
from typing import Union


class InputExample(object):
    """A single test example for simple sequence classification."""

    def __init__(self, guid: int, text_a: str):
        self.guid = guid
        self.text_a = text_a


class InputFeature(object):
    """A single set of features of data."""

    def __init__(
        self,
        input_ids: Union[str, list[str]],
        input_mask: list[int],
        segment_ids: list[int],
    ):
        self.input_ids = input_ids
        self.input_mask = input_mask
        self.segment_ids = segment_ids
