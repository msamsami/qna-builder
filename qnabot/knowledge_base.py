import subprocess

from .const import KNOWLEDGE_BASE_EDITOR, DEFAULT_KNOWLEDGE_BASE


def knowledge_base_editor(knowledge_base: str = DEFAULT_KNOWLEDGE_BASE) -> None:
    """Opens the knowledge base editor in the web browser.

    Args:
        knowledge_base (str): Knowledge base file path. Defaults to DEFAULT_KNOWLEDGE_BASE.

    """
    if type(knowledge_base) is str:
        subprocess.run(f"streamlit run {KNOWLEDGE_BASE_EDITOR} {knowledge_base}", shell=True, check=True)
    else:
        raise ValueError("'knowledge_base' must be a valid file path")
