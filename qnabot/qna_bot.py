from typing import Any, Tuple, Union, List

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

from kb import QnAKnowledgeBase, FilePath, QnA
from ._enum import EmbeddingModel, SimilarityMetric


similarity = {
    'cosine': cosine_similarity,
    'euclidean': euclidean_distances,
    'manhattan': manhattan_distances,
    'haversine': haversine_distances
}


class QnABot:
    _is_fitted: bool = False
    _model_kwargs = dict = {}

    _params = {
        "kb": None,
        "model": None,
        "ref_embeddings": None
    }

    def __init__(self, model_name: EmbeddingModel = "tfidf", similarity_metric: SimilarityMetric = "cosine",
                 min_score: float = 0.25, cache: bool = False, **kwargs) -> None:
        """Initializes an instance of the class.

        Args:
            model_name (str): Name of the model used for text embedding. Defaults to 'tfidf'.
            similarity_metric (str): Similarity metric used to find the most similar question. Defaults to 'cosine'.
            min_score (float): Minimum similarity score below which an "I don't know" answer will be returned.
                               Defaults to 0.25.
            cache (bool): Whether to cache the entire knowledge base in memory. Defaults to False.
            **kwargs: Other keyword arguments supported to initialize models.

        """
        self.model_name: str = model_name
        self.similarity_metric: str = similarity_metric
        self.min_score: float = min_score
        self.cache: bool = cache

        self._model_kwargs = kwargs

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

    def fit(self, data: Union[FilePath, QnAKnowledgeBase]):
        """Fits QnA Bot to a given knowledge base.

        Args:
            data (Union[FilePath, QnAKnowledgeBase]): Path to the knowledge base JSON file or buffer, or a
                                                       QnAKnowledgeBase object.

        Returns:
            self: The instance itself.
        """
        self._params["kb"] = data if isinstance(data, QnAKnowledgeBase) else QnAKnowledgeBase(data, self.cache)
        self._params["model"] = self._initialize_model(model_name=self.model_name, **self._model_kwargs)
        self._params["ref_embeddings"] = self.model_.fit_transform(self.knowledge_base_.ref_questions)

        self._is_fitted = True
        return self

    def find_similarity(self, input: str = "") -> Tuple[int, float]:
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
        q_idx = self.knowledge_base_.ref_questions_idx

        # Extract input statement embedding
        input_embeddings = self.model_.transform([input])

        # Calculate the similarities between the input embedding and the reference embeddings
        similarities = similarity[self.similarity_metric](input_embeddings, self.ref_embeddings_).flatten()
        if self.similarity_metric != 'cosine':
            similarities = MinMaxScaler().fit_transform(similarities.reshape(-1, 1))
            similarities = 1.0 - similarities.flatten()

        # Find the ID of the answer with the highest score
        highest_id = int(np.argmax(similarities))
        highest_id = q_idx[highest_id]

        # Find the score of the answer with the highest score
        score = float(similarities[highest_id])

        return highest_id, score

    def answer(self, input: str = "", return_score: bool = False) -> Union[str, Tuple[str, float]]:
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
        data: List[QnA] = self.knowledge_base_.qna
        idk_answers: List[str] = self.knowledge_base_.idk_answers

        # If score was lower than the minimum accepted value
        if score < self.min_score:
            # Return a random "I don't know" answer
            answer_ = np.random.choice(idk_answers)

        else:
            # Pick a random answer among the answers of the most similar question
            answer_ = np.random.choice(data[highest_id]['a'])

        if return_score:
            return answer_, score
        else:
            return answer_

    @property
    def knowledge_base_(self) -> QnAKnowledgeBase:
        """Returns the knowledge base on which the QnA Bot is fitted.

        """
        return self._params["kb"]

    @property
    def model_(self) -> Any:
        """Returns the embedding model fitted on the knowledge base.

        """
        return self._params["model"]

    @property
    def ref_embeddings_(self) -> csr_matrix:
        """Returns the embedding matrix extracted from reference questions in the knowledge base.

        """
        return self._params["ref_embeddings"]

    def __repr__(self):
        return "<QnABot(model_name='%s', similarity_metric='%s', min_score=%.2f, cache=%s)>" % \
               (self.model_name, self.similarity_metric, self.min_score, self.cache)
