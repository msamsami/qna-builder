import json
import subprocess
from typing import Union, List, Optional

from ._utils import check_value_error, check_type_error
from ._exceptions import KnowledgeBaseSchemaError
from .const import (
    KNOWLEDGE_BASE_TYPES,
    DEFAULT_KNOWLEDGE_BASE_TYPE,
    KNOWLEDGE_BASE_EDITOR_FILE_PATH
)


class QnAKnowledgeBase:
    name: Optional[str] = None  # Knowledge base name
    version: Optional[str] = None  # Knowledge base version
    author: Optional[str] = None  # Knowledge base author name
    file_path: Optional[str] = None  # Knowledge base file path

    _buffer_data: dict = {}

    def __init__(self, data: Union[str, dict], type: str = DEFAULT_KNOWLEDGE_BASE_TYPE,  buffer: bool = False):
        """Initializes an instance of the class based on a given knowledge base information.

        Args:
            data (Union[str, dict]): Knowledge base file path (str) or buffer, i.e., the variable containing the
                                     knowledge base information (dict).
            type (str): Knowledge base type. Defaults to DEFAULT_KNOWLEDGE_BASE_TYPE.
            buffer (bool): Whether to store the knowledge base information in the memory instead of loading it
                           from file each time it's required. Defaults to False.

        Returns:
            self: The instance itself.
        """
        check_value_error('type', type, KNOWLEDGE_BASE_TYPES)
        if (not buffer) and (not isinstance(data, str)):
            raise ValueError("buffer must be enabled when data is not a file path")

        self.data: Union[str, dict] = data  # Knowledge base file path or information
        self.type: str = type
        self.buffer: bool = buffer

        self._internal_init(self.data)

    @staticmethod
    def _check_schema(data: dict, type: str = DEFAULT_KNOWLEDGE_BASE_TYPE):
        main_keys = data.keys()

        if type == 'default':
            for key in ['info', 'no_answer', 'qna']:
                if key not in main_keys:
                    raise KnowledgeBaseSchemaError(f"Knowledge base must have an '{key}' field")

            if 'name' not in data['info'].keys():
                raise KnowledgeBaseSchemaError(f"'name' is not provided in 'info'")

            for key in data['info'].keys():
                check_type_error(key, data['info'][key], 'str')

            check_type_error('no_answer', data['no_answer'], ['str', ])
            check_type_error('qna', data['qna'], [{"q": [], "a": []}, ])

        else:
            pass

    def _load(self, data: Union[str, dict], only_no_answers: bool = False, only_ref_questions: bool = False):
        """Loads a QnA knowledge from file or Python dictionary.

        Args:
            data (Union[str, dict]): Knowledge base file path (str) or buffer, i.e., the variable containing the
                                     knowledge base information (dict).
        """
        if type(data) is str:
            with open(data) as file:
                data: dict = json.load(file)

        self._check_schema(data)

        no_answers = data['no_answer']
        if only_no_answers:
            return no_answers

        ref_questions_unpacked = [item['q'] for item in data['qna']]
        ref_questions = [item for elem in ref_questions_unpacked for item in elem]
        if only_ref_questions:
            return ref_questions

        ref_questions_idx = list()
        for i, item in enumerate(ref_questions_unpacked):
            ref_questions_idx.extend([i for _ in range(len(item))])

        return data, no_answers, ref_questions, ref_questions_idx

    def _internal_init(self, data: Union[str, dict]):
        if type(data) is str:
            self.file_path = data

        data, no_answers, ref_questions, ref_questions_idx = self._load(data)

        self.name = data['info']['name']
        self.version = data['info']['version'] if 'version' in data['info'].keys() else None
        self.author = data['info']['author'] if 'author' in data['info'].keys() else None

        if self.buffer:
            self.data = data
            self._buffer_data['no_answers'] = no_answers
            self._buffer_data['ref_questions'] = ref_questions
            self._buffer_data['ref_questions_idx'] = ref_questions_idx

    @property
    def no_answers(self) -> List[str]:
        """Returns the list of "I don't understand" answers.

        """
        if self.buffer:
            return self._buffer_data['no_answers']
        else:
            return self._load(data=self.data, only_no_answers=True)

    @property
    def ref_questions(self) -> List[str]:
        """Returns the list of reference questions,

        """
        if self.buffer:
            return self._buffer_data['ref_questions']
        else:
            return self._load(data=self.data, only_ref_questions=True)

    @property
    def ref_questions_idx(self) -> List[int]:
        """Returns the list of reference questions' indices,

        """
        if self.buffer:
            return self._buffer_data['ref_questions_idx']
        else:
            _, _, _, _ref_questions_idx = self._load(data=self.data)
            return _ref_questions_idx

    def run_editor(self):
        """Opens the knowledge base editor app in the web browser.

        Applicable only when self.file_path is a valid knowledge base file path.
        """
        editor(self.file_path)

    def __repr__(self):
        return "<QnAKnowledgeBase (name='%s', type='%s', buffer=%s)>" % (self.name, self.type, self.buffer)


def editor(file_path: str) -> None:
    """Opens the knowledge base editor app in the web browser.

    Args:
        file_path (str): Knowledge base file path.
    """
    check_type_error('file_path', file_path, 'str')

    subprocess.run(f"streamlit run {KNOWLEDGE_BASE_EDITOR_FILE_PATH} {file_path}", shell=True, check=True)
