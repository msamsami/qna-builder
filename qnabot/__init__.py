"""
qna-bot is a similarity-based conversational dialog engine for Python that helps you quickly and easily create
smart chatbots using a knowledge base of pre-defined questions and answers.
"""

__version__ = "0.0.3"
__author__ = "Mehdi Samsami"

__all__ = ['QnABot', 'knowledge_base_editor']


from .qna_bot import QnABot
from .knowledge_base import knowledge_base_editor
