"""
This test file will test the functionality of all readers such as docx_reader, pdf_reader, and ppt_reader.

"""

import glob
import os

import pytest

from plagiarism.adapters.document_converter import DocxReader, PDFReader, PPTXReader


def test_read_docx():
    docx_reader = DocxReader()
    docx_path = "tests/unit/adapters/document_transformation/raw_documents_test/*.docx"
    docx_files = glob.glob(docx_path)

    for docx_file in docx_files:
        text = docx_reader.read_docx(docx_file)
        assert text is not None
        assert len(text) > 0


def test_read_pdf():
    pdf_reader = PDFReader()
    pdf_path = "tests/unit/adapters/document_transformation/raw_documents_test/*.pdf"
    pdf_files = glob.glob(pdf_path)

    for pdf_file in pdf_files:
        text = pdf_reader.read_pdf(pdf_file)
        assert text is not None
        assert len(text) > 0


def test_read_pptx():
    pptx_reader = PPTXReader()
    pptx_path = "tests/unit/adapters/document_transformation/raw_documents_test/*.pptx"
    pptx_files = glob.glob(pptx_path)

    for pptx_file in pptx_files:
        text = pptx_reader.read_pptx(pptx_file)
        assert text is not None
        assert len(text) > 0
