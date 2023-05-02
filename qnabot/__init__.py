"""
qna-bot is a similarity-based conversational dialog engine for Python that helps you quickly and easily create
smart chatbots using a knowledge base of pre-defined questions and answers.
"""

__version__ = "0.0.5"
__author__ = "Mehdi Samsami"

__all__ = [
    "QnABot",
    "QnAKnowledgeBase",
    "EmbeddingModel",
    "SimilarityMetric"
]


from .qna_bot import QnABot
from ._enum import EmbeddingModel, SimilarityMetric
from .kb import QnAKnowledgeBase
