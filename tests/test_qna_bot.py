from unittest import TestCase

from qnabuilder import QnABot, EmbeddingModel, SimilarityMetric


class TestQnABot(TestCase):
    def test_wrong_model_name(self):
        bot = QnABot(model_name="tensorflow")
        with self.assertRaises(ValueError) as ctx:
            bot.fit()
        self.assertIn("tensorflow is not a valid model_name", str(ctx.exception))

    def test_wrong_similarity_metric(self):
        bot = QnABot(similarity_metric="mahalanobis")
        with self.assertRaises(ValueError) as ctx:
            bot.fit()
            bot.answer("hi")
        self.assertIn("mahalanobis is not a valid similarity_metric", str(ctx.exception))

    def test_generic_answer_tfidf(self):
        for metric in SimilarityMetric:
            bot = QnABot(model_name=EmbeddingModel.TFIDF, similarity_metric=metric)
            bot.fit()
            self.assertEqual(bot.answer("Who are you?"), "I am QnA Builder!")
