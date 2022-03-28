from sklearn.metrics.pairwise import cosine_similarity
from numpy import argmax, random
from typing import Tuple, Union


def find_similarity(self, input: str = "") -> Tuple[int, float]:
    if not self.__is_fitted:
        raise RuntimeError('The model is not fitted. Use fit() method before calling answer()')

    # Extract input statement embedding
    input_embed = self.model.transform([input])

    # Calculate the cosine similarities between the input embedding and the reference embeddings
    cosine_similarities = cosine_similarity(input_embed, self.ref_embed).flatten()

    # Find the ID of the answer with highest score
    highest_id = int(argmax(cosine_similarities))
    highest_id = self.q_idx[highest_id]

    # Find the score of the answer with highest score
    score = float(cosine_similarities[highest_id])

    return highest_id, score


def answer(self, input: str = "", min_score: float = 0.3, return_score: bool = False) -> Union[str, Tuple[str, float]]:
    highest_id, score = self.find_similarity(input)

    # If score was lower than the minimum accepted value
    if score < min_score:
        # Return a random "I don't understand" answer
        answer = random.choice(self.no_answers)

    else:
        # Pick a random answer among the answers of the most similar question
        answer = random.choice(self.data['qna'][highest_id]['a'])

    if return_score:
        return answer, score
    else:
        return answer


def parse(input: Union[list, str]) -> Union[str, list]:
    if type(input) is list:
        return "\n".join(input)
    elif type(input) is str:
        return input.split("\n")
