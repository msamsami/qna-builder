from sklearn.metrics.pairwise import cosine_similarity
from numpy import argmax, random


def find_similarity(self, input=""):
    if not self.is_fitted_:
        RuntimeError('The model is not fitted. Use .fit() method before using .answer()')

    # Extract input statement embedding
    input_embed = self.model.transform([input])

    # Calculate the cosine similarities between the input embedding and the reference embeddings
    cosine_similarities = cosine_similarity(input_embed, self.ref_embed).flatten()

    highest_id = int(argmax(cosine_similarities))
    highest_id = self.q_idx[highest_id]
    score = float(cosine_similarities[highest_id])

    return highest_id, score


def answer(self, input="", min_score=0.3, return_score=False):
    highest_id, score = self.find_similarity(input)
    if score < min_score:  # If score was lower than the minimum accepted value
        # Return a random "I don't understand" answer
        answer = random.choice(self.no_answers)
    else:
        # Pick a random answer among the answers of the most similar question
        answer = random.choice(self.data['qna'][highest_id]['a'])

    if return_score:
        return answer, score
    else:
        return answer
