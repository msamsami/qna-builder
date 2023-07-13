from .._utils import check_type_error
from ._exceptions import KnowledgeBaseSchemaError


def check_kb_schema(data: dict):
    """Checks the schema of a knowledge base and raises error if it doesn't match the correct schema of QnABot
    knowledge base.

    Args:
        data (dict): A dictionary containing knowledge base data.

    """
    main_keys = data.keys()

    for key in ["info", "idk_answers", "qna"]:
        if key not in main_keys:
            raise KnowledgeBaseSchemaError(f"Knowledge base must have an '{key}' field")

    if "name" not in data["info"].keys():
        raise KnowledgeBaseSchemaError(f"'name' is not provided in 'info'")

    for key in data["info"].keys():
        check_type_error(key, data["info"][key], "str")

    check_type_error("idk_answers", data["idk_answers"], ["str",])
    check_type_error("qna", data["qna"], [{"q": [], "a": []},])
