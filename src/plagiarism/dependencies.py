"""
This script is for dependencies that are used in the project.
"""

from plagiarism.adapters.elasticsearch_db import ElasticsearchConn
from plagiarism.settings.elasticsearch_settings import ElasticsearchSettings

#################
# Elasticsearch #
#################

es_settings = ElasticsearchSettings()

# Elasticsearch connection settings
es = ElasticsearchConn(es_settings)
