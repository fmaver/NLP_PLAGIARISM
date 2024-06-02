"""
Assignments Entry Point.
"""
import logging
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from plagiarism.adapters.detector import NameDetector
from plagiarism.adapters.document_converter import DocumentAnalyzer
from plagiarism.adapters.elasticsearch_db import ElasticsearchConn
from plagiarism.dependencies import TopicPredictorDependency
from plagiarism.domain.events.assignments import AssignmentStored
from plagiarism.service_layer.sentences_detector import SentencesPlagiarized
from plagiarism.settings.elasticsearch_settings import ElasticsearchSettings
from plagiarism.settings.index import IndexSettings
from plagiarism.utils import content_type

router = APIRouter(prefix="/assignments")

supported_content_types = [
    content_type.APPLICATION_PDF,
    content_type.APPLICATION_DOCX,
    content_type.APPLICATION_PPT,
    content_type.APPLICATION_TXT,
]


@router.post(path="", status_code=status.HTTP_202_ACCEPTED, tags=["Commands"])
def search_plagiarism(
    file: Annotated[UploadFile, File(description="Assignment's File")], topic_predictor: TopicPredictorDependency
) -> AssignmentStored:
    """
    Compares an assignment against a set of other assignments to see if there is any plagiarism.

    Only PDF, DOCX, PPT and txt files are supported.
    """
    document_converter = DocumentAnalyzer()
    name_detector = NameDetector()
    sentences_plagiarized = SentencesPlagiarized()

    es_con = ElasticsearchConn(ElasticsearchSettings())
    es = es_con.conn
    index = IndexSettings()
    index_name = index.INDEX_NAME

    # checks if the file type is supported
    if file.content_type not in supported_content_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Content type {file.content_type} is not supported.",
        )

    # Submitted File
    logging.info(f"Submitted File: {file.filename}")
    logging.info("Detecting author and topic...")
    filename = file.filename
    content = document_converter.convert_into_txt(file)
    author = name_detector.get_author(filename, content)
    logging.info("...Author detected")
    topic = topic_predictor.predict(content)
    logging.info("...Topic detected")

    # Similar Documents
    logging.info("Searching for similar documents...")
    similar_docs = es_con.search_similar(index_name, content)
    logging.info("...Similar documents found")
    plagiarized_sentences = []
    i = 0
    for doc in similar_docs:
        logging.info(f"Checking plagiarized sentences in document {i}...")
        plagiarized_sentences = sentences_plagiarized.get_plagiarized_sentences(content, doc)
        i += 1

    # Score
    logging.info("Calculating similarity score...")
    score = [sentence.score for sentence in plagiarized_sentences]
    score = sum(score) / len(score) if len(score) > 0 else 0.0

    # [SimilarSentences(submitted_sentence=sentence.submitted_sentence, plagiarised_sentence=sentence.plagiarised_sentence,]
    similar_sentences = [sentence for sentence in plagiarized_sentences]
    print(f"Similar Sentences: {similar_sentences}")

    print(f"Author: {author}")
    print(f"Name: {filename}")
    print(f"Score: {score}")
    print(f"Topic: {topic}")

    return AssignmentStored(
        author=author,
        name=filename,
        score=score,
        topic=topic,
        similar_sentences=similar_sentences,
    )
