"""
This script is for elastic search database connection.
"""

from elasticsearch import Elasticsearch
from sklearn.metrics.pairwise import cosine_similarity

from plagiarism.adapters.detector import SentenceDetector
from plagiarism.domain.models.bert_model import BertModelWrapper
from plagiarism.settings.elasticsearch_settings import ElasticsearchSettings


class ElasticsearchConn:
    def __init__(self, es_settings: ElasticsearchSettings):
        self.host = es_settings.HOST
        self.port = es_settings.PORT
        self.user = es_settings.USER
        self.password = es_settings.ELASTIC_PASSWORD
        self.conn = self.get_conn()

    def get_conn(self):
        return Elasticsearch(
            hosts=f"https://{self.host}:{self.port}", basic_auth=(self.user, self.password), verify_certs=False
        )

    def create_index_if_not_exists(self, index_name: str):
        if not self.conn.indices.exists(index=index_name):
            self.conn.indices.create(
                index=index_name,
                body={
                    "mappings": {
                        "properties": {"text": {"type": "text"}, "vector": {"type": "dense_vector", "dims": 768}}
                    }
                },
            )
            return "Index created successfully"
        return "Index already exists"

    def index_document(self, index_name: str, doc_id: str, text: str, embedding: list, student_name: str, topic: str):
        doc = {"student_name": student_name, "Topic": topic, "text": text, "vector": embedding}
        self.conn.index(index=index_name, id=doc_id, body=doc)
        return "Document indexed successfully"

    def refresh(self, index_name: str):
        self.conn.indices.refresh(index=index_name)
        return "Index refreshed successfully"

    def search_similar(self, index_name: str, query_text: str, k=None):
        bert_model = BertModelWrapper()
        query_embedding = bert_model.get_embedding(query_text)

        print(self.create_index_if_not_exists(index_name))

        script_query = {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'vector')",
                    "params": {"query_vector": query_embedding},
                },
            }
        }
        size = k if k else 5
        response = self.conn.search(
            index=index_name, body={"size": size, "query": script_query, "_source": {"excludes": ["vector"]}}
        )
        return response["hits"]["hits"]

    def detect_plagiarized_sentences(
        self, new_text_sentences: list[str], new_sentences_embedding: list[str], plagiarized_text: str
    ) -> list[tuple[str, str, float]]:
        bert_model = BertModelWrapper()
        sentence_detector = SentenceDetector()
        plagiarized_sentences_result = []

        plagiarized_sentences = sentence_detector.get_sentences(plagiarized_text)
        plagiarized_sentences_embedding = [bert_model.get_embedding(sentence) for sentence in plagiarized_sentences]

        for i, new_sentence_embedding in enumerate(new_sentences_embedding):
            for j, plagiarized_sentence_embedding in enumerate(plagiarized_sentences_embedding):
                if (
                    "?" not in new_text_sentences[i]
                    and "?" not in plagiarized_sentences[j]
                    and len(new_text_sentences[i]) > 10
                    and len(plagiarized_sentences[j]) > 10
                    and "capítulos" not in new_text_sentences[i]
                    and "capítulos" not in plagiarized_sentences[j]
                    and "explique" not in new_text_sentences[i]
                    and "explique" not in plagiarized_sentences[j]
                    and "ejemplo" not in new_text_sentences[i]
                    and "brevemente" not in plagiarized_sentences[j]
                ):
                    similarity = cosine_similarity([new_sentence_embedding], [plagiarized_sentence_embedding])[0][0]
                    if similarity > 0.957:
                        plagiarized_sentences_result.append(
                            (new_text_sentences[i], plagiarized_sentences[j], similarity)
                        )
                        break

        return plagiarized_sentences_result
