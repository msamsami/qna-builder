import os


KNOWLEDGE_BASE_TYPES = ['default', ]
DEFAULT_KNOWLEDGE_BASE_TYPE = 'default'
DEFAULT_KNOWLEDGE_BASE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "knowledge_base.json")
KNOWLEDGE_BASE_EDITOR_FILE_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "knowledge_base_editor.py"
)

MODELS = [
    'tfidf',
    'murmurhash',
    'count'
]
DEFAULT_MODEL = 'tfidf'

METRICS = [
    'cosine',
    'euclidean',
    'manhattan',
    'haversine'
]
DEFAULT_METRIC = 'cosine'

MIN_SCORE = 0.25
