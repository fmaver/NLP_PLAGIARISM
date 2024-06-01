import logging
import os

from plagiarism.adapters.assignment_reader import TopicDetector
from plagiarism.adapters.detector import NameDetector
from plagiarism.adapters.document_converter import DocumentAnalyzer
from plagiarism.adapters.elasticsearch_db import ElasticsearchConn
from plagiarism.adapters.zip_extractor import ZipExtractor
from plagiarism.domain.models.bert_model import BertModelWrapper
from plagiarism.settings.elasticsearch_settings import ElasticsearchSettings

if __name__ == "__main__":
    bert_model = BertModelWrapper()
    name_detector = NameDetector()
    topic_detector = TopicDetector()

    logging.basicConfig(level=logging.INFO)

    # Connecting to Elasticsearch
    es_con = ElasticsearchConn(ElasticsearchSettings())
    es = es_con.conn
    logging.info(es.info())
    logging.info("Connected to Elasticsearch")

    landing_files_path = "/app/raw_data/"
    source_zip_path = "/app/data/dataset-nlp-plagio-utn-20240518T005122Z-001.zip"

    # instance a zip extractor
    zip_extractor = ZipExtractor(source_zip_path, landing_files_path)
    zip_extractor.extract()

    # Convert all files into txt files using the DocumentAnalyzer
    landing_txt_path = "/app/data_txt/files/"
    da = DocumentAnalyzer()
    da.convert_files_to_txt(zip_extractor.get_files(), landing_txt_path)

    # Create an index with a dense_vector field
    index_name = "documents_for_plagiarism"
    index_status = es_con.create_index_if_not_exists(index_name)
    logging.info(index_status)

    # Index all the txt files
    for filename in os.listdir(landing_txt_path):
        if filename.endswith(".txt"):
            logging.info(f"File: {filename}")
            file_path = os.path.join(landing_txt_path, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()

                indexing_status = es_con.index_document(
                    index_name,
                    filename,
                    text,
                    bert_model.get_embedding(text),
                    name_detector.get_author(file_path, text),
                    topic_detector.get_topic(filename),
                )
                logging.info(indexing_status)

    logging.info(es_con.refresh(index_name))
