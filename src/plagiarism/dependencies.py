"""
This script is for dependencies that are used in the project.
"""
from typing import Annotated

from fastapi import Depends

from plagiarism.adapters.assignment_reader import SklearnTopicPredictor
from plagiarism.adapters.elasticsearch_db import ElasticsearchConn
from plagiarism.settings.api_settings import ApplicationSettings
from plagiarism.settings.elasticsearch_settings import ElasticsearchSettings

API_SETTINGS = ApplicationSettings()

#################
# Elasticsearch #
#################

es_settings = ElasticsearchSettings()

# Elasticsearch connection settings
es = ElasticsearchConn(es_settings)

###################
# Topic Predictor #
###################
topic_predictor = None


def get_topic_predictor():
    """
    Returns the topic predictor.
    """
    global topic_predictor

    if topic_predictor is None:
        topic_predictor = SklearnTopicPredictor(download=False, model_path=API_SETTINGS.MODEL_PATH)

    return topic_predictor


TopicPredictorDependency = Annotated[SklearnTopicPredictor | None, Depends(get_topic_predictor)]
