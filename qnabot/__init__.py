import subprocess
from typing import Tuple, Union
from ._fitting import fit, _initialize_model
from ._prediction import find_similarity, answer
from qnabot import const


class QnABot:
    def __init__(self, model_name: str = const.DEFAULT_MODEL, metric: str = const.DEFAULT_METRIC,
                 cache: bool = False, *args, **kwargs) -> None:
        """Initializes an instance of the class.

        Args:
            model_name (str): Name of the model used for text embedding. Defaults to const.DEFAULT_MODEL.
            metric (str): Similarity metric used to find the most similar question. Defaults to const.DEFAULT_METRIC.
            cache (bool): Whether or not to cache (store) the knowledge base data in the instance. Defaults to False.
            *args, **kwargs: Other arguments and keyword arguments supported to initialize models.

        Returns:
            self: The instance itself.
        """
        self.model_name = model_name
        self.cache = cache
        self.metric = metric

        self.model = _initialize_model(model_name=model_name, *args, **kwargs)
        self.__is_fitted = False
        self.ref_embed = None

        self.knowledge_base = None
        self.kb_name = None
        self.kb_version = None
        self.kb_author = None
        self.data = dict()

    def fit(self, knowledge_base: Union[str, dict] = const.DEFAULT_KNOWLEDGE_BASE):
        """Fits QnA Bot to knowledge_base.

        Args:
            knowledge_base (Union[str, dict]): Knowledge base file path (str) or the variable containing the
                                               knowledge base (dict). Defaults to const.DEFAULT_KNOWLEDGE_BASE.

        Returns:
            self: The instance itself.
        """
        return fit(self, knowledge_base=knowledge_base)

    def find_similarity(self, input: str = '') -> Tuple[int, float]:
        """Returns the index and similarity score of the question in the knowledge base most similar to the input.

        Args:
            input (str): Input question. Defaults to ''.

        Returns:
            int: Index of the most similar question.
            float: Similarity score of the most similar question.
        """
        return find_similarity(self, input=input)

    def answer(self, input: str = '', min_score: float = const.MIN_SCORE, return_score: bool = False) \
            -> Union[str, Tuple[str, float]]:
        """Returns the index and similarity score of a question in the knowledge base that is most similar to the input.

        Args:
            input (str): Input question. Defaults to ''.
            min_score (float): Minimum similarity score below which an "I don't understand" answer will be returned.
                               Defaults to const.MIN_SCORE.
            return_score (bool): Whether or not to return the similarity score. Defaults to False.

        Returns:
            Union[str, Tuple[str, float]]: One of the answers of the most similar question in the knowledge base
                                           if return_score=False, otherwise a tuple containing:
                str: One of the answers of the most similar question in the knowledge base.
                float: Similarity score.
        """
        return answer(self, input=input, min_score=min_score, return_score=return_score)


def knowledge_base_editor(knowledge_base: str = const.DEFAULT_KNOWLEDGE_BASE) -> None:
    """Opens the knowledge base editor in the web browser.

    Args:
        knowledge_base (str): Knowledge base file path. Defaults to const.DEFAULT_KNOWLEDGE_BASE.

    """
    if type(knowledge_base) is str:
        subprocess.run(f"streamlit run {const.KNOWLEDGE_BASE_EDITOR} {knowledge_base}", shell=True, check=True)
    else:
        raise ValueError("'knowledge_base' must be a valid file path")
