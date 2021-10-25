import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from numpy import argmax, random
from sklearn.feature_extraction.text import HashingVectorizer


def parse(input_):
    if type(input_) is list:
        return "\n".join(input_)
    elif type(input_) is str:
        return input_.split("\n")


class QnABot:
    def __init__(self, kb_dir='knowledge_base.json', model='tfidf'):
        try:
            # Load the knowledge base
            with open(kb_dir) as file:
                self.data = json.load(file)
        except:
            FileNotFoundError('Knowledge base file cannot be found.')

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

    def fit(self, decode_error='strict', strip_accents='ascii', lowercase=True, preprocessor=None, tokenizer=None,
            stop_words=None, analyzer='word', norm='l2',
            max_df=1.0, min_df=1, use_idf=True, smooth_idf=True, sublinear_tf=False,
            n_features=1048576, alternate_sign=True):

        if self.model_name=='tfidf':
            self.model = TfidfVectorizer(decode_error=decode_error, strip_accents=strip_accents, lowercase=lowercase, norm=norm,
                                         preprocessor=preprocessor, tokenizer=tokenizer, stop_words=stop_words, analyzer=analyzer,
                                         max_df=max_df, min_df=min_df, use_idf=use_idf, smooth_idf=smooth_idf, sublinear_tf=sublinear_tf)

            self.ref_embed = self.model.fit_transform(self.q)
            self.is_fitted_ = True
            return 1

        elif self.model_name=='murmurhash3':
            self.model = HashingVectorizer(decode_error=decode_error, strip_accents=strip_accents, lowercase=lowercase, norm=norm,
                                           preprocessor=preprocessor, tokenizer=tokenizer, stop_words=stop_words, analyzer=analyzer,
                                           n_features=n_features, alternate_sign=alternate_sign)

            self.ref_embed = self.model.fit_transform(self.q)
            self.is_fitted_ = True
            return 1

    def find_similarity(self, input=""):
        if not self.is_fitted_:
            RuntimeError('The model is not fitted. Use .fit() method before using .answer()')

        # Extract input statement embedding
        input_embed = self.model.transform([input])

        # Calculate the cosine similarities between the input embedding and the reference embeddings
        cosine_similarities = cosine_similarity(input_embed, self.ref_embed).flatten()

        highest_id = int(argmax(cosine_similarities))
        highest_id = self.q_idx[highest_id]
        confidence = float(cosine_similarities[highest_id])

        return highest_id, confidence

    def answer(self, input="", min_confidence=0.4, return_confidence=False):
        highest_id, confidence = self.find_similarity(input)
        if confidence < min_confidence:  # If confidence score was lower than the minimum accepted value
            # Return a random "I don't understand" response
            answer = random.choice(self.no_answers)
        else:
            # Pick a random response among closest responses
            answer = random.choice(self.data['qna'][highest_id]['a'])

        if return_confidence:
            return answer, confidence
        else:
            return answer
