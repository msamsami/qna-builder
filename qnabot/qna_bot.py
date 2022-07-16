import json
from typing import Tuple, Union, Optional, Any, List

import numpy as np
from scipy.sparse import csr_matrix

from sklearn.exceptions import NotFittedError
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import (
    TfidfVectorizer,
    HashingVectorizer,
    CountVectorizer
)
from sklearn.metrics.pairwise import (
    cosine_similarity,
    euclidean_distances,
    manhattan_distances,
    haversine_distances
)

from ._utils import check_value_error
from .const import (
    MODELS,
    DEFAULT_MODEL,
    DEFAULT_KNOWLEDGE_BASE,
    METRICS,
    DEFAULT_METRIC,
    MIN_SCORE
)


similarity = {
    'cosine': cosine_similarity,
    'euclidean': euclidean_distances,
    'manhattan': manhattan_distances,
    'haversine': haversine_distances
}


class QnABot:
    model: Optional[Any]    # Model instance
    _is_fitted: bool    # Model fit status

    knowledge_base: Optional[Union[str, dict]] = None   # Knowledge base file path or information
    knowledge_base_name: Optional[str] = None   # Knowledge base name
    knowledge_base_version: Optional[str] = None    # Knowledge base version
    knowledge_base_author: Optional[str] = None     # Knowledge base author name

    no_answers: List[str]   # List of "I don't understand" answers (this attribute is initialized if caching is enabled)
    q: List[str]    # List of reference questions (this attribute is initialized if caching is enabled)
    q_idx: List[int]    # List of reference questions' indices (this attribute is initialized if caching is enabled)

    ref_embeddings: csr_matrix     # Reference embedding matrix returned after model fitting

    def __init__(self, model_name: str = DEFAULT_MODEL, similarity_metric: str = DEFAULT_METRIC,
                 min_score: float = MIN_SCORE, cache: bool = False, **kwargs) -> None:
        """Initializes an instance of the class.

        Args:
            model_name (str): Name of the model used for text embedding. Defaults to DEFAULT_MODEL.
            similarity_metric (str): Similarity metric used to find the most similar question.
                                     Defaults to DEFAULT_METRIC.
            min_score (float): Minimum similarity score below which an "I don't understand" answer will be returned.
                               Defaults to MIN_SCORE.
            cache (bool): Whether to cache (store) the knowledge base information in the memory instead of loading it
                          from file each time it's required. Defaults to False.
            **kwargs: Other keyword arguments supported to initialize models.

        Returns:
            self: The instance itself.
        """
        check_value_error('model_name', model_name, MODELS)
        check_value_error('similarity_metric', similarity_metric, METRICS)

        self.model_name: str = model_name
        self.similarity_metric: str = similarity_metric
        self.min_score: float = min_score
        self.cache: bool = cache

        self.model = self._initialize_model(model_name=model_name, **kwargs)
        self._is_fitted: bool = False

    @staticmethod
    def _initialize_model(model_name: str, **kwargs):
        if model_name == 'tfidf':
            return TfidfVectorizer(**kwargs)
        elif model_name == 'murmurhash':
            return HashingVectorizer(**kwargs)
        elif model_name == 'count':
            return CountVectorizer(**kwargs)
        else:
            return None

    @staticmethod
    def load_knowledge_base(knowledge_base: Union[str, dict]) -> Tuple[dict, List[str], List[str], List[int]]:
        """Loads a QnA knowledge from file or Python dictionary.

        Args:
            knowledge_base (Union[str, dict]): Knowledge base file path (str) or the variable containing the
                                               knowledge base information (dict).

        Returns:
            Tuple[dict, List[str], List[str], List[int]]: tuple containing:
                dict: Knowledge base information.
                List[str]: List of "I don't understand" answers.
                List[str]: List of reference questions.
                List[int]: List of reference questions' indices.
        """
        if type(knowledge_base) is str:
            with open(knowledge_base) as file:
                data: dict = json.load(file)
        else:
            data: dict = knowledge_base

        no_answer = data['no_answer']
        q = [item['q'] for item in data['qna']]
        q_idx = list()
        for i, item in enumerate(q):
            q_idx.extend([i for _ in range(len(item))])
        q = [item for elem in q for item in elem]

        return data, no_answer, q, q_idx

    def init_knowledge_base(self, knowledge_base: Union[str, dict]) -> List[str]:
        if self.cache and type(knowledge_base) is not str:
            raise ValueError("A valid file path must be entered for 'knowledge_base' when caching is enabled")

        data, no_answer, q, q_idx = self.load_knowledge_base(knowledge_base)

        self.knowledge_base = knowledge_base if type(knowledge_base) is str else None
        self.knowledge_base_name = data['info']['name']
        self.knowledge_base_version = data['info']['version']
        self.knowledge_base_author = data['info']['author']

        if self.cache:
            self.knowledge_base = data
            self.no_answers = no_answer
            self.q = q
            self.q_idx = q_idx

        return q

    def fit(self, knowledge_base: Union[str, dict] = DEFAULT_KNOWLEDGE_BASE):
        """Fits QnA Bot to knowledge_base.

        Args:
            knowledge_base (Union[str, dict]): Knowledge base file path (str) or the variable containing the
                                               knowledge base information (dict). Defaults to DEFAULT_KNOWLEDGE_BASE.

        Returns:
            self: The instance itself.
        """
        questions = self.init_knowledge_base(knowledge_base=knowledge_base)
        self.ref_embeddings = self.model.fit_transform(questions)
        self._is_fitted = True
        return self

    def find_similarity(self, input: str = '') -> Tuple[int, float]:
        """Returns the index and similarity score of the question in the knowledge base most similar to the input.

        Args:
            input (str): Input question. Defaults to ''.

        Returns:
            int: Index of the most similar question.
            float: Similarity score of the most similar question.
        """
        if not self._is_fitted:
            raise NotFittedError('The model is not fitted. Use fit() method before calling answer()')

        # Retrieve questions' indices from knowledge base
        if self.cache:
            q_idx = self.q_idx
        else:
            _, _, _, q_idx = self.load_knowledge_base(knowledge_base=self.knowledge_base)

        # Extract input statement embedding
        input_embeddings = self.model.transform([input])

        # Calculate the similarities between the input embedding and the reference embeddings
        similarities = similarity[self.similarity_metric](input_embeddings, self.ref_embeddings).flatten()
        if self.similarity_metric != 'cosine':
            similarities = MinMaxScaler().fit_transform(similarities.reshape(-1, 1))
            similarities = 1.0 - similarities.flatten()

        # Find the ID of the answer with the highest score
        highest_id = int(np.argmax(similarities))
        highest_id = q_idx[highest_id]

        # Find the score of the answer with the highest score
        score = float(similarities[highest_id])

        return highest_id, score

    def answer(self, input: str = '', return_score: bool = False) -> Union[str, Tuple[str, float]]:
        """Returns the index and similarity score of a question in the knowledge base that is most similar to the input.

        Args:
            input (str): Input question. Defaults to ''
            return_score (bool): Whether to return the similarity score. Defaults to False.

        Returns:
            Union[str, Tuple[str, float]]: One of the answers of the most similar question in the knowledge base
                                           if return_score=False, otherwise a tuple containing:
                str: One of the answers of the most similar question in the knowledge base.
                float: Similarity score.
        """
        highest_id, score = self.find_similarity(input)

        # Retrieve knowledge base information
        if self.cache:
            data: dict = self.knowledge_base
            no_answers: List[str] = self.no_answers
        else:
            data, no_answers, _, _ = self.load_knowledge_base(knowledge_base=self.knowledge_base)

        # If score was lower than the minimum accepted value
        if score < self.min_score:
            # Return a random "I don't understand" answer
            answer_ = np.random.choice(no_answers)

        else:
            # Pick a random answer among the answers of the most similar question
            answer_ = np.random.choice(data['qna'][highest_id]['a'])

        if return_score:
            return answer_, score
        else:
            return answer_

    def __repr__(self):
        return "<QnABot (model='%s', similarity_metric='%s', min_score=%.2f, cache=%s)>" % \
               (self.model_name, self.similarity_metric, self.min_score, self.cache)
