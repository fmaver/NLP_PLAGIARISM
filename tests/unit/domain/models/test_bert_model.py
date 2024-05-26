from plagiarism.adapters.elasticsearch_db import ElasticsearchConn
from plagiarism.domain.models.bert_model import BertModelWrapper
from plagiarism.settings.elasticsearch_settings import ElasticsearchSettings

bert_model = BertModelWrapper()

# Initialize Elasticsearch client
es_con = ElasticsearchConn(ElasticsearchSettings())
es = es_con.conn
print(es.info())

# create unit test for testing BertModelWrapper


def test_bert_model():
    bert_model = BertModelWrapper()
    assert bert_model is not None
    assert bert_model.get_embedding("This is a test") is not None


# Create an index with a dense_vector field
index_name = "documents_testing_3"
index_status = es_con.create_index_if_not_exists(index_name)
print(index_status)

# Example documents
documents = {
    "1": "This is a document about natural language processing.",
    "2": "This document discusses machine learning algorithms.",
    "3": "Here we talk about deep learning techniques.",
}

# Index all documents
for doc_id, text in documents.items():
    indexing_status = es_con.index_document(index_name, doc_id, text, bert_model.get_embedding(text))
    print(indexing_status)

print(es_con.refresh(index_name))

# Example query
query = "Information retrieval using machine learning."
similar_docs = es_con.search_similar(index_name, query)


# Test that the search_similar_documents function returns a list
def test_search_similar_documents():
    assert type(es_con.search_similar(index_name, query)) == list
    assert len(es_con.search_similar(index_name, query)) > 0
    assert es_con.search_similar(index_name, query)[0] is not None
