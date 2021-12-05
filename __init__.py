import json
import os
from ._fitting import fit
from ._prediction import find_similarity, answer


__author__ = """M. Mehdi Samsami"""
__email__ = "mehdisamsami@live.com"
__version__ = '0.0.1'


def parse(input_):
    if type(input_) is list:
        return "\n".join(input_)
    elif type(input_) is str:
        return input_.split("\n")


class QnABot():
    def __init__(self, kb_dir='qnabot/knowledge_base.json', model='tfidf'):
        self.kb_dir_ = kb_dir
        try:
            # Load the knowledge base
            with open(self.kb_dir_) as file:
                self.data = json.load(file)
        except:
            raise FileNotFoundError('Knowledge base file cannot be found.')

        self.kb_name_ = self.data['info']['name']
        self.kb_version_ = self.data['info']['version']
        self.kb_author_ = self.data['info']['author']

        self.no_answers = self.data['no_answer']
        self.q = [item['q'] for item in self.data['qna']]
        self.q_idx = []
        for i, item in enumerate(self.q):
            self.q_idx.extend([i for j in range(len(item))])
        self.q = [item for elem in self.q for item in elem]

        self.model_name = model
        self.model = None
        self.is_fitted_ = False
        self.ref_embed = None

    def fit(self, *args, **kwargs):
        return fit(self, *args, **kwargs)

    def find_similarity(self, input=""):
        return find_similarity(self, input=input)

    def answer(self, input="", min_score=0.4, return_score=False):
        return answer(self, input=input, min_score=min_score, return_score=return_score)

    def knowledge_base(self):
        os.system(f"streamlit run qnabot/knowledge_base.py {self.kb_dir_}")



