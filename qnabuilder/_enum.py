from enum import Enum


__all__ = [
    "EmbeddingModel",
    "SimilarityMetric"
]


class EmbeddingModel(str, Enum):
    """
    Names of text embedding models.
    """
    TFIDF = "tfidf"
    MURMURHASH = "murmurhash"
    COUNT = "count"


class SimilarityMetric(str, Enum):
    """
    Names of similarity calculation metrics.
    """
    COSINE = "cosine"
    EUCLIDEAN = "euclidean"
    MANHATTAN = "manhattan"
    HAVERSINE = "haversine"
