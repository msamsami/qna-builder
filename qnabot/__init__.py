import json
import subprocess
from ._fitting import fit
from ._prediction import find_similarity, answer
from typing import Tuple, Union


class QnABot:
    def __init__(self, model: str = 'tfidf', kb_dir: str = 'qnabot/knowledge_base.json') -> None:
        # Initialize knowledge base
        self._kb_dir, self.data = None, dict()
        self.kb_dir = kb_dir

        # Save model-related details
        self.model_name = model
        self.model = None
        self.__is_fitted = False
        self.ref_embed = None

    @property
    def kb_dir(self):
        return self._kb_dir

    @kb_dir.setter
    def kb_dir(self, kb_dir):
        try:
            # Load and initialize knowledge base
            with open(kb_dir) as file:
                self.data = json.load(file)
            self._kb_dir = kb_dir
            self.kb_name = self.data['info']['name']
            self.kb_version = self.data['info']['version']
            self.kb_author = self.data['info']['author']

            # Save knowledge base details
            self.no_answers = self.data['no_answer']
            self.q = [item['q'] for item in self.data['qna']]
            self.q_idx = []
            for i, item in enumerate(self.q):
                self.q_idx.extend([i for _ in range(len(item))])
            self.q = [item for elem in self.q for item in elem]
        except:
            raise FileNotFoundError('Knowledge base file cannot be found')

    def fit(self, *args, **kwargs):
        return fit(self, *args, **kwargs)

    def find_similarity(self, input: str = "") -> Tuple[int, float]:
        return find_similarity(self, input=input)

    def answer(self, input: str = "", min_score: float = 0.4, return_score: bool = False) \
            -> Union[str, Tuple[str, float]]:
        return answer(self, input=input, min_score=min_score, return_score=return_score)

    def knowledge_base(self) -> None:
        subprocess.run(f"streamlit run qnabot/knowledge_base.py {self.kb_dir}", shell=True, check=True)
