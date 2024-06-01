"""Elasticsearch settings

Defines environment variables configuration
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class ElasticsearchSettings(BaseSettings):
    """Define application configuration model.

    Constructor will attempt to determine the values of any fields not passed
    as keyword arguments by reading from the environment. Default values will
    still be used if the matching environment variable is not set.

    Environment variables:
        * ELASTICSEARCH_HOST
        * ELASTICSEARCH_PORT
        * ELASTICSEARCH_USER
        * ELASTICSEARCH_PASSWORD

    Attributes:
        HOST (str): Elasticsearch host.
        PORT (str): Elasticsearch port.
        USER (str): Elasticsearch user.
        ELASTIC_PASSWORD (str): Elasticsearch password.
    """

    HOST: str = "localhost"
    PORT: str = "9200"
    USER: str = "elastic"
    ELASTIC_PASSWORD: str = "elastic"

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_prefix="ELASTICSEARCH_",
    )
