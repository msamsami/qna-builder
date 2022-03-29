import numpy as np
from typing import Tuple, Union
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances, manhattan_distances, haversine_distances
from sklearn.preprocessing import MinMaxScaler
from sklearn.exceptions import NotFittedError
from qnabot import const
from ._fitting import _load_knowledge_base, _initialize_knowledge_base


similarity = {
        'cosine': cosine_similarity,
        'euclidean': euclidean_distances,
        'manhattan': manhattan_distances,
        'haversine': haversine_distances
    }


def find_similarity(self, input: str) -> Tuple[int, float]:
    if not self.__is_fitted:
        raise NotFittedError('The model is not fitted. Use fit() method before calling answer()')

    if self.metric not in const.METRICS:
        raise ValueError(f"similarity metric '{self.similarity_metric}' is not supported")

    if not self.cache and type(self.knowledge_base) is not str:
        raise ValueError("A valid file path must be entered for 'knowledge_base' when cache=False")

    # Retrieve questions' indices from knowledge base
    if self.cache:
        q_idx = self.q_idx
    else:
        _, _, _, q_idx = _load_knowledge_base(data=_initialize_knowledge_base(self, knowledge_base=self.knowledge_base))

    # Extract input statement embedding
    input_embed = self.model.transform([input])

    # Calculate the similarities between the input embedding and the reference embeddings
    similarities = similarity[self.metric](input_embed, self.ref_embed).flatten()
    if self.metric != 'cosine':
        similarities = MinMaxScaler().fit_transform(similarities.reshape(-1, 1))
        similarities = 1.0 - similarities.flatten()

    # Find the ID of the answer with highest score
    highest_id = int(np.argmax(similarities))
    highest_id = q_idx[highest_id]

    # Find the score of the answer with highest score
    score = float(similarities[highest_id])

    return highest_id, score


def answer(self, input: str, min_score: float, return_score: bool) -> Union[str, Tuple[str, float]]:
    highest_id, score = self.find_similarity(input)

    # Retrieve knowledge base data
    if self.cache:
        data = self.data
        no_answer = self.no_answer
    else:
        data, no_answer, _, _ = _load_knowledge_base(
            data=_initialize_knowledge_base(self, knowledge_base=self.knowledge_base)
        )

    # If score was lower than the minimum accepted value
    if score < min_score:
        # Return a random "I don't understand" answer
        answer_ = np.random.choice(no_answer)

    else:
        # Pick a random answer among the answers of the most similar question
        answer_ = np.random.choice(data['qna'][highest_id]['a'])

    if return_score:
        return answer_, score
    else:
        return answer_
