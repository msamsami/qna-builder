# QnA Bot

<div style="text-align:center">
<img src="https://icon-library.com/images/chatbot-icon/chatbot-icon-8.jpg"
     alt="QnA Bot Image" />
</div>

**QnA Bot** is a similarity-based conversational dialog engine for Python which makes it easy to generate automated responses to input text according to a set of known conversations, called the ***knowledge base***. QnA Bot relies on a collection of question-answer pairs to generate answers for new inputs. QnA Bot is can be set up and used in four simple steps:
<<<<<<< HEAD
1. Import the *QnABot* class:  `from qnabot import QnABot`
=======
1. Import the `QnABot` class:  `from qnabot import QnABot`
>>>>>>> 9cdb631ba1e26f3739afdc9a1c4c82475382cbd7
3. Initialize a bot using a knowledge base:  `bot = QnABot(kb_dir='knowledge_base.json')`
4. Fit the bot engine to the knowledge base:  `bot.fit()`
5. Generate answers:  `bot.answer('Hey. What's up?')`

Currently, QnA Bot engine supports the following algorithms for similarity-based answer generation:
- TF-IDF
<<<<<<< HEAD
- Murmurhash3
=======
- Murmurhash3

>>>>>>> 9cdb631ba1e26f3739afdc9a1c4c82475382cbd7
