"""
this script will test the Elasticsearch connection
"""

from unittest.mock import Mock

import pytest

from plagiarism.adapters.elasticsearch_db import ElasticsearchConn
from plagiarism.settings.elasticsearch_settings import ElasticsearchSettings


@pytest.fixture
def es_settings():
    return ElasticsearchSettings()


def test_elasticsearch_conn(es_settings):
    es = ElasticsearchConn(es_settings)
    assert es.host == "localhost"
    assert es.port == "9200"


def test_get_conn(es_settings: ElasticsearchSettings):
    es = ElasticsearchConn(es_settings)
    conn = es.get_conn()
    print(conn.info())
    assert conn is not None


def test_create_index_if_not_exists(es_settings: ElasticsearchSettings):
    es = ElasticsearchConn(es_settings)
    index_name = "test_index"
    es.conn.indices.exists = Mock(return_value=False)
    es.conn.indices.create = Mock(return_value="Index created successfully")
    assert es.create_index_if_not_exists(index_name) == "Index created successfully"
    es.conn.indices.exists = Mock(return_value=True)
    assert es.create_index_if_not_exists(index_name) == "Index already exists"


def test_index_document(es_settings: ElasticsearchSettings):
    es = ElasticsearchConn(es_settings)
    index_name = "test_index"
    doc_id = "1"
    text = "This is a test document"
    embedding = [0.1, 0.2, 0.3]
    es.conn.index = Mock(return_value="Document indexed successfully")
    assert es.index_document(index_name, doc_id, text, embedding) == "Document indexed successfully"
