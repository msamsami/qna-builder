from os import PathLike
from typing import List, TypedDict, Union


FilePath = Union[str, "PathLike[str]"]


class QnA(TypedDict):
    q: List[str]
    a: List[str]


class QnAKbMapping(TypedDict):
    qna: List[QnA]
    idk_answers: List[str]


class QnAKbMappingExtra(TypedDict):
    qna: List[QnA]
    idk_answers: List[str]
    ref_questions: List[str]
    ref_questions_idx: List[int]
