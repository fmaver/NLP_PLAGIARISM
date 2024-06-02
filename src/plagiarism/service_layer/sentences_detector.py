from plagiarism.adapters.detector import SentenceDetector
from plagiarism.adapters.elasticsearch_db import ElasticsearchConn
from plagiarism.domain.events.assignments import SimilarSentences
from plagiarism.domain.models.bert_model import BertModelWrapper
from plagiarism.settings.elasticsearch_settings import ElasticsearchSettings
from plagiarism.settings.index import IndexSettings


class SentencesPlagiarized:
    def __init__(self):
        self.index_name = IndexSettings().INDEX_NAME
        self.sentence_detector = SentenceDetector()
        self.bert_model = BertModelWrapper()
        self.es_con = ElasticsearchConn(ElasticsearchSettings())

    def get_plagiarized_sentences(self, text: str, similar_doc) -> list[SimilarSentences]:
        """
        Get the plagiarized sentences from the text.

        Args:
            similar_doc: The similar documents.
            text: The text to analyze.

        Returns:
            list[str]: The plagiarized sentences of the text.
        """
        similar_sentences = []

        query_sentences = self.sentence_detector.get_sentences(text)
        query_sentences_embedding = [self.bert_model.get_embedding(sentence) for sentence in query_sentences]

        plagiarized_sentences = self.es_con.detect_plagiarized_sentences(
            query_sentences, query_sentences_embedding, similar_doc["_source"]["text"]
        )

        for sentence, plagiarized_sentence, similarity in plagiarized_sentences:
            similar_sentences.append(
                SimilarSentences(
                    submitted_sentence=sentence,
                    plagiarised_sentence=plagiarized_sentence,
                    plagiarised_author=similar_doc["_source"]["student_name"],
                    plagiarised_filename=similar_doc["_id"],
                    score=similarity,
                )
            )
        return similar_sentences
