import json
import os
from ._fitting import fit
from ._prediction import find_similarity, answer
from typing import Tuple, Union


class QnABot:
    def __init__(self, kb_dir: str = 'knowledge_base.json', model: str = 'tfidf') -> None:
        # Save knowledge base general info
        self.kb_dir = kb_dir
        self.kb_name = self.data['info']['name']
        self.kb_version = self.data['info']['version']
        self.kb_author = self.data['info']['author']

        # Save knowledge base details
        self.no_answers = self.data['no_answer']
        self.q = [item['q'] for item in self.data['qna']]
        self.q_idx = []
        for i, item in enumerate(self.q):
            self.q_idx.extend([i for j in range(len(item))])
        self.q = [item for elem in self.q for item in elem]

        # Save model-related details
        self.model_name = model
        self.model = None
        self.__is_fitted = False
        self.ref_embed = None

    @property
    def kb_dir(self):
        return self.kb_dir

    @kb_dir.setter
    def kb_dir(self, kb_dir):
        # Load the knowledge base
        try:
            with open(self.kb_dir) as file:
                self.data = json.load(file)
        except:
            raise FileNotFoundError('Knowledge base file cannot be found')
        self.kb_dir = kb_dir

    def fit(self, *args, **kwargs):
        return fit(self, *args, **kwargs)

    def find_similarity(self, input: str = "") -> Tuple[int, float]:
        return find_similarity(self, input=input)

    def answer(self, input: str = "", min_score: float = 0.4, return_score: bool = False) \
            -> Union[str, Tuple[str, float]]:
        return answer(self, input=input, min_score=min_score, return_score=return_score)

    def knowledge_base(self) -> None:
        os.system(f"streamlit run qnabot/knowledge_base.py {self.kb_dir}")



