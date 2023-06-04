import codecs
from os import path
from setuptools import setup


setup(
    name='qna-bot',
    version='0.1.1',
    description='Similarity-based conversational dialog engine for Python.',
    keywords=['python', 'qna', 'qnabot', 'chat', 'chatbot', 'conversation', 'dialog', 'nlp'],
    author='Mehdi Samsami',
    author_email='mehdisamsami@live.com',
    url='https://github.com/msamsami/qna-bot',
    project_urls={
        'Documentation': 'https://qna-bot.readthedocs.io',
    },
    long_description=codecs.open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=['qnabot'],
    classifiers=[
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Communications :: Chat',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires=">=3.7",
    install_requires=['scikit-learn==1.0.2'],
    extras_require={
        'kb_editor': ['streamlit==1.21.0']
    },
)
