import json
import subprocess
from typing import List

from .._utils import check_type_error
from ._const import KNOWLEDGE_BASE_EDITOR_FILE_PATH
from ._exceptions import KnowledgeBaseSchemaError
from ._types import FilePath, QnA, QnAKBMapping, QnAKBMappingExtra


class QnAKnowledgeBase:
    _is_loaded: bool = False

    _info = {
        "name": None,
        "version": None,
        "author": None
    }

    _cache_data: QnAKBMappingExtra = {
        "qna": None,
        "idk_answers": None,
        "ref_questions": None,
        "ref_questions_idx": None
    }

    def __init__(self, filepath_or_buffer: FilePath, cache: bool = False):
        """Initializes an instance of the class for a given knowledge base.

        Args:
            filepath_or_buffer (FilePath): Path to the knowledge base JSON file.
            cache (bool): Whether to cache the entire knowledge base in memory. Defaults to False.

        Returns:
            self: The instance itself.
        """
        self.filepath_or_buffer = filepath_or_buffer
        self.cache = cache

    def _load(self, filepath_or_buffer: FilePath) -> QnAKBMapping:
        with open(filepath_or_buffer, "r") as file:
            kb: dict = json.load(file)

        check_kb_schema(kb)

        self._set_info(kb["info"])

        if self.cache:
            ref_questions, ref_questions_idx = self._ref_questions(kb["qna"])
            _cache_data: QnAKBMappingExtra = {
                "qna": kb["qna"],
                "idk_answers": kb["idk_answers"],
                "ref_questions": ref_questions,
                "ref_questions_idx": ref_questions_idx
            }

        self._is_loaded = True

        return dict(qna=kb["qna"], idk_answers=kb["idk_answers"])

    def _set_info(self, info: dict):
        self._info["name"] = info.get('name')
        self._info["version"] = info.get('version')
        self._info["author"] = info.get('author')

    @staticmethod
    def _ref_questions(qna: List[QnA]):
        ref_questions_unpacked = [item['q'] for item in qna]
        ref_questions = [item for elem in ref_questions_unpacked for item in elem]

        ref_questions_idx = list()
        for i, item in enumerate(ref_questions_unpacked):
            ref_questions_idx.extend([i] * len(item))

        return ref_questions, ref_questions_idx

    @property
    def name(self) -> str:
        """Returns the name of the knowledge base.

        """
        return self._info["name"]

    @property
    def author(self) -> str:
        """Returns the name of the knowledge base author.

        """
        return self._info["author"]

    @property
    def version(self) -> str:
        """Returns the name of the knowledge base.

        """
        return self._info["version"]

    @property
    def qna(self) -> List[QnA]:
        """Returns the list of questions and answers in the knowledge base.

        """
        if self.cache and self._is_loaded:
            return self._cache_data['qna']
        else:
            return self._load(filepath_or_buffer=self.filepath_or_buffer)["qna"]

    @property
    def idk_answers(self) -> List[str]:
        """Returns the list of "I don't know" answers in the knowledge base.

        """
        if self.cache and self._is_loaded:
            return self._cache_data['idk_answers']
        else:
            return self._load(filepath_or_buffer=self.filepath_or_buffer)["idk_answers"]

    @property
    def ref_questions(self) -> List[str]:
        """Returns the list of reference questions in the knowledge base.

        """
        if self.cache and self._is_loaded:
            return self._cache_data['ref_questions']
        else:
            return self._ref_questions(self._load(filepath_or_buffer=self.filepath_or_buffer)["qna"])[0]

    @property
    def ref_questions_idx(self) -> List[int]:
        """Returns the list of indices of the reference questions in the knowledge base.

        """
        if self.cache and self._is_loaded:
            return self._cache_data['ref_questions_idx']
        else:
            return self._ref_questions(self._load(filepath_or_buffer=self.filepath_or_buffer)["qna"])[1]

    def run_editor(self):
        """Opens the knowledge base editor app in the web browser.

        Applicable only when self.file_path is a valid knowledge base file path.
        """
        editor(self.filepath_or_buffer)

    def __repr__(self):
        return "<QnAKnowledgeBase(name='%s', author='%s', version=%s)>" % (self.name, self.author, self.version)


def check_kb_schema(data: dict):
    """Checks the schema of a knowledge base and raises error if it doesn't match the correct schema of QnABot
    knowledge base.

    Args:
        data (dict): A dictionary containing knowledge base data.

    """
    main_keys = data.keys()

    for key in ['info', 'idk_answers', 'qna']:
        if key not in main_keys:
            raise KnowledgeBaseSchemaError(f"Knowledge base must have an '{key}' field")

    if 'name' not in data['info'].keys():
        raise KnowledgeBaseSchemaError(f"'name' is not provided in 'info'")

    for key in data['info'].keys():
        check_type_error(key, data['info'][key], 'str')

    check_type_error('idk_answers', data['idk_answers'], ['str', ])
    check_type_error('qna', data['qna'], [{"q": [], "a": []}, ])


def editor(file_path: str) -> None:
    """Opens the knowledge base editor app in the web browser.

    Args:
        file_path (str): Knowledge base file path.
    """
    check_type_error('file_path', file_path, 'str')

    subprocess.run(f"streamlit run {KNOWLEDGE_BASE_EDITOR_FILE_PATH} {file_path}", shell=True, check=True)
