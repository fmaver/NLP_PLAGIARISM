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
        * ELASTICSEARCH_CERT_FINGER

    Attributes:
        HOST (str): Elasticsearch host.
        PORT (str): Elasticsearch port.
        USER (str): Elasticsearch user.
        ELASTIC_PASSWORD (str): Elasticsearch password.
        CERT_FINGER (str): Elasticsearch certificate fingerprint.
    """

    HOST: str = "localhost"
    PORT: str = "9200"
    USER: str = "elastic"
    ELASTIC_PASSWORD: str = "elastic"
    CERT_FINGER: str = "ED:FA:E0:34:DD:41:54:80:96:E1:8B:CE:28:01:4F:2A:7F:04:42:9F:C9:5E:20:5A:74:51:E4:84:06:49:94:E5"

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_prefix="ELASTICSEARCH_",
    )
