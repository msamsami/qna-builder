from sklearn.feature_extraction.text import TfidfVectorizer, HashingVectorizer, CountVectorizer
from qnabot import const
import json
from typing import Union, Tuple


def fit(self, knowledge_base: Union[str, dict]):
    data = _initialize_knowledge_base(self, knowledge_base=knowledge_base, store_info=True)
    data, no_answer, q, q_idx = _load_knowledge_base(data=data)
    if self.cache:
        _cache_knowledge_base(self, data, no_answer, q, q_idx)
    self.ref_embed = self.model.fit_transform(q)
    self.__is_fitted = True
    return self


def _initialize_model(model_name: str, *args, **kwargs):
    if model_name not in const.MODELS:
        raise ValueError(f"model type '{model_name}' is not supported")

    if model_name == 'tfidf':
        return TfidfVectorizer(*args, **kwargs)
    elif model_name == 'murmurhash':
        return HashingVectorizer(*args, **kwargs)
    elif model_name == 'count':
        return CountVectorizer(*args, **kwargs)
    else:
        return None


def _initialize_knowledge_base(self, knowledge_base: Union[str, dict], store_info: bool = False):
    if self.cache and type(knowledge_base) is not str:
        raise ValueError("A valid path must be entered for 'knowledge_base' when knowledge base caching is enabled")

    if type(knowledge_base) is str:
        with open(knowledge_base) as file:
            data = json.load(file)
    else:
        data = knowledge_base

    if store_info:
        self.knowledge_base = knowledge_base if type(knowledge_base) is str else None
        self.kb_name = data['info']['name']
        self.kb_version = data['info']['version']
        self.kb_author = data['info']['author']

    return data


def _load_knowledge_base(data: dict) -> Tuple[dict, list, list, list]:
    no_answer = data['no_answer']
    q = [item['q'] for item in data['qna']]
    q_idx = []
    for i, item in enumerate(q):
        q_idx.extend([i for _ in range(len(item))])
    q = [item for elem in q for item in elem]

    return data, no_answer, q, q_idx


def _cache_knowledge_base(self, data: dict, no_answer: list, q: list, q_idx: list) -> None:
    self.data = data
    self.no_answers = no_answer
    self.q = q
    self.q_idx = q_idx
