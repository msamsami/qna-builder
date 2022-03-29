import codecs
from os import path
from setuptools import setup


setup(
    name='qna-bot',
    version='0.0.2',
    description='Similarity-based conversational dialog engine for Python.',
    keywords=['python', 'qna', 'chat', 'chatbot', 'conversational', 'dialog'],
    author='Mehdi Samsami',
    author_email='mehdisamsami@live.com',
    url='https://github.com/msamsami/qna-bot',
    long_description=codecs.open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=['qnabot'],
    classifiers=[
        'Topic :: Probabilistic Classification',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires=">=3.4",
    install_requires=['scikit-learn==1.0.2'],
    extras_require={
        'knoledge_base_editor': ['streamlit==1.8.0']
    },
)
