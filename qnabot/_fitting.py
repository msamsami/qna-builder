from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer


def fit(self, decode_error='strict', strip_accents='ascii', lowercase=True, preprocessor=None, tokenizer=None,
        stop_words=None, analyzer='word', norm='l2',
        max_df=1.0, min_df=1, use_idf=True, smooth_idf=True, sublinear_tf=False,
        n_features=1048576, alternate_sign=True):

    if self.model_name not in ['tfidf', 'murmurhash3']:
        raise ValueError("model must be either 'tfidf' or 'murmurhash3'")

    if self.model_name == 'tfidf':
        self.model = TfidfVectorizer(decode_error=decode_error, strip_accents=strip_accents, lowercase=lowercase,
                                     norm=norm, preprocessor=preprocessor, tokenizer=tokenizer, stop_words=stop_words,
                                     analyzer=analyzer, max_df=max_df, min_df=min_df, use_idf=use_idf,
                                     smooth_idf=smooth_idf, sublinear_tf=sublinear_tf)

        self.ref_embed = self.model.fit_transform(self.q)
        self.__is_fitted = True

    elif self.model_name == 'murmurhash3':
        self.model = HashingVectorizer(decode_error=decode_error, strip_accents=strip_accents, lowercase=lowercase,
                                       norm=norm, preprocessor=preprocessor, tokenizer=tokenizer, stop_words=stop_words,
                                       analyzer=analyzer, n_features=n_features, alternate_sign=alternate_sign)

        self.ref_embed = self.model.fit_transform(self.q)
        self.__is_fitted = True

