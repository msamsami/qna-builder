import os


MODELS = [
    'tfidf',
    'murmurhash',
    'count'
]
DEFAULT_MODEL = 'tfidf'

DEFAULT_KNOWLEDGE_BASE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "knowledge_base.json")

KNOWLEDGE_BASE_EDITOR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "knowledge_base_editor.py"
)

METRICS = [
    'cosine',
    'euclidean',
    'manhattan',
    'haversine'
]
DEFAULT_METRIC = 'cosine'

MIN_SCORE = 0.25
