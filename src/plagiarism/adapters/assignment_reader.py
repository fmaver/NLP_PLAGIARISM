import joblib
import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


class TopicDetector:
    """
    Topic Detector.
    """

    def __init__(self):
        self.training_csv = "/app/data/training.csv"

    def get_topic(self, filename: str) -> str:
        """
        Gets the topic of the file.
        Args:
            filename: The filename.
        Returns: The topic.
        """
        topic_df = pd.read_csv(self.training_csv)
        topic = topic_df[topic_df["_id"] == filename]["topic"].values[0]
        return topic


class SklearnTopicPredictor:
    """
    Sklearn Topic Predictor.
    """

    def __init__(self, download: bool = False, model_path: str = ""):
        self.pipeline = Pipeline(
            [
                ("tfidf", TfidfVectorizer()),
                ("clf", MultinomialNB()),
            ]
        )

        if download:
            self.download_model()

        if model_path:
            self.pipeline = joblib.load(model_path)

    def download_model(self):
        """
        Downloads the model.
        """
        spacy.cli.download("es_core_news_lg")

    def predict(self, content: str) -> str:
        """
        Predicts the topic of the content.
        Args:
            content: The content to predict.
        Returns: The predicted topic.
        """
        return self.pipeline.predict([content])[0]
