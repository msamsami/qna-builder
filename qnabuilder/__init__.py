"""
QnA Builder is a similarity-based conversational dialog engine for Python that helps you quickly and easily create
smart chatbots using a knowledge base of pre-defined questions and answers.
"""

__version__ = "0.1.2"
__author__ = "Mehdi Samsami"

__all__ = (
    "QnABot",
    "EmbeddingModel",
    "SimilarityMetric",
    "QnAKnowledgeBase",
    "DEFAULT_KNOWLEDGE_BASE_FILE_PATH",
)


from .qna_bot import QnABot
from ._enums import EmbeddingModel, SimilarityMetric
from .kb import QnAKnowledgeBase, DEFAULT_KNOWLEDGE_BASE_FILE_PATH
