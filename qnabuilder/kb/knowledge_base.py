import json
import subprocess
from typing import List

from .validators import check_kb_schema
from ._const import KNOWLEDGE_BASE_EDITOR_FILE_PATH
from ._types import FilePath, QnA, QnAKbMapping, QnAKbMappingExtra


class QnAKnowledgeBase:
    _is_loaded: bool = False

    _info = {
        "name": None,
        "version": None,
        "author": None
    }

    _cache_data: QnAKbMappingExtra = {
        "qna": None,
        "idk_answers": None,
        "ref_questions": None,
        "ref_questions_idx": None
    }

    def __init__(self, filepath_or_buffer: FilePath, cache: bool = False):
        """Initializes an instance of the class for a given knowledge base file.

        Args:
            filepath_or_buffer (FilePath): Path to the knowledge base JSON file.
            cache (bool): Whether to cache the entire knowledge base in memory. Defaults to False.

        """
        self.filepath_or_buffer = filepath_or_buffer
        self.cache = cache

    def _load(self, filepath_or_buffer: FilePath) -> QnAKbMapping:
        with open(filepath_or_buffer, "r") as file:
            kb: dict = json.load(file)

        check_kb_schema(kb)

        self._set_info(kb["info"])

        if self.cache:
            ref_questions, ref_questions_idx = self._ref_questions(kb["qna"])
            self._cache_data: QnAKbMappingExtra = {
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

        streamlit package must be installed.

        """
        editor(self.filepath_or_buffer)

    def __repr__(self):
        return "<QnAKnowledgeBase(name='%s', author='%s', version=%s)>" % (self.name, self.author, self.version)


def editor(file_path: FilePath) -> None:
    """Opens the knowledge base editor app in the web browser.

    Args:
        file_path (FilePath): Knowledge base file path.

    """
    subprocess.run(f"streamlit run {KNOWLEDGE_BASE_EDITOR_FILE_PATH} {file_path}", shell=True, check=True)
