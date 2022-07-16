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

from .knowledge_base import QnAKnowledgeBase
from ._utils import check_value_error
from .const import (
    MODELS,
    DEFAULT_MODEL,
    DEFAULT_KNOWLEDGE_BASE,
    DEFAULT_KNOWLEDGE_BASE_TYPE,
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

    knowledge_base: Optional[QnAKnowledgeBase] = None   # Knowledge base object

    ref_embeddings: csr_matrix     # Reference embedding matrix returned after model fitting

    def __init__(self, model_name: str = DEFAULT_MODEL, similarity_metric: str = DEFAULT_METRIC,
                 min_score: float = MIN_SCORE, buffer: bool = False, **kwargs) -> None:
        """Initializes an instance of the class.

        Args:
            model_name (str): Name of the model used for text embedding. Defaults to DEFAULT_MODEL.
            similarity_metric (str): Similarity metric used to find the most similar question.
                                     Defaults to DEFAULT_METRIC.
            min_score (float): Minimum similarity score below which an "I don't understand" answer will be returned.
                               Defaults to MIN_SCORE.
            buffer (bool): Whether to store the knowledge base information in the memory instead of loading it from
                           file each time it's required. Defaults to False.
            **kwargs: Other keyword arguments supported to initialize models.

        Returns:
            self: The instance itself.
        """
        check_value_error('model_name', model_name, MODELS)
        check_value_error('similarity_metric', similarity_metric, METRICS)

        self.model_name: str = model_name
        self.similarity_metric: str = similarity_metric
        self.min_score: float = min_score
        self.buffer: bool = buffer

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

    def fit(self, data: Union[str, dict, QnAKnowledgeBase] = DEFAULT_KNOWLEDGE_BASE,
            type: str = DEFAULT_KNOWLEDGE_BASE_TYPE):
        """Fits QnA Bot to knowledge_base.

        Args:
            data (Union[str, dict, QnAKnowledgeBase]): Knowledge base file path (str), buffer, i.e., the variable
                                                       containing the knowledge base information (dict), or a
                                                       QnAKnowledgeBase object. Defaults to DEFAULT_KNOWLEDGE_BASE.
            type (str): Knowledge base type. Defaults to DEFAULT_KNOWLEDGE_BASE_TYPE.

        Returns:
            self: The instance itself.
        """
        self.knowledge_base = QnAKnowledgeBase(data, type, self.buffer) if not isinstance(data, QnAKnowledgeBase) else data
        self.ref_embeddings = self.model.fit_transform(self.knowledge_base.ref_questions)
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
        q_idx = self.knowledge_base.ref_questions_idx

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
        data: dict = self.knowledge_base.data
        no_answers: List[str] = self.knowledge_base.no_answers

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
        return "<QnABot (model='%s', similarity_metric='%s', min_score=%.2f, buffer=%s)>" % \
               (self.model_name, self.similarity_metric, self.min_score, self.buffer)
