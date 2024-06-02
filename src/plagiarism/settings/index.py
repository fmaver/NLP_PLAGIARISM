"""
This file is to define the index name for the elastic search
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class IndexSettings(BaseSettings):
    """Define index settings for Elasticsearch.

    Attributes:
        INDEX_NAME (str): Name of the index in the Elasticsearch.
    """

    INDEX_NAME: str = "plagiarism"

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_prefix="INDEX_",
    )
