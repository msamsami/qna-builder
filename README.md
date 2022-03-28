# QnA Bot

<div style="text-align:center">
<img src="https://icon-library.com/images/chatbot-icon/chatbot-icon-8.jpg"
     alt="QnA Bot Image" />
</div>

**QnA Bot** is a similarity-based conversational dialog engine for Python which makes it easy
to generate automated responses to input text according to a set of known conversations, i.e.,
question-answer pairs, stored in a ***knowledge base***. QnA Bot relies on a collection
of question-answer pairs to generate (predict) answers for new inputs.

# Install

-------------------------
The easiest way to install the qna-bot is using `pip`:
```shell
pip install git+https://github.com/msamsami/qna-bot
```
This library is shipped as an all-in-one module implementation with minimalistic
dependencies and requirements.

# Getting started

-------------------------

QnA Bot can be set up and used in four simple steps:
1. Import **`QnABot`** class

```python
from qnabot import QnABot
```

2. Initialize a bot using a knowledge base
```python
bot = QnABot(kb_dir='knowledge_base.json')
```

3. Fit the bot engine to the knowledge base
```python
bot.fit()
```

4. Generate answers
```python
bot.answer("Hey. What's up?")
```

# Algorithms

-------------------------
Currently, QnA Bot engine supports the following algorithms for similarity-based answer generation:
- TF-IDF (`bot.model='tfidf'`)
- Murmurhash3 (`bot.model='murmurhash3'`)


# Knowledge base editor

-------------------------
By calling `bot.knowledge_base()`, the knowledge base editor window will open up in your web browser
and allows you to edit your knowledge base by adding, removing, or modifying questions/answers.
Here you can see a screenshot of the knowledge base editor:

<div style="text-align:center">
<img src="knowledge_base_screenshot.png"
     alt="QnA Bot Knowledge Base Editor" />
</div>

Note that you need to install the optional requirement [streamlit](https://streamlit.io/)
to be able to use the knowledge base editor.